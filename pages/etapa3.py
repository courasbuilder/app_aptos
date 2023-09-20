import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import plotly.express as px



st.set_page_config(
    page_title='Etapa 3: Painel de dados'
)

df_final = pd.read_csv('datasets/df_final.csv')

def titulo():
    st.title(":red[Etapa 3: Análise Exploratória dos dados de imóveis:]")

    '''
    O presente painel trata-se de uma breve análise exploratória dos dados dos apartamentos à venda em 
    Itajaí - Santa Catarina. Os dados foram obtidos através de webscrapping no portal de uma imobiliária
    da cidade. Para maiores informações do processo de obtenção dos dados, o leitor pode conferir nas etapas 
    anteriores.
    '''

def load_data(data):
    st.subheader(':red[Dataset Completo:]')
    data.drop(['Unnamed: 0', 'link'], axis = 1, inplace = True)
    st.dataframe(data)
    st.write(f'O dataset possui {data.shape[0]} linhas e {data.shape[1]} colunas.')
    st.subheader(':red[Colunas do Dataset:]')
    st.markdown('''
    * :red[**titulo**]: Título do imóvel no anúncio.
    * :red[**preco**]: Preço do imóvel.
    * :red[**quartos, suites, banheiros, vagas**]: Quantidades em cada imóvel
    * :red[**privativos**]: Metragem da área privativa do imóvel.
    * :red[**lat e long**]: Coordenadas geográficas do imóvel.
    * :red[**numero_rua, bairro, cidade**]: Endereço do imóvel.
    * :red[**piscina, gas_central, elevador, salao, academia**]: Informações sobre infraestrutura do condomínio,
    o valor de 1 represente que o imóvel possui a infraestrutura e 0 quando não possui.
    ''')

def infos(data):
    st.subheader(':red[Informações Gerais:]')
    st.table(data.describe())
    st.markdown('''
    * A média de preços dos imóveis é de, aproximadamente, 1,4 milhões de reais, com imóveis a partir
    de 200 mil e podendo chegar até os 13 milhões de reais; 
    * A média de quartos é de 2,5 enquanto o de suítes é de 1,5. Todos os imóveis possuem quartos e muitos 
    imóveis possuem suítes, já que o 1o quartil das suítes é 1. 
    * Na média os imóveis possuem 2,6 banheiros, porém menos de 25% dos imóveis possuem mais de 2 banheiros.
    * Alguns imóveis não possuem vagas de garagem, talvez tratam-se de vagas compartilhadas ou de kitnets 
    que estão catalogadas como apartamentos. Além disso, mais de 50% dos imóveis possuem duas vagas de garagem.
    * A média dos imóveis é de 105 metros quadrados, sendo o menor deles com 34 metros quadrados. Destaca-se
    que mais a mediana é de 83 metros, então temos uma boa quantidade de apartamentos grandes que estão elevando
    essa média.
    * Dos itens de infraestrutura do condomínio, o mais presente é o Salão de Festas com quase 92%. Elevador
    e Piscina também fazem parte de muitos imóveis com 84% e 80%. Academia em 68% dos imóveis e o Aquecimento
    a Gás em 23%. 
    ''')

def correlacao(data):
    st.subheader(':red[Heatmap de Correlação das Variáveis:]')
    variaveis_numericas = ['preco','quartos','suites','banheiros','vagas','privativos','piscina','gas_central','elevador','salao','academia']
    corr_df = data[variaveis_numericas].corr(method='pearson')
    fig,ax = plt.subplots()
    sns.heatmap(corr_df, ax = ax, annot=True)
    st.write(fig)
    st.markdown(
    '''
    * Como poderíamos suspeitar inicialmente, as características dos imóveis como quartos, suítes, banheiros,
    e área privativa, possuem uma boa correlação. Afinal uma suíte já implica num banheiro, os imóveis maiores 
    devem possuir mais quartos e etc. 
    * O preço possui uma correlação maior com a metragem, seguido das vagas de garagem e do número de quartos. 
    É bastante comum nos imóveis a negociação de vagas extras de garagem, venda de vagas entre os condôminos,e 
    isso pode impactar no preço dos imóveis. Dependendo do imóveis, as vagas possuem um valor bastante significativo.
    * Entre as variáveis das características do apartamento e as características do condomínio, as correlações
    são bem menores. Ainda assim, as que apresetam valores intermediárias de correlação são preço e suítes,
    correlacionados com a presença de gás central, elevador e academia.
    *Entre as variáveis do condomínio, a academia apresenta maiores valores, sendo assim, podes suspeitar que 
    os imóveis que possuem academia também devem possuir os demais itens de infraestrutura.   
    '''
    )

def filtros(data): 
    st.title(':red[Filtragem dos imóveis:]')
    st.write('Utilize os filtros para selecionar imóveis com características do seu interesse:')
    select_infra = st.multiselect('Seleciona os itens de infraestrutura dos imóveis:', ['Piscina', 'Aquecimento à Gás', 'Elevador','Salão de Festas', 'Academia'])
    if select_infra == []:
        st.warning('Você não selecionou itens extras de infraestrutura.')
    else:
        st.success(f'Você selecionou os seguintes itens: {select_infra}')


    min_quartos, max_quartos = st.select_slider('Quantidade de Quartos:', range(1,6,1), value=(1,5))
    filtro_quartos = (data['quartos'] >= min_quartos) & (data['quartos'] <= max_quartos)

    min_suites, max_suites = st.select_slider('Quantidade de Suítes:', range(0,6,1), value=(0,5))
    filtro_suites = (data['suites'] >= min_suites) & (data['suites'] <= max_suites)

    min_banheiros, max_banheiros = st.select_slider('Quantidade de Banheiros:', range(1,7,1), value=(1,6))
    filtro_banheiros = (data['banheiros'] >= min_banheiros) & (data['banheiros'] <= max_banheiros)

    min_vagas, max_vagas = st.select_slider('Quantidade de Vagas:', range(0,7,1), value=(0,6))
    filtro_vagas = (data['vagas'] >= min_vagas) & (data['vagas'] <= max_vagas)

    col_priv_1, col_priv_2 = st.columns(2)
    with col_priv_1:
        min_privativos = st.number_input('Metragem mínima do imóvel', min_value=32, max_value = 512, value = 34, help='Os imóveis possuem entre 34 e 512 metros quadrados.')
    with col_priv_2:
        max_privativos = st.number_input('Metragem máxima do imóvel', min_value = 512, max_value = 512, value = 512, help='Os imóveis possuem entre 34 e 512 metros quadrados.')
    col_preco_1, col_preco_2 = st.columns(2)
    filtro_metragem = (data['privativos'] >= min_privativos) & (data['privativos'] <= max_privativos)

    with col_preco_1:
        min_preco = st.number_input('Preço mínimo do imóvel', min_value=200000, value = 200000)
    with col_preco_2:
        max_preco = st.number_input('Preço máximo do imóvel', min_value = 201000, value = 13500000)
    filtro_preco = (data['preco'] >= min_preco) & (data['preco'] <= max_preco)

    bairros = data['bairro'].unique()
    all_bairros = st.checkbox('Selecionar todos os bairros.', value=True)
    if all_bairros:
        select_bairros = st.multiselect('Selecione os bairros que desejar:',bairros, bairros)
    else:
        select_bairros = st.multiselect('Selecione os bairros que desejar: ',bairros)

    filtro_bairro = data['bairro'].isin(select_bairros)

    container = st.container()
    df_filtrado = data.loc[filtro_quartos & filtro_suites & filtro_banheiros & filtro_vagas & filtro_metragem & filtro_preco & filtro_bairro]
    container.subheader(f':red[Dados Filtrados: {df_filtrado.shape[0]} imóveis.]')
    container.write(df_filtrado)
    graficos(df_filtrado)
    mapa(df_filtrado)
    return

def graficos(data):
    st.subheader(':red[Distribuição dos preços por quarto e Preços x Metragem:]')
    fig,axes = plt.subplots(2,1)
    plt.tight_layout()
    preco_piscina = sns.boxplot(x='quartos', y = 'preco', data=data, ax=axes[0])
    preco_privativo = sns.scatterplot(x = 'privativos', y='preco', hue = 'quartos', data = data, ax=axes[1])
    st.write(fig)


def mapa(data):
    fig = px.scatter_mapbox(data, lat="lat", lon="long", zoom=12, hover_name='titulo', 
                            hover_data=['preco', 'quartos', 'suites','banheiros','vagas'], 
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15,
                            color = 'preco', size = 'privativos')
    st.subheader(':red[Localização Geográfica dos Imóveis:]')
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

titulo()
load_data(df_final)
infos(df_final)
correlacao(df_final)
filtros(df_final)

