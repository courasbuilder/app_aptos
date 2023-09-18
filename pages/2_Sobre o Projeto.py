import streamlit as st

st.set_page_config(
    page_title='Sobre o Projeto de Predição de Preços'
)

st.title(':blue[Projeto de Predição de Preços de Apartamentos]')

st.image("https://images.unsplash.com/flagged/photo-1564767609342-620cb19b2357?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1373&q=80")

st.subheader(':blue[Sobre o Projeto:]')
'''
O presente projeto consiste em um webapp de precificação de apartamentos na cidade de Itajaí - 
Santa Catarina. Ressalto que o projeto foi feito, exclusivamente, para fins de estudos e 
desenvolvimento de competências de Ciências de Dados. Os valores e análises não devem ser entendidos
de forma rigorosa e nem utilizados para qualquer outro fim. 

O objetivo do projeto surge do interesse
de proprietários e possíveis compradores em determinar um valor justo a ser pago por um imóvel. Esse 
processo complexo abranje diversas variáveis, desejos, sonhos, conhecimentos técnicos e etc. Afim de
facilitar o processo de determinação de valor, surge a necessidade de técnicas que auxiliem esse cálculo. 
Dada a necessidade, optamos por desenvolver um modelo de Machine Learning que pudesse estimar o valor
de um imóvel baseado num dataset de imóveis 'semelhantes'. 

Limitamos o escopo do projeto 
para termos um primeiro modelo pronto. Novos avanços no projeto poderão vir no futuro, como outras cidades,
outras informações presentes no dataset e etc. Além de restringirmos a cidade, também restringimos o tipo
de imóvel, no momento, vamos trabalhar apenas com apartamentos. Sendo assim, o projeto teve que ser 
separados nas seguintes etapas:

'''
st.divider()
'''
Você poderá navegar pelas abas ao lado para acessar cada etapa do projeto. Qualquer crítica, sugestão ou 
dúvida é sempre bem-vinda. Você poderá entrar em contato comigo acessando as minhas redes na aba "Contato". 
Será um imenso prazer discurtir com outras pessoas sobre o projeto. 
'''
st.divider()
st.subheader(':blue[Etapa 1 - Webscrapping dos Dados]')
#st.image("https://images.unsplash.com/photo-1542903660-eedba2cda473?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80"
#         , width=500)
'''Utilizando a biblioteca Selenium, fizemos a extração dos dados dos imóveis a
venda no site da maior imobiliária de cidade de Itajaí - Santa Catarina. Limitados o escopo do projeto 
para termos um primeiro modelo pronto. Sendo assim, varremos o site e retiramos 
as informações necessárias para o projeto como: nome do anúncio, local do imóvel, preço e características 
gerais da infraestrutura do imóvel e do condomínio.
'''
st.subheader(':orange[Etapa 2 - Limpeza dos dados]')
# st.image("https://images.unsplash.com/photo-1627905646269-7f034dcc5738?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80",
#          width=500)
'''
Limpeza dos dados obtidos e formatação para os padrões necessários. 
Foram tratados os dados ausentes, a formatação de dados 'object' para numéricos, separação de algumas variáveis 
importantes e demais cuidados necessários com os dados.
'''
st.subheader(':red[Etapa 3 - Painel de Dados]')
# st.image("https://plus.unsplash.com/premium_photo-1661434270550-fc467725a2ed?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1471&q=80",
#          width=500)
'''
Uma breve análise exploratória e visual dos dados para a 
geração de insights importantes que podem ser úteis na formulação dos nosso futuro modelo de 
Machine Learning. Nessa etapa, possibilitamos também a personalização de filtros pelos usuário para 
encontrar imóveis com características que desejar.
'''
st.subheader(':violet[Etapa 4 - Modelo de Machine Learning]')
# st.image("https://images.unsplash.com/photo-1504639725590-34d0984388bd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1374&q=80",
#          width=500)

'''
Elaboração do modelo de Machine Learning com o inúito de prever o valor dos imóveis.
'''

st.subheader(':blue[Etapa 5 - WebApp de Previsão]')
# st.image("https://images.unsplash.com/photo-1560520653-9e0e4c89eb11?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1373&q=80",
#          width=500)

'''
Um Web App interativo para a inserção das características de um imóvel e o calculo de previsão
do valor de venda gerado por modelo Machine Learning.
'''

st.divider()
st.markdown('''Desenvolvido por: **Pedro Lourenço Mendes Júnior**''')
st.write("""<div style="width:100%;"><a href="https://www.linkedin.com/in/mendesjuniorpedro/" style="float:center"><img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="40px"></img></a>""" + """<a href="https://github.com/pedromendesjr" style="float:center"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="32px"></img></a></div>""", unsafe_allow_html=True)

