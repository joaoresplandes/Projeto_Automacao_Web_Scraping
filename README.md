# Projetos
## Neste respositório constitui-se os seguintes projetos
### Projetos_Automacao_Web_Scraping
- Pesquisa_Precos_Automatico

## Pesquisa_Precos_Automatico

### Contexto do Projeto
- Realizar uma busca automatica de preços em sites de busca, como Google Shopping, Buscapé (Contidos neste projeto) entre outros, reduzindo tempo, o qual seria grande caso a busca fosse feita de forma manual.

### Desenvolvimento do Projeto
- O mesmo foi realizado criando funções para cada um dos sites de busca, usando como base o arquivo BUSCAS.XLSX que contem os itens a serem buscados nos sites de busca GOOGLE SHOPPING e BUSCAPÉ. Por meio da biblioteca SELENIUN, foi possivel usar os atribuitos de HTML dos sites informados, automatizando o passo a passo de busca que seria feito de forma manual. Todos os produtos que forem encotrados, respeitando os critérios de PRODUTO, TERMOS_BANIDOS, PRECO_MINIMO e PRECO_MAXIMO, são armazenados em um DATAFRAME e exportados em formato XLSX e HTML, posteriormente encaminhados por email de forma tambem automática usado o YAGMAIL.
- O uso do Pathlib, foi para a criação de pastar para backup, uma para arquivos XLSX e outra HTML, onde serão armazenados seus respectivos tipos de arquivos, mas dentro, por tipo de produto separadamente.
 
#### Colunas do Arquivo BUSCAS.XLSX:
- PRODUTO -> nome do produto a ser buscado, de forma a separar todos os termos.
- TERMOS_BANIDOS -> Nomes que não podem conter no produto buscado.
- PRECO_MINIMO -> Preço mínimo é recomensavel para que o programa não encontre possiveis acessórios do que contem o nome do produto, itens não desejaveis. E tambem para se desconfiar de preços muito baixo, com possiveis golpes.
- PRECO_MAXIMO -> Preço máximo a que o usuário deseja pagar pelo produto.

#### Bibliotécas Usadas:
- Pandas
- Time.sleep
- yagmail
- pathlib
- selenium

#### Observações:
- O arquivo BUSCAS.XLSX que é usado pelo programa, deve estar contido no mesmo diretório que o arquivo do programa
- Necessario o uso do arquivo chromedriver.exe (caso esteja usando o google chrome) para que o SELENIUM possa abrir e usar o BROWSER.
- Site para download do arquivo: https://chromedriver.chromium.org/downloads a versão é a mesma que a do BROWSER
- A senha para o envio do e-mail deve ser gerado em Segurança, na conta do Gmail -> Gerir Conta/Segurança/Iniciar Sessão no Goole/Palavra-Passe de Aplicações/ e Gere sua senha para uso.
# Projeto_Automacao_Web_Scraping
