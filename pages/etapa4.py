import streamlit as st
import joblib

st.set_page_config(
    page_title='Etapa 4: Modelo de Machine Learning'
)

st.header(':violet[Etapa 4: Modelo de Machine Learning]')
st.image('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjkyNzZ6OWltOWh4dWhycmhmdW84Zmphc2V0bjJha21qMzU5bG5pciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/F14BrsUdpzcc1wsSbV/giphy.gif', width=300)

'''
Quarta e última etapa do nosso projeto. Depois de obter os dados, limpar, organizar e visualizar, chegou o momento do aprendizado de máquina. É nessa etapa que vamos usar os nossos dados para elaborar um mecanismo de predição de preços dos imóveis. 

Nessa etapa teremos alguns pontos cruciais, como:
* 4.1. Separação dos dados que serão usados pelo modelo.
* 4.2. Separação dos dados de treinamento e de teste.
* 4.3. Aplicação de encoder e scalers.
* 4.4. Encontrar o melhor modelo de Machine Learning.
* 4.5. Configurar o modelo.
* 4.6. Exportar os arquivos necessários.

O objetivo dessa etapa é que, ao final, tenhamos um modelo de machine learning capaz de predizer os valores dos imóveis e 
gerar os arquivos necessários para que possamos utilizar num webapp interativo. O usuário será capaz de colocar
as informações de um apartamento fictício e o modelo irá predizer o valor com base nesses dados.

Bora começar! 
'''

st.subheader(':violet[4.1. Separação dos dados que serão usados pelo modelo.]')

'''
Primeiramente, vamos importar as nossas bibliotecas e o nosso DataFrame pós-limpeza.
'''
code1 = '''
# Importando Bibliotecas:
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
import category_encoders as ce
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import GridSearchCV

# Importando o dataframe:
df = pd.read_csv('df_final.csv')
'''
st.code(code1, language='python')

'''
Até aqui, nenhuma novidade. Tem uma série de bibliotecas novas, mas nada muito diferente do que a gente está acostumado a 
ver em projetos de Machine Learning. Agora é importante perceber que alguns colunas não serão usadas pelo modelo de Machine Learning. 
A variável título com o título do anúncio não é interessante, assim como o link para a página do anúncio. 

Outras duas variáveis que não utilizaremos é a latitude e longitude, esse é um erro bastante comum, praticado por 
iniciantes. As coordenadas geográficas não são boas de se utilizar, uma alternativa seria utilizar as coordenadas 
para calcular a distância até a praia, ou a distância  para outros pontos importantes da cidade. No momento não 
vamos utilizar esse abordagem, novas atualização virão no futuro e essa é uma melhoria possível. 

Além disso, não vamos utilizar a variável rua e cidade. A variável rua é uma variável categórica com muitas classes e o 
nosso dataset é pequeno. Serão pouquíssimos imóveis numa mesma rua e etc. Além disso, já temos a variável bairro que irá 
permanecer no dataset e irá nos fornecer essa característica de localização. Esperamos que o bairro seja suficiente. A variável
cidade é inútil, já que temos imóveis apenas na cidade de Itajaí após a limpeza. 
'''
code2 = '''
# Excluindo colunas desnecessárias para o modelo:
df.drop(['Unnamed: 0','titulo','link','lat','long','numero_rua','cidade'], axis = 1, inplace=True)
'''
st.code(code2, language='python')
'''Dataset pronto, partiu separação dos dados.'''

st.subheader(':violet[4.2. Separação dos dados de treinamento e de teste. ]')

'''
Essa é uma etapa crucial para fazer a predição e, principalmente, avaliar o modelo. Precisamos separar uma parte do nosso
dataset para que seja visto só no final pelo modelo. É com a parte de teste que o modelo irá passar pelo desafio e prever o preço. 
'''
code3 = '''
# Separando os dados em treino - teste:
X_train, X_test, y_train, y_test = train_test_split(df.drop(['preco'], axis = 1), df['preco'], test_size = 0.30)

print(f'O dataset de treino ficou com dimensões {X_train.shape} enquanto o nosso target de treino ficou {y_train.shape}.')
print(f'O dataset de test ficou com dimensões {X_test.shape} enquanto o nosso target de teste ficou {y_test.shape}.')
'''
st.code(code3, language='python')
'''
Com isso, ficamos com a seguinte situação:

O dataset de treino ficou com dimensões (189, 11) enquanto o nosso target de treino ficou (189,).

O dataset de test ficou com dimensões (81, 11) enquanto o nosso target de teste ficou (81,).
'''
st.subheader(':violet[4.3. Aplicação de encoder e scalers]')

'''
Nessa etapa, vamos utilizar os Encoders e Scaler, duas técnicas distintas de pré-processamento de dados. 

O encoder é uma técnica para converter dados de um formato para outro, comumente usado para transformar 
dados categóricos em uma representação numérica. É frequentemente utilizado quando se tem variáveis categóricas
(por exemplo, cores, tipos de produtos, bairros, categorias) que precisam ser transformadas em números antes
de serem usadas em algoritmos de aprendizado de máquina. Isso permite que o algoritmo compreenda e trabalhe com 
esses dados de forma mais eficaz. 

O Scaler (ou normalizador) é uma técnica usada para ajustar a escala dos dados numéricos para um intervalo específico ou 
para torná-los comparáveis entre si. É frequentemente usado para garantir que todas as características (features) tenham
a mesma importância durante o treinamento do modelo. Isso é especialmente importante algorítmos
sensíveis à escala, como regressão linear, k-means e entre outros. Existem diversas técnicas, incluindo o MinMax Scaling e
Standard Scaler.
'''
code4 = '''
# Aplicando Target Encoder na variável 'bairro':
target_encoder = ce.TargetEncoder()
X_train_encoded = target_encoder.fit_transform(X_train[['bairro']], y_train)
X_train_encoded = X_train_encoded.join(X_train.drop('bairro', axis = 1))

# Aplicando MinMaxScaler nas variáveis numéricas:

scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train_encoded)

# Aplicando Target Encoder no Test:
X_test_encoded = target_encoder.transform(X_test[['bairro']])
X_test_encoded = X_test_encoded.join(X_test.drop('bairro', axis = 1))

# Aplicando MinMaxScaler no Test:
X_test_scaled = scaler.transform(X_test_encoded)
'''
st.code(code4, language='python')
'''
Após essa etapa, agora temos dois novos dataset, o *X_train_encoded* e o X_test_encoded*, derivados dos dataset originais, mas 
agora com a variável categórica *bairros* já transformada em numérica e com as variáveis normalizadas.
'''
st.subheader(':violet[4.4. Encontrar o melhor modelos de Machine Learning.]')
st.image('https://media.giphy.com/media/5zoxhCaYbdVHoJkmpf/giphy.gif', width=300)
'''
Nesta etapa vamos testar vários modelos de Machine Learning diferentes e obter as métricas de previsão dos preços com os dados
de teste. Para isso, vamos utilizar as seguintes métricas: :orange[MAE (Mean Absolute Error), MAPE (Mean Absolute Percentage Error), MSE
(Mean Squared Error), R2-Squared]. Para cada modelo, vamos treinar, testar e medir o desempenho. Os resultados serão agrupados numa tabela.\
'''

code5 = '''
# Função para testar vários modelos:
def modelos_and_metricas(X_train, X_test, y_train, y_test):
    # Modelos:
    modelos = {
        'Regressão Linear Múltipla':LinearRegression(),
        'Regressão Ridge': Ridge(),
        'Regressão Lasso': Lasso(),
        'SVR':SVR(),
        'Random Forest Regressor': RandomForestRegressor(),
        'K-Nearest Neighbors': KNeighborsRegressor(),
        'XGBoost Regressor': XGBRegressor()
    }
    resultados = []
    # Resultados de cada modelo:
    for nome_modelo, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        mae = mean_absolute_error(y_test,y_pred)
        mse = mean_squared_error(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        r2 = r2_score(y_test,y_pred)

        resultado = {
            'Modelo': nome_modelo,
            'MAE': mae,
            'MSE': mse,
            'MAPE': mape,
            'R-squared':r2
        }
        # Salvando os resultados
        resultados.append(resultado)
    resultados_df = pd.DataFrame(resultados)
    return resultados_df

resultados = modelos_and_metricas(X_train_scaled, X_test_scaled, y_train, y_test)
'''
st.code(code5, language='python')
'''
* :violet[Resultados:] Abaixo podemos ver os resultados dos diferentes algorítmos para
as principais métricas.
'''
resultados = joblib.load(open('files/resultados_tabela.pkl', 'rb'))
st.table(resultados)
'''
Pelos resultados, podemos perceber que o melhor desempenho foi o :violet[Random Forest Regressor],
um modelo ensemble de árvore, bastante difundido no universo de Machine Learning. 

O modelo obteve um *MAE (Mean Absolute Error) de 164 mil*, ou seja, o modelo está 
errando o preço dos imóveis de teste em 164 mil em média. É claro que alguns ele erra por
valores menos e outros ultrapassada esse valor de MAE. Outra métrica interessante é o *MAPE (
Mean Absolute Percentage Error) de 0.15*, isso significa que, em médio, o modelo erra por 15% 
no valor dos imóveis. É difícil fazer uma avaliação do modelo em si, a quantidade de dados é 
pequena, sejam imóveis quanto features. Mas é interessante um erro de apenas 15%. E o *R-quadrado 
de 0,84* indica que o modelo consegue 'explicar' 84% dos valores dos imóveis. 

Um outro modelo que teve métricas próximas foi o *XGBoost Regressor* que é baseado em árvore, 
assim como o Random Forest. Trata-se de um modelo ensemble também. 
'''
st.subheader(':violet[4.5. Configurar modelo final.]')
'''
Como o *RandomForestRegressor* se mostrou o melhor, neste caso. Optamos por faz uma validação 
cruzada para melhor alguns hiperparâmetros do modelo. O resultado, após a tunagem dos hiperparâmetros, 
não mostrou muito diferença em relação ao modelo baseline. :violet[*Aqui requer uma investigação mais detalhada, 
o que faramos nas próximas atualizações do projeto.*] 
'''

code6 = '''
# Instanciando o melhor modelo:
rf = RandomForestRegressor()
# Hiperparâmetros para testar:
param = {'max_depth':[4,5,6,7], 'n_estimators':[20,40,60,80,100]}
# Cross-Validation
cv_rf = GridSearchCV(rf, param_grid = param, scoring = 'neg_mean_absolute_error', n_jobs = None,
                       refit = True, cv = 4, verbose = 1, error_score = np.nan,
                       return_train_score = True)

# Treinando a Validação Cruzada:
cv_rf.fit(X_train_scaled,y_train)

# Buscando os melhores parâmetros da Validação Cruzada:
cv_rf_results = pd.DataFrame(cv_rf.cv_results_)

# Utilizando o modelo tunado:
rf_final = RandomForestRegressor(max_depth = 7, n_estimators = 100)
rf_final.fit(X_train_scaled, y_train)
y_pred = rf_final.predict(X_test_scaled)

# Obtendo as métricas da aplicação do modelo:
mae = mean_absolute_error(y_test,y_pred)
mse = mean_squared_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)
r2 = r2_score(y_test,y_pred)

'''
st.code(code6, language='python')
'''
Com isso, temos o nosso modelo de *Random Forest Regressor* que irá ser utilizado no WebApp da próxima etapa.
'''

st.subheader(':violet[4.6. Exportar os arquivos necessários:]')
'''
Por fim, precisamos exportar alguns arquivos necessários para a construção do nosso modelo no WebApp. 
Utilizando a biblioteca *JobLib*, podemos exportar os arquivos no formato .pkl e depois importar no modelo.
'''
code7 = '''
# Lista de Bairros:

bairros = df['bairro'].unique().tolist()

# Utilizando o Joblib para exportar o modelo:

joblib.dump(rf_final,'model.pkl')
joblib.dump(target_encoder,'encoder.pkl')
joblib.dump(scaler,'scaler.pkl')
joblib.dump(bairros,'bairros.pkl')
joblib.dump(resultados,'resultados_tabela.pkl')
'''
st.code(code7, language='python')

st.subheader(':violet[Conclusão]')
st.image('https://media.giphy.com/media/UtEUhkfriklonVdweC/giphy.gif', width=300)
'''
Com isso, finalizamos a nossa Etapa 4 do projeto, assim como a documentação dele. A próxima etapa consiste no Web App 
de predição de preços dos imóveis utilizando o modelo desenvolvivo nessa etapa. A etapa final do projeto é bastante simples, 
fizemos alguns inputs para o usuários fornecer as informações do imóvel. Mais precisamente, fizemos um input para cada feature 
do nosso modelo. O usuário fornece as informações e depois clica num botão para reproduzir o código no novo conjunto de dados fornecidos.
Esse processo é semelhante ao momento onde usamos o modelo no conjunto de teste, a diferença é que não temos o valor real do imóvel 
para comparar com o valor predito. 

Primeiramente, gostaria de agradecer a leitura e a paciência de quem chegou até o final. Esse projeto é dos primeiros da minha carreira 
de Cientista de Dados. Alguns erros foram cometidos, a maioria por falta de experiência e conhecimento. Existe um imensidão de técnicas 
para aprender no universo de dados e eu estou pronto e motivado para isso. 
'''

st.divider()
st.markdown('''Desenvolvido por: **Pedro Lourenço Mendes Júnior**''')
st.write("""<div style="width:100%;"><a href="https://www.linkedin.com/in/mendesjuniorpedro/" style="float:center"><img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="40px"></img></a>""" + """<a href="https://github.com/pedromendesjr" style="float:center"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="32px"></img></a></div>""", unsafe_allow_html=True)