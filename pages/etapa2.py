import streamlit as st

st.set_page_config(
    page_title='Etapa 2: Limpeza de Dados'
)

st.header(':orange[Etapa 2: Limpeza dos Dados]')

st.image('https://media.giphy.com/media/Vdid4881G8lFkPFfeE/giphy.gif', width=300)
'''
A limpeza dos dados é uma etapa fundamental. Qualquer análise ou modelo de Machine Learning vai precisar
de dados "bom comportados". A etapa de limpeza de dados não serve apenas para determinarmos o que é útil
e o que é inútil, essa etapa vai muito além. :orange[É fundamental garantir a visualização dos dados e a padronização
das informações].

Após a Etapa 1 de raspagem dos dados e a tabulação desse num DataFrame, precisamos agora dar uma olhada na
formatação dessas informações e ver as necessidades que essa etapa irá nos exigir. 
'''

st.subheader(':orange[2.1. A primeira espiada no DataFrame:]')

'''
Nesse momento precisamos responder a uma série de perguntas:
* :orange[Qual o tamanho do nosso dataset? Quais os tipos de variáveis em cada coluna? Qual a quantidade de valores nulos? Existem 
dados duplicados?]

O nosso dataset ficou 400 linhas (apartamentos) e 12 colunas. Você pode estar se perguntando se o dataset é pequeno, e ele é 
mesmo. Porém, como o nosso projeto é apenas para construção de portfólio de estudos, acredito que temos imóveis suficientes 
para o objetivo. Não temos qualquer pretenção além de demonstrar as técnicas de ciência de dados aprendidas. 

Ao fazer o webscrapping, todos os dados foram raspados em forma de texto (com exceção da infraestrutura que era uma lista 
de textos), acontece que o próprio python/pandas já identificou algumas colunas numéricas. As colunas :orange[**quartos, 
suítes, banheiros e vaga**] já estão formatadas com *float/int*, mas todo o resto está em *object*, até mesmo variáveis 
que serão numéricas, como preço e metragem do imóvel. 

A respeito da presença de valores nulos/faltantes, temos alguns problemas:
* 67 imóveis não possuem valores de suítes e, verificando nos anúncios, percebemos que o site não possui a caixa com a informação
das suítes nos imóveis que não possuem suítes. Nesse caso, vamos substituir os valores nulos por 0. 
* Verificamos os imóveis que tinham valores nulos no banheiro e percebemos um preenchimento incorreto no site. Os imóveis possuiam
suítes e consequentemente banheiros. Atribuímos valores conforme a quantidade de suítes e um acréscimo de uma unidade para um 
banheiro social. 
* Atribuímos 0 para as vagas de garagem com valores nulos.
* Na metragem do imóvel, extraímos duas informações: metragem privativa e metragem total. A metragem privativa é, exclusivamente,
o apartamento da porta para dentro. Já a metragem total possui a metragem privativa somada com garagam e uma parcela da área comum
do condomínio. O nosso dataset estava com 123 valores nulos na metragem total e 2 valores nulos na metragem privativa. Por entender
que a metragem pode ser uma variável bastante importante na definição de preço do imóvel e temos uma grande quantidade de valores
nulos para a metragem total, optamos por excluir essa variável e permanecer apenas com a metragem privativa. 
* As coordenadas geográficas também não foram encontradas para outros 10 apartamenos. Dos dados faltantes, esse é o menor dos
problemas. As coordenadas não estariam no nosso modelo de Machine Learning, serão apenas utilizadas na Etapa 3 de análise exploratória.
'''

st.subheader(':orange[2.2. Novos problemas, novos desafios e novas soluções:]')
st.image('https://media.giphy.com/media/wZZPZwKY2QdG8RmCdh/giphy-downsized-large.gif', width=300)
'''
* :orange[*Formatação do Preço: *]

Após tratar dos valores nulos, agora temos o problema das formatações e tipos de variável. A começar pelo preço do imóvel, 
importantíssimo, que será o nosso :orange[*target*] no modelo de Machine Learning. Ao extrair do site, temos o preço no formato *object*, 
mas além disso o preço está com o *'R\$'* na frente do número. Sendo assim, precisamos retirar o *'R\$'* e deixar no formato float
com o padrão brasileiro separando as casas decimais por vírgula. Para isso, usamos a biblioteca :orange[regex] para fazer a formatação. 
'''
code1 = '''
# Função para limpar a variável preço: 
def limpar_preco(preco):
    # Retirar da frente o 'R$'
    preco_sem_r = re.sub(r'^R\$','', preco)
    # Retirar os pontos:
    preco_sem_pontos = re.sub(r'\.','', preco_sem_r)
    # Substituir a vírgula por poonto e retornar no retormato float
    preco_em_float = re.sub(r',','.', preco_sem_pontos)
    return float(preco_em_float)
# Aplicando na variável preço
aptos.preco = aptos.preco.apply(limpar_preco)
'''
st.code(code1, language='python')
'''
* :orange[*Formatação da Metragem do Imóvel: *]

Temos um problema na variável 'privativos', que informa a metragem privativa do imóvel. No site, o valor numérico vinha
acompanhado do 'm$^2$'. Precisamos retirar a sigla da metragem e ficar apenas com a parte numérica para que modelo de 
machine learning funcione. Novamente vamos utilizar :orange[regex] para o tratamento.
'''
code2 = '''
# Função para limpar as variáveis que determinam área e possuem "M2" (metro quadrado) no final.
def extrair_metros_quadrados(texto):
    # Se for nulo, vai continuar sendo nulo
    metragem = texto
    # Tenta retirar o 'M2' do final para os dados que apresentarem e transforma para inteiro.
    try:
        match = re.search(r'(\d+) M2', texto)
        metragem = int(match.group(1)) 
    except: 
        pass
    return metragem
# Aplica a função na variável 'privativos' e na variável 'totais'
aptos.privativos = aptos.privativos.apply(extrair_metros_quadrados)
'''
st.code(code2, language='python')
'''
* :orange[*Formatação das Coordenadas Geográficas: *]

Ao extrair as coordenadas geográficas de latitude e longitude no site, o texto retornada era uma string única com as duas 
informações. Precisamos separar longitude e latitude em duas novas colunas no nosso dataset, que chamaremos de *'lat'* e *'long'*.
'''
code3 = '''
# Função para extrair as coordenadas dos links do Google Maps:
def extrair_coordenadas(link):
    # Se não possuir a informação, returna nulo.
    if link is None or pd.isna(link):
        return None, None
    # Padrão da regex
    padrao = r'q=(-?\d+\.\d+), (-?\d+\.\d+)'
    # Busca pelo padrão e salva as duas informações de latitude e longitude
    dados = re.search(padrao, link)
    # Defini as novas variáveis e retorna a dupla:
    if dados:
        latitude = float(dados.group(1))
        longitude = float(dados.group(2))
        return latitude, longitude
    else:
        return None, None
# Cria duas novas colunas (lat e long) para receberem os valores de latitude e longitude.
aptos['lat'], aptos['long'] = zip(*aptos['coordenadas'].map(extrair_coordenadas))
'''
st.code(code3, language='python')

'''
* :orange[*Formação do Endereço do Imóvel*]

Assim como as coordenadas que foram raspadas num texto único, o endereço também ocorreu no mesmo problema. Precisamos 
utilizar as regex para separar a rua com o número, bairro e cidade em três novas colunas. 
'''
code4 = '''# Função para separar o endereço em 'Rua com número', 'Bairro' e 'Cidade'
def separar_endereco(endereco):
    # Inicializa as variáveis para as partes do endereço
    numero_rua = None
    bairro = None
    cidade = None

    # Use regex para extrair as partes do endereço
    dados = re.match(r'^(.*?), (\d+), (.*?) - (.*?)$', endereco)
    # Armazenar os valores e retorna:
    if dados:
        numero_rua = dados.group(1) + ", " + dados.group(2)
        bairro = dados.group(3)
        cidade = dados.group(4)
    return numero_rua, bairro, cidade
# Cria três novas colunas para receberem as três informações:
aptos['numero_rua'], aptos['bairro'], aptos['cidade'] = zip(*aptos['endereco'].apply(separar_endereco))'''
st.code(code4, language='python')
st.subheader(':orange[2.3. Demais features: DataFrame vai tomando forma:]')
st.image('https://media.giphy.com/media/b7tZKvYa7G3GDKpmJn/giphy.gif', width=300)
'''
* :orange[*O problema das features de infraestrutura:*]
Como comentado anteriormente, queremos verificar se os imóveis possuem algumas qualidades importantes que podem impactar 
no preço. Vamos criar 5 novas características: :orange[piscina, gás central, salão de festa, elevador e academia]. Nesse 
momento, uma das nossas colunas **infra** contém uma lista com todos os itens presentes no condomínio em formato de texto. 
A variedade de itens presentes nas listas é enorme, e se fossemos criar uma coluna para avaliar a presença de cada características, 
teríamos um dataset com muitas colunas, o que poderia gerar um problema de alta dimensionalidade. Sendo assim, vamos nos restringir
aos 5 itens especificados anteriormente. 

Para resolver o problema, tivemos que fazer dois passos: 

* Transformar as strings da coluna :orange[infra] em uma lista.

* O primeiro é criar uma lista com todas características que um condomínio pode ter. Isso foi necessários para buscar 
nomes distintos para características iguais ou muito próximos, como por exemplo 'Sala Fitness' e 'Academia', ou ainda 'Gás Central'
e 'Aquecimento a Gás'.  
'''
code5 = ''''
# Junta todos os itens de infraestrutura dos condomínios em um único conjunto:
aptos['infra'] = aptos['infra'].apply(lambda x: eval(x) if isinstance(x, str) else x)

infra_total = list(set(item for lista in aptos['infra'] for item in lista))
'''
st.code(code5, language='python')

'''
* Para cada um dos itens (:orange[piscina, gás central, salão de festa, elevador e academia]), vamos criar uma função que
verifica se aquele item está na lista da coluna :orange[infra] e retorna 1 caso positivo e 0 caso negativo.
'''

code6 = '''
# Verificar os condomínios que possuem 'Piscina Coletiva' na lista de infraestrutura:
def check_piscina(lista):
    # Define como 0 a ausência de piscina
    valor = 0
    # Varre as linhas da coluna buscando por piscina e caso seja verdadeiro atribui 1
    if 'Piscina Coletiva' in lista:
        valor = 1
    return valor
# Cria a coluna booleana da piscina.
aptos['piscina'] = aptos.infra.apply(check_piscina)
'''
st.code(code6, language='python')

st.subheader(':orange[2.4. Últimos ajustes: Preparando para decolagem:]')
st.image('https://media.giphy.com/media/YrkUExkYM5LRMDCs6g/giphy.gif', width=300)

''''
Analisando os dados, pudemos encontrar alguns dados que não faziam muito sentido para o nosso projeto. Por exemplo, encontramos
um apartamento com 12 quartos e 21 vagas de garagem que, ao verificar o anúncio manualmente, se tratava de um conjunto de kitnets.
Além disso, alguns imóveis possuiam valores extremamente altos e como o nosso objetivo com o projeto é puramente estudo, vamos eliminar
esses outliers de preço. Já será bastante difícil de obtermos um modelo com boa previsão pela quantidade pequena de dados, então vamos 
eliminar alguns problemas que dificultariam ainda mais a nossa jornada. Num projeto real, esse tipo de decisão é muito mais complexa de se tomar. 
'''

code7 = '''
# Retirar um imóvel que possui 21 vagas de garagem. Isso está bem fora na normalidade:
aptos = aptos[aptos['vagas'] <= 6]
# Vamos retirar os imóveis muito luxuosos e possuem valores extremamente altos utilizando a remoção de outliers por IQR.
q1_preco = aptos.preco.quantile(.25)
q3_preco = aptos.preco.quantile(.75)
iqr_preco = q3_preco - q1_preco

inf_preco = q1_preco - (1.5*iqr_preco)
sup_preco = q3_preco + (1.5*iqr_preco)

print(f'IQR Preco: {iqr_preco}.')
print(f'Limite Inferior: {inf_preco}.')
print(f'Limite Superior: {sup_preco}.')

outliers_preco = len(aptos[aptos.preco > sup_preco])
print(f'Outliers de preço: {outliers_preco}.')
print(f'% do dataset perdida em outliers {round(outliers_preco/aptos.shape[0],3)*100}%.')

aptos_copy = aptos.copy()
aptos_copy.drop(aptos[aptos.preco > sup_preco].index, axis = 0, inplace = True)
'''
st.code(code7, language='python')

''''
* :orange[*Últimos ajustes:*]

Finalmente, excluímos algumas colunas que não nos interessam mais como: :orange[endereço](substituído por três novas colunas com 
as informações segmentadas), :orange[infra, metragem total e coordenadas] também substituídas sem perda de informação relevante.
'''
code8 = '''
# Exclui algumas alunos que não são mais necessárias:
df_limpo = aptos_copy.drop(['Unnamed: 0', 'endereco','infra','coordenadas',], axis = 1)
'''
st.code(code8, language='python')
'''
Filtramos pela cidade de Itajaí, já que alguns imóveis de cidades vizinhas foram raspados durante o processo de webscrapping
'''
code9 = '''
# Filtra apenas os apartamentos na cidade de Itajaí/SC:
df_limpo_itajai = df_limpo.loc[df_limpo['cidade'] == 'Itajaí/SC']
'''
st.code(code9, language='python')
'''
Conversão das algumas colunas do formato float para int.
'''
code10 = '''
# Converter os tipos de algumas colunas que estão em formato 'float' para 'int'. 
colunas_converter = ['suites','banheiros','vagas','privativos']
df_limpo_itajai[colunas_converter] = df_limpo_itajai[colunas_converter].astype('int64')
# Verifica os tipos de dados em cada coluna:
df_limpo_itajai.dtypes
'''
st.code(code10, language='python')
'''
Fizemos um cópia final e salvamos o arquivo .csv'''
code11 = '''
# Determina o dataset final pós limpeza e tratamento dos dados:
df_final = df_limpo_itajai.copy()

# Salva o novo dataset:
df_final.to_csv('df_final.csv')
'''
st.code(code11, language='python')
st.subheader(':orange[Etapa 3: Concluída. Agora o céu é o limite.]')
st.image('https://media.giphy.com/media/NRWFU8lq7hCXS/giphy.gif', width=300)

st.divider()
st.markdown('''Desenvolvido por: **Pedro Lourenço Mendes Júnior**''')
st.write("""<div style="width:100%;"><a href="https://www.linkedin.com/in/mendesjuniorpedro/" style="float:center"><img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="40px"></img></a>""" + """<a href="https://github.com/pedromendesjr" style="float:center"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="32px"></img></a></div>""", unsafe_allow_html=True)


