import streamlit as st

st.set_page_config(
    page_title='Etapa 1: Webscrapping de dados'
)

st.title(':blue[Etapa 1: Webscrapping de Dados]')

st.subheader(":blue[1.1. Dados: Quais? Quem? Onde? Por quê?]")

st.image('https://media.giphy.com/media/xT9C25UNTwfZuk85WP/giphy-downsized-large.gif', width=400)
'''


O projeto não existe sem os dados. E é nisso que a primeira etapa do projeto concentrou-se, em
fornecer os dados necessários para a realização do projeto. A ideia, desde o início do projeto, foi
de criar um modelo de previsão de preços de venda de imóveis. E neste momento, já surge o primeiro questionamento:

* :blue[_Quais imóveis serão utilizados no projeto?_]

Por se tratar de um dos meus primeiros projetos, preferi limitar para imóveis da minha cidade, Itajaí, uma
cidade do litoral de Santa Catarina, vizinha de Balneário Camboriú, que carrega uma fama maior nacionalmente.
Por serem imóveis da minha cidade, eu conhecia melhor as regiões da cidade, bairros de classe mais alta, 
bairros mais próximos do centro da cidade, regiões valorizadas e etc. Entendi que isso poderia me ajudar 
durante a realização do projeto. Escolhido o local do projeto, agora temos a questão:

* :blue[_Onde encontrar os dados necessários?_]

Essa foi uma etapa de investigação pela internet, existem grandes plataformas de anúncios como **OLX**, 
**Zap Imóveis** e etc. Só que essas plataformas possuem um problema difícil de contornar: a falta de 
padronização nos anúncios. Por se tratar de plataformas abertas onde qualquer usuário pode criar um anúncio, 
isso cada gerando formar diferentes de fornecer as informações por cada usuário. Além disso, percebemos uma 
repetição/duplicidade muito grande nos imóveis, pois o mesmo imóvel pode estar sendo oferecido por vários corretores e/ou
imobiliárias, e por isso, cada um criava um anúncio diferente para o mesmo imóvel. 

Com a dificuldade de utilizar os dados dessas plataformas, surge uma segunda opção que é utilizar os dados
dos sites de imobiliárias. O problema da duplicidade é quase inexistente, o preenchimento dos campos com as 
informações era mais bem comportado, poucas informações faltantes e etc. Sendo assim, optei por utilizar um
site de uma imobiliária. A imobiliária escolhida foi a [Max Imóveis](https://maximoveis.com.br/), uma das 
maiores imobiliárias da cidade.
'''
st.subheader(':blue[1.2. Dados encontrados: investigação inicial.]')
st.image('https://media.giphy.com/media/Gpf8A8aX2uWAg/giphy-downsized-large.gif',width=400)

'''
O processo de webscrapping ou raspagem de dados, requer algumas ferramentas extras. Existem diferentes 
bibliotecas em Python que lhe auxiliam nesse processo como Selenium, Scrapy, BeautifulSoup e entre outras.
Para o projeto, utilizamos apenas o Selenium. E ao entrar no site da imobiliária e pesquisar por 'Apartamentos'
na cidade de 'Itajaí', chegamos na [página](https://maximoveis.com.br/venda/apartamento/itajai/) com a lista dos imóveis com essas características. 

Aqui é importante entender que o processo de raspagem de dados é um procesos para extrair informações que estão
visuais no site/HTML que está sendo impresso na tela do dispositivo. Não temos acesso ao banco de dados 
estruturados onde a imobiliária armazena os seus dados. Temos que fazer uma raspagem 'personalizada' e 'manual'
pelo site para extrair o que necessitamos. 

* :blue[_Quais dados extrair?_]

Como o objetivo é criar um web app de predição de preço dos imóveis, é interessante coletar informações que 
sejam importantes para determinar o preço do imóvel. Sendo assim, vamos capturar as seguintes informações básicas:
**preço, quantidade de quartos, suítes, banheiros e vagas na garagem, metragem do apartamento e endereço**. Além disso, 
também é importante conhecer **características do condomínio** que podem impactar no preço. Existem diversos itens
de infraestrutura que impactam no preço, mas optamos por pegar apenas a presença de **piscina, elevador,
gás central, salão de festas e academia**. Futuramente, o projeto pode se estender para outros itens. Também desejamos
capturar, se possível, o **latitute e longitude do imóvel**. Isso não será utilizado no modelo de Machine Learning, 
mas pode ser útil na visualização dos dados. 
'''


st.subheader(':blue[1.3. Os primeiros problemas começam a aparecer.]')
'''
Após a pesquisa, o site lista *cards* dos imóveis com algumas informações básicas, fotos, e ao clicar nos *cards*
somos redirecionados para a página do imóvel com as informações detalhadas. Acontece que os *cards* não possuem
todas as informações que necessitamos, ou seja, teremos que entrar em cada *card* e acessar a página detalhada de
cada imóvel. Sim, isso pareceu bem complexo e assustador para quem nunca havia realizado um webscrapping antes.
Além disso, o site da imobiliária funciona semelhante as redes sociais atuais, onde temos uma *'timeline infinita'*.
Ou seja, os dados não são apresentados/carregados na tela por completo, eles vão aparecendo conforme deslizamos na página. 
Ao rolar a página, novos *cards* de imóveis iam aparecendo e os *cards* iniciais desaparecendo, inclusive no código HTML. 
Sendo assim, dificulta a raspagem de dados por não termos acesso a todos os *cards* via HTML diretamente ao entrar no site. 
'''
st.subheader(':blue[1.4. Mãos à obra: Hora de resolver problemas.]')
st.image('https://media.giphy.com/media/QAU6ZKDf7q8nS33IjN/giphy.gif',width=400)

'''
* :blue[_Ligar a máquina: Conectar o Selenium ao site:_]
'''
code1 = '''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Navega para a URL de login
driver = webdriver.Firefox()

tipo_imovel = 'apartamento'
cidade = 'itajai'

# Navega para a URL e maximiza a página:
driver.get('https://maximoveis.com.br/venda/'+ tipo_imovel + '/' + cidade + '/')
driver.maximize_window()
time.sleep(3)

# Lista para guardar os links das paginas:
links = []
'''
st.code(code1, language='python')
'''
Inicialmente importamos as bibliotecas necessárias para o projeto. O 'webdriver' é o recurso do Selenium para
navegar pelo site, é o principal comando que vamos utilizar. O 'driver.get()' é o responsável por navegar
até o link fornecido. Depois maximizamos a janela do navegador com o 'driver.maximize_window()', isso é importante por conta de alguns sites
responsivos que podem ocultar informações com janelas pequenas. Por fim, o 'time.sleep(3)' é apenas uma
pause de 3 segundos, isso é importante para que o site tenha tempo de carregar todas as informações. 
'''


'''
* :blue[_O problema da 'timeline infinita':_]

Ao deslizar no site podemos perceber que uma parte dos *cards* é carregada e uma outra parte é ocultada. Assim, 
vamos utilizar o webscrapping para capturar os links de cada *card* conforme vamos deslizando no site. A estratégia que 
eu utilizei é verificar quantos *'Page Downs'* eu necessitaria para percorrer todos os *cards* de imóveis e chegar até o final
da página. E conforme o Selenium fosse enviando os *'Page Downs'*, ela já iria percorrendo os *cards* e capturando os links 
de cada card. 
'''
code2 = '''
# Selecionando o local onde irá ser feito o PAGE_DOWN:
box_page = driver.find_element(By.CSS_SELECTOR,'.clb-search-result-property')
i = 0

while i < 70:
    # PAGE_DOWN aguardando 1 segundo:
    box_page.send_keys(Keys.PAGE_DOWN)
    box_page.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    i = i + 1'''
st.code(code2, language='python')
'''
Nessa parte do código utilizamos o Selenium para selecionar a parte do site onde estão os cards dos apartamentos.
É nessa parte que queremos dar o *'Page Down'* para varrer todos os *cards*. Criamos um *'while'* com um iterador que vai
dar *'page downs'* até o final da página. Verificamos que i < 70 era um bom limitador, já era suficiente para passar por
todos os *cards* de imóveis. Sempre finalizamos cada etapa com um 'time.sleep(1)' para dar tempo de carregamento da página.
'''
code3 = '''
# Selecionando as páginas para procurar os links:
    pages = driver.find_elements(By.CLASS_NAME,'page')
    for page in pages:
        # Selecionando os cards dentro das páginas:
        cards = driver.find_elements(By.CLASS_NAME,'titulo-anuncio')
        for card in cards:
            # Pegando o link dentro de cada card:
            link = card.find_element(By.TAG_NAME,'a').get_attribute('href')
            # Vendo se é um link novo ou não:
            if link not in links:
                links.append(link)
'''
st.code(code3, language='python')
'''
Ainda dentro da laço *'while'*, verificamos que os *cards* dos imóveis estão separados por *'pages'*, que é o nome
da classe no código HTML. Então demos um *'driver.find_elements'* para capturar todas as *'pages'* do site.
Depois, para cada *'page'* dentro das *'pages'*, vamos capturar os *cards* de imóveis que estão ali dentro através
da classe *'título-anuncio'*. Todos os *cards* compartilham dessa classe. 

Dentro de cada *card*, vamos buscar os links de cada página de detalhes dos imóveis. O link se encontra numa
div de HTML com a *tag <a>* e o atributo *'href'*. Com o link em mãos, vamos adicionar esse link a nossa lista 
de links previamente definida. Como não queremos repetições de links, colocamos a condição no final para 
garantir valores únicos.

Com isso, teremos no final uma lista com os links de todos os imóveis. 
'''
code4 = '''
df_links = pd.DataFrame({
    'links':links
})

df_links.to_csv('df_links.csv')
'''
st.code(code4, language='python')
'''
Só geramos um dataframe dos links e salvamos em um arquivo *.csv* os dados. Assim finalizamos a etapa de obter
todos os links dos imóveis que queremos capturar as informações. 

**Problem 1: Done!**
'''
st.image('https://media.giphy.com/media/5z0cCCGooBQUtejM4v/giphy.gif', width=200)

st.divider()

st.subheader(':blue[1.5. Webscrapping dos imóveis: Chegou o grande momento:]')
st.image('https://media.giphy.com/media/vyf5C83uin6oMwUt6V/giphy.gif', width=300)
'''
Municiados dos links de cada imóvel e em um novo arquivo Python, agora temos que acessar cada link e raspar as informações que queremos. 
Precimos investigar o código HTML do site e encontrar cada bloco (div) que contém as informações úteis para acessa-las
com o driver do Selenium.
'''
code5 = '''
# Abrir navegador Firefox:
driver = webdriver.Firefox()

# Dataset com os links dos imóveis:
df_links = pd.read_csv('df_links.csv')

links = df_links['links']

#Criando conjunto de dados:
colunas = ['titulo','endereco','preco','quartos','suites','banheiros','vagas','privativos','total','infra','coordenadas','link']
aptos = pd.DataFrame(columns=colunas)
index = 0
'''
st.code(code5, language='python')
'''
Vamos abrir o navegador com o Selenium, resgatar os nossos links salvos no arquivo *'df_links.csv'* e criar o
DataFrame que vai receber os nossos dados.
'''
code6 = '''
for link in links:
    # Acessar site, maximizar janela e tempo de carregamento:
    driver.get(link)
    driver.maximize_window()
    time.sleep(3)

    # Variável para guarda as informações de cada imóvel:
    aptos.loc[index] = [None] * 12
    aptos.loc[index].link = link
    
    # #Informações do topo da página (Título anúncio, endereço imóvel e preço):
    topo = driver.find_element(By.ID,'clb-imovel-topo')
    aptos.loc[index].titulo = topo.find_element(By.CLASS_NAME,'row').find_element(By.TAG_NAME,'h1').text
    aptos.loc[index].endereco = topo.find_element(By.CLASS_NAME,'endereco').text
    aptos.loc[index].preco = topo.find_element(By.CLASS_NAME,'thumb-price').text
'''
st.code(code6, language='python')
''''
Nessa etapa do código acessamos cada link da nossa lista de links, maximizamos a janela e demos um tempo de carregamento 
pro site. Criamos um linha no DataFrame nula e já colocamos o link na respectiva coluna. 
A ideia de criar uma linha nula é apenas para o caso de termos informações faltantes durante o webscrapping e o código não travar. 

Navegando pelo HTML do site, percebemos uma div na parte superior do site que fornecia algumas informações 
importantes para o projeto. Podemos acessar a div pela seu ID único *'clb-imovel-topo'*. O processo de webscrapping,
nesse momento, é um processo de investigação para encontrar uma forma de acessar o valor desejado, o Selenium 
consegue acessar itens de diferentes formas, e cabe ao usuário encontrar uma melhor maneira para isso. Muitas vezes, 
o problema possui mais de uma solução para se chegar no valor desejado. Conseguimos acessar o título do anúncio,
o endereço do imóvel e o preço através dos nomes das classes de cada um. Repare que a informação é sempre extraida 
em forma de texto. Numa etapa posterior, teremos que tratar todas essas informações. 

* :blue[_Já conseguimos: Título, endereço, preço e link. Seguimos..._]
'''

code7 = '''
    # # Informações do imóvel:
    imovel = driver.find_element(By.CLASS_NAME,'property-amenities')
    try: # Buscar quantidade de quartos:
        aptos.loc[index].quartos = imovel.find_element(By.ID,'amenity-dormitorios').find_element(By.TAG_NAME,'span').text
    except:
        pass
'''
st.code(code7, language='python')

'''
Encontramos uma outra caixa de informações importantes no site. Conseguimos acessar essa bloco de código pela
sua *'class: property-amenities'*. Nesse bloco de código HTML, podemos acessar cada parte através do seu ID único,
e depois acessar o texto através da 'tag' de HTML *'<span>'*. Fizemos esse processo com as ID`s: *amenity-dormitorios,
amenity-suites, amenity-banheiros, amenity-vagas, amenity-privativa e amenity-area-total* para pegar as quantidades de 
dormitórios, suítes, banheiros, vagas de garagem e áreas tanto privativa quanto total. Tivemos que usar um *try/except*
pois alguns imóveis estão com informações faltantes e a ID não era acessada pelo Selenium, o que gerava um erro. Com essa 
solução, o Selenium tentava acessar a ID e caso não encontrasse, ele simplesmente pulava e ia para a próxima linha de 
código. 
'''

code8 = '''
# Características do imóvel (Infraestrutura do condomínio/imóvel):
    aptos.loc[index].infra = []
    try:
        caracteristicas = driver.find_element(By.CSS_SELECTOR,'html body.page-template.page-template-page-imovel.page-template-page-imovel-php.page.page-id-6 main#page div.pg-imovel div#form-start-floating.contact-form-rail section#clb-descricao.printable div.container div.row div.col-xs-12.col-sm-12.col-md-7.col-lg-8.clb-infra-imo')
        infras = caracteristicas.find_elements(By.TAG_NAME,'p')
        for p in infras:
            aptos.loc[index].infra.append(p.text)
    except:
        pass
'''
st.code(code8, language='python')
'''
Vimos que os itens de infraestrutura do imóvel/condomínio ficam dispostos em uma outra parte do código HTML. E não seria 
possível acessar apenas os itens que desejámos (piscina, gás central e etc). Sendo assim, a solução encontrada foi criar uma
lista vazia, acessar o elemento HTML que possuía as características do condomínio, através do CSS_SELECTOR, e acessar 
cada tag *<p>*. Ao acessar a tag individualmente, capturamos o texto e adicionamos a lista da infraestrutura do condomínio. Ou 
seja, a coluna 'infra' é uma coluna de listas de itens de infraestrutura de cada um dos apartamentos.

* :blue[_Com isso, temos quase todas as informações desejadas._]
'''

code9 = '''
# Localização do imóvel (Link GoogleMaps):
    frame = driver.find_element(By.ID,'form-start-floating').find_element(By.TAG_NAME,'iframe')
    coordenadas = frame.get_attribute('data-src')
    aptos.loc[index].coordenadas = coordenadas
'''
st.code(code9,language='python')
'''
Por fim, ainda dentro do *'for'* inicial, encontramos um 'ID' que possuía uma tag *'iframe'* capaz de fornecer os dados
geográficos do apartamento. O Selenium requer um cuidado especial nos casos de 'iframe', mas com o código acima conseguimos 
obter os dados das coordenadas em formato de texto. 
'''

code10 = '''
# Fechar navegador:
driver.quit()

# Salvar o dataset:
aptos.to_csv('aptos.csv')

'''
st.code(code10,language='python')
'''
Finalmente, fechamos o navegador com o Selenium e salvamos o nosso queridíssimo DataFrame com os dados dos apartamentos. 
'''

st.divider()
st.subheader('1.6. Conclusão da Etapa e próximos desafios:')
st.image('https://media.giphy.com/media/2uI9jYTJLILfkAtMqQ/giphy.gif', width=400)
'''Esse foi o nosso webscrapping para obtenção dos dados dos imóveis. Como dito antes, existem diversas maneiras para 
fazer a raspagem dos dados no site. É um processo extremamente desafiador, ainda mais se tratando do primeiro webscrapping. 
Uma porção de erros incontáveis ocorreram durante o processo, mas aos poucos fomos solucionando-os. Tenho certeza que não
são as melhores soluções, mas chegaram ao resultado esperado e desejado. 

Temos um dataset com as informações mas, se vocês repararam, todas as informações estão no formato de texto (string). 
Além disso, certamente aparecerão valores nulos em alguns dados. Vamos precisar fazer uma limpeza e formatação dos dados.
A Etapa 2 do projeto cuidará disso. Vamos deixar os dados brilhando, tudo ajustado para a análise e depois modelagem de 
machine learning. 

Até a Etapa 2 e obrigado pela leitura.
'''
st.image('https://media.giphy.com/media/m93v8Rl9GBaW61AmOK/giphy.gif', width=300)

st.divider()
st.markdown('''Desenvolvido por: **Pedro Lourenço Mendes Júnior**''')
st.write("""<div style="width:100%;"><a href="https://www.linkedin.com/in/mendesjuniorpedro/" style="float:center"><img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="40px"></img></a>""" + """<a href="https://github.com/pedromendesjr" style="float:center"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="32px"></img></a></div>""", unsafe_allow_html=True)

