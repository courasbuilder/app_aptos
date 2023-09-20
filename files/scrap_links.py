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

# Selecionando o local onde irá ser feito o PAGE_DOWN:
box_page = driver.find_element(By.CSS_SELECTOR,'.clb-search-result-property')
i = 0

while i < 70:
    # PAGE_DOWN aguardando 1 segundo:
    box_page.send_keys(Keys.PAGE_DOWN)
    box_page.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    i = i + 1
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

df_links = pd.DataFrame({
    'links':links
})

print(df_links)

df_links.to_csv('df_links.csv')


    


