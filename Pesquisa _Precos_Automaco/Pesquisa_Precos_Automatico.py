## importando as bibliotecas
import pandas as pd
from time import sleep
import yagmail
import pathlib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

backup_excel = pathlib.Path('backup_excel') # definindo o diretorio BACKUP EXCEL
backup_html = pathlib.Path('backup_html') # definindo o diretorio BACKUP HTML

#1° abrir o browser(no caso o Google)
endereco_driver = r'C:\Users\joaof\.jupyter\chromedriver.exe'
navegador = webdriver.Chrome(endereco_driver)

## Importando as bases
produtos_df = pd.read_excel('buscas.xlsx')
print(produtos_df)

def busca_google_shopping(navegador, nome, termos_banidos, preco_minimo, preco_maximo):
    navegador.get('https://www.google.com.br')  # abrindo o browser do Google Chrome no site home do google

    #Separando os atributos em um lista para ser comparada e deixando tudo em minúsculo
    nome.lower()
    atributos_necessarios = nome.split(' ')
    termos_banidos.lower()
    atributos_nao_necessarios = termos_banidos.split(' ')

    # 1°Na barra de busca, procurar por determinado produto
    navegador.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(nome, Keys.ENTER)
    # Ir em shopping
    elementos = navegador.find_elements(By.CLASS_NAME, 'hdtb-mitem')
    for elemento in elementos:
        # print(elemento)
        if 'Shopping' in elemento.text:
            elemento.click()
            break

    lista_ofertas = []
    # com Inspecionar, pegar informações como nome, preço e link do produto
    elementos_produto = navegador.find_elements(By.CLASS_NAME, 'sh-dgr__grid-result')
    for n_produto in elementos_produto:

        # Buscando os nomes dos produtos
        produto = n_produto.find_element(By.CLASS_NAME, 'Xjkr3b').text.lower()
        # Liks dos respectivos produtos
        elemento_chield = n_produto.find_element(By.CLASS_NAME, 'KoNVE')
        elemento_antes = elemento_chield.find_element(By.XPATH, '..')
        link = elemento_antes.get_attribute('href')

        # critérios de busca - Verificando se o nome do produto corresponde ao critério de NOME e não contem algum dos TERMOS BANIDOS
        condicao_atributos_necessarios = True # De inicio, indica que está em FALSE
        for palavra in atributos_necessarios: # percorre todas as palavras splitadas para comparar com a palavra que atribuida a 'produto'
            if palavra not in produto: # verifica se a 'palavra' não está em 'produto':
                condicao_atributos_necessarios = False # altera a condição para FALSE de condicao de atributos necessarios

        condicao_atributos_nao_necessarios = True
        for palavra in atributos_nao_necessarios:
            if palavra in produto:
                condicao_atributos_nao_necessarios = False

        # caso os critérios não seja atendidos, os mesmos não serão incluidos na busca
        try:
            if condicao_atributos_necessarios and condicao_atributos_nao_necessarios:
                preco = n_produto.find_element(By.CLASS_NAME, 'a8Pemb').text
                preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
                preco = float(preco)

                # caso o preco não esteja dentro do intervalo estipulado, não será filtrando junto das buscas
                if preco_minimo <= preco <= preco_maximo:

                    # durante isso, colocar tudo em uma lista de tuplas (nome, preco, link)
                    lista_ofertas.append((produto, preco, link))
        except:
            continue
    return lista_ofertas

# Função para buscar preços no site buscapé
def busca_buscape(navegador, nome, termos_banidos, preco_minimo, preco_maximo):
    # 2° Na barra de busca do browser, colocar o endereço do buscapé e clicar
    navegador.get('https://www.buscape.com.br/')

    nome.lower()
    termos_banidos.lower()

    # realizando um tratamento das informaçõe de acordo com os critérios do dataset "buscas.xlsx"
    atributos_necessarios = nome.split(' ')
    atributos_nao_necessarios = termos_banidos.split(' ')

    lista_ofertas_buscape = []
    # Na barra de busca do próprio site, procurar por determinado produto
    navegador.find_element(By.CLASS_NAME,'search-bar__text-box').send_keys(nome, Keys.ENTER)
    sleep(3)
    resultados = navegador.find_elements(By.CLASS_NAME, 'Cell_Content__1630r')
    for elemento in resultados:
        produto = elemento.get_attribute('title').lower()

        #Link do respectivo produto
        link = elemento.get_attribute('href')

        # Verificando atributos necessarios e não necessarios:
        condicao_atributos_necessarios = True
        for palavra in atributos_necessarios:
            if palavra not in produto:
                condicao_atributos_necessarios = False

        condicao_atributos_nao_necessarios = True
        for palavra in atributos_nao_necessarios:
            if palavra in produto:
                condicao_atributos_nao_necessarios = False

        ## Verificação do nome se contem os atributos necessario e se não contem os atributos não necessarios:
        if condicao_atributos_necessarios and condicao_atributos_nao_necessarios:
            try:
                preco = elemento.find_element(By.CLASS_NAME, 'CellPrice_MainValue__3s0iP').text
                preco = preco.replace('R$', '').replace(' ','').replace('.','').replace(',','.')
                preco = float(preco)
                if preco_minimo <= preco <= preco_maximo:
                    # durante isso, colocar tudo em uma lista de tuplas (nome, preco, link)
                    lista_ofertas_buscape.append((produto, preco, link))
            except:
                continue
    return lista_ofertas_buscape

# Chama as funções das buscas para cada uma das lojas
lista_arquivo_html = []
for item in produtos_df.index:
    nome = produtos_df.iloc[item, 0]
    termos_banidos = produtos_df.iloc[item, 1]
    preco_minimo = produtos_df.iloc[item, 2]
    preco_maximo = produtos_df.iloc[item, 3]

    tabela_ofertas = pd.DataFrame()  # Criar um DataFrame de Tabela de Ofertas

    lista_google = busca_google_shopping(navegador, nome, termos_banidos, preco_minimo, preco_maximo)

    # Verificando se a lista_google não está vazia
    if lista_google:
        lista_precos = pd.DataFrame(lista_google, columns = ['Nome_Produto', 'Preco_Produto', 'Link_Produto'])
        tabela_ofertas = tabela_ofertas.append(lista_precos)

    lista_buscape = busca_buscape(navegador, nome, termos_banidos, preco_minimo, preco_maximo)

    # Verificando se a lista_buscape não está vazia
    if lista_buscape:
        lista_precos = pd.DataFrame(lista_buscape, columns = ['Nome_Produto', 'Preco_Produto', 'Link_Produto'])
        tabela_ofertas = tabela_ofertas.append(lista_precos)

    # Resetando o index da tabela de ofertas
    tabela_ofertas = tabela_ofertas.reset_index(drop = True)

    # ordenado valores do produtos de forma decrescente
    tabela_ofertas.sort_values(by='Preco_Produto')

    # Salva o arquivo em html
    tabela_ofertas.to_html(backup_html / f'tabela_ofertas_{nome}.html', index = False)

    # Salva o arquivo em excel
    tabela_ofertas.to_excel(backup_excel / f'tabela_ofertas_{nome}.xlsx', index=False)

    # adicionando arquivo pa, posteriormente serem separados em tabela de produtos diferentes no e-mail.
    lista_arquivo_html.append(tabela_ofertas)

# Por final, fecha o navegador da busca:
navegador.quit()

# Enviando email para o solicitante:
usuario = yagmail.SMTP(user= 'email_remetente', password='senha')
email_destino = 'email_destinatário'
assunto = 'Tabela de Pesquisa de Preço'

corpo_email =f'''
<p>Bom dia!</p>
<p>Segue a baixo a tabela dos preços do produtos encontrados levando com base os critérios de busca</p>
<p>Iphone 12 64Gb:</p>
<table>{lista_arquivo_html[0].to_html(index=False)}</table>
<p>RTX 3060</p>
<table>{lista_arquivo_html[1].to_html(index=False)}</table>
<p>Qualquer dúvida, estarei a dispossição</p>
<p>Att.,</p>
<p>João Pedro Resplandes da Silva
'''

# buscando anexos do e-mail
anexos = []
for v in backup_excel.iterdir():
    anexos.append(v)
usuario.send(to = email_destino,
            subject = assunto,
            contents = corpo_email,
            attachments = anexos)

print('Email Enviado...')

print('Busca Concluída')
