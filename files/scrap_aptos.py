import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Abrir navegador Firefox:
driver = webdriver.Firefox()

# Dataset com os links dos imóveis:
df_links = pd.read_csv('df_links.csv')

links = df_links['links']

#Criando conjunto de dados:
colunas = ['titulo','endereco','preco','quartos','suites','banheiros','vagas','privativos','total','infra','coordenadas','link']
aptos = pd.DataFrame(columns=colunas)
index = 0

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

    # # Informações do imóvel:
    imovel = driver.find_element(By.CLASS_NAME,'property-amenities')
    try: # Buscar quantidade de quartos:
        aptos.loc[index].quartos = imovel.find_element(By.ID,'amenity-dormitorios').find_element(By.TAG_NAME,'span').text
    except:
        pass
    try: # Buscar quantidade de suítes:
        aptos.loc[index].suites = imovel.find_element(By.ID,'amenity-suites').find_element(By.TAG_NAME,'span').text
    except:
        pass
    try: # Buscar quantidade de banheiros:
        aptos.loc[index].banheiros = imovel.find_element(By.ID,'amenity-banheiros').find_element(By.TAG_NAME,'span').text
    except:
        pass
    try: # Buscar quantidade de vagas de garagem:
        aptos.loc[index].vagas = imovel.find_element(By.ID,'amenity-vagas').find_element(By.TAG_NAME,'span').text
    except:
        pass
    try: # Buscar a metragem da área privativa:
        aptos.loc[index].privativos = imovel.find_element(By.ID,'amenity-area-privativa').find_element(By.TAG_NAME,'span').text
    except:
        pass
    try: # Buscar a metragem total do imóvel
        aptos.loc[index].total = imovel.find_element(By.ID,'amenity-area-total').find_element(By.TAG_NAME,'span').text
    except:
        pass
    
    # Características do imóvel (Infraestrutura do condomínio/imóvel):
    aptos.loc[index].infra = []
    try:
        caracteristicas = driver.find_element(By.CSS_SELECTOR,'html body.page-template.page-template-page-imovel.page-template-page-imovel-php.page.page-id-6 main#page div.pg-imovel div#form-start-floating.contact-form-rail section#clb-descricao.printable div.container div.row div.col-xs-12.col-sm-12.col-md-7.col-lg-8.clb-infra-imo')
        infras = caracteristicas.find_elements(By.TAG_NAME,'p')
        for p in infras:
            aptos.loc[index].infra.append(p.text)
    except:
        pass

    # Localização do imóvel (Link GoogleMaps):
    frame = driver.find_element(By.ID,'form-start-floating').find_element(By.TAG_NAME,'iframe')
    coordenadas = frame.get_attribute('data-src')
    aptos.loc[index].coordenadas = coordenadas

    # Acompanhar execução:
    print(f'Apartamento: {index}.')
    index += 1

# Fechar navegador:
driver.quit()

# Salvar o dataset:
aptos.to_csv('aptos.csv')

