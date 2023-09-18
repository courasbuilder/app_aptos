import pandas as pd
import streamlit as st
import joblib

st.set_page_config(
    page_title='App v1.1 - Predição de preços de imóveis'
)


# Importando os dados necessários:
bairros = joblib.load('bairros.pkl')
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
encoder = joblib.load('encoder.pkl')


# Criando dataframe que vai receber os dados
apto = pd.DataFrame([[1,0,1,1,80,None,0,0,0,0,0]], columns=['quartos', 'suites', 'banheiros', 'vagas', 'privativos', 'bairro',
        'piscina', 'gas_central', 'elevador', 'salao', 'academia'])

# Título
st.title('Web App 1.0 - Predição de valor de apartamentos')

st.write('Para conhecer mais sobre o projeto, convido você a navegar pelo menu ao lado. Você encontrará os detalhes de cada etapa de construção desse projeto.')

st.subheader('Insira as característica do apartamento:')

# Painel de inserção de dados
quartos = st.selectbox('Quantidade de quartos:', (1,2,3,4,5,6))
suites = st.selectbox('Quantidade de suítes:',(0,1,2,3,4,5,6))
banheiros = st.selectbox('Quantidade de banheiros:',(1,2,3,4,5,6))
vagas = st.selectbox('Quantidade de vagas de garagem:',(0,1,2,3,4,5))
privativos = st.number_input('Quantidade de metros quadrados:', min_value=30, max_value=500)
bairro = st.selectbox('Insira o bairro:', bairros)
st.write('Selecione as características presentes no condomínio:')

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    #Checkbox do item definido previamente como false/não
    piscina = st.checkbox('Piscina')
    tem_piscina = 'Não'
    # Caso positivo, alteração da coluna do dataframe
    if piscina:
        apto['piscina'] = 1
        tem_piscina = 'Sim'
with col2:
    gas_central = st.checkbox('Gás Central')
    tem_gas = 'Não'
    if gas_central:
        apto['gas_central'] = 1 
        tem_gas = 'Sim'
with col3:
    elevador = st.checkbox('Elevador')
    tem_elevador = 'Não'
    if elevador:
        apto['elevador'] = 1
        tem_elevador = 'Sim'
with col4:
    salao = st.checkbox('Salão de Festas')
    tem_salao = 'Não'
    if salao:
        apto['salao'] = 1
        tem_salao = 'Sim'
with col5:
    academia = st.checkbox('Academia')
    tem_academia = 'Não'
    if academia: 
        apto['academia'] = 1
        tem_academia = 'Sim'  
# Botão para gerar o calculo da previsão
click = st.button('Calcular preço do imóvel:')
if click:
    # Passando as variáveis inseridas
    apto['quartos'] = quartos
    apto['suites'] = suites
    apto['vagas'] = vagas
    apto['banheiros'] = banheiros
    apto['privativos'] = privativos
    apto['bairro'] = bairro
    # Aplicação de Encoder e Escaler
    apto_encoded = encoder.transform(apto[['bairro']])
    apto_encoded = apto_encoded.join(apto.drop('bairro', axis = 1))
    apto_scaled = scaler.transform(apto_encoded)
    # Predict dos dados
    preco = model.predict(apto_scaled)
    # Resultado do modelo e dados do apartamento.
    st.subheader('Predição de valor do imóvel:  :blue[**R$ {:,.2f}**]'.format(preco[0]).replace('.', '|').replace(',', '.').replace('|', ','))
    st.info(f'Informações do apartamento:  \n Quartos: {quartos}  \n Suítes: {suites}  \n Banheiros: {banheiros}  \n Vagas: {vagas}  \n Metragem: {privativos} m2  \n Bairro: {bairro}  \n Piscina: {tem_piscina}  \n Gás Central: {tem_gas}  \n Elevador: {tem_elevador}  \n Salão de Festas: {tem_salao}  \n Academia: {tem_academia}')

st.divider()
st.markdown('''Desenvolvido por: **Pedro Lourenço Mendes Júnior**''')
st.write("""<div style="width:100%;"><a href="https://www.linkedin.com/in/mendesjuniorpedro/" style="float:center"><img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="40px"></img></a>""" + """<a href="https://github.com/pedromendesjr" style="float:center"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="32px"></img></a></div>""", unsafe_allow_html=True)

