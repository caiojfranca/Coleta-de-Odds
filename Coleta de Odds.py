#!/usr/bin/env python
# coding: utf-8

# # *CÓDIGO DE COLETA DE DADOS*

# In[2]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re


# In[3]:


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=2920x1080")


# In[74]:


driver = webdriver.Chrome()


# In[5]:


driver = webdriver.Chrome(options=chrome_options)


# ## *Função de Lista de Links para os Jogos*

# In[63]:


link_page = []
anos = [2021, 2020, 2019, 2018,
            2017, 2016, 2017, 2016,
            2015, 2014, 2013, 2012,
            2011, 2010]
for ano in anos:    
    for paginas in range(1, 9):         
        link_page.append(
            f'https://www.oddsportal.com/soccer/brazil/serie-a-{ano}/results/#/page/{paginas}/'
        )


# In[67]:


codigos = []
todos_links = []
def all_links():

    for link in link_page:
        driver.get(link)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html')
        jogos = soup.find_all('a', attrs={'href':re.compile('/soccer/brazil/serie-a-')})    
        links = list(map(lambda x : x.attrs['href'],jogos[25:]))      
        time.sleep(2)
        for lin in links:
            codigos.append(lin)
            
    for i in codigos: 
        todos_links.append(f'https://www.oddsportal.com{i}')


# ### Posibilidade de coletar mais odds
# O site deixa coletar mais Odds caso você esteja devidamente cadastrado

# In[219]:


#driver.get('https://www.oddsportal.com/login/')
#driver.find_element(By.ID,"login-username1").send_keys('caiojfranca')
#driver.find_element(By.ID,"login-password1").send_keys('caiocaio04')
#driver.find_element(By.XPATH,'//*[@id="user-header-oddsformat-expander"]').click()
#driver.find_element(By.XPATH,'//*[@id="user-header-oddsformat"]/li[1]/a').click()
#driver.find_element(By.XPATH,'//*[@id="col-content"]/div[2]/div/form/div[3]/button').click()


# ## *FUNÇÃO PARA A COLETA DAS ODDS DIRETAMENTE NOS JOGOS*

# In[80]:


odds = []
casa = []
falhas = []
def coleta(x):
        try:
            driver.get(x)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html')
            nome = soup.find_all('h1')
# INFORMAÇÕES SOBRE A DATA ESTÃO NA SEGUNDA POSIÇÃO        
            data = soup.find_all('p')[1]
            tabela = soup.find('tbody')
            odd = tabela.find_all('td')
# odd É A LISTA QUE CONTEM TODAS AS INFORMAÇÕES SOBRE AS ODDS
# NO CASO A PRIMEIRA INFORMAÇÃO É O NOME DA CASA DE APOSTA
            casas = odd[0::6]
            for i in casas:
                casa.append(i.text.replace("\xa0",""))
# AS SEGUNDAS INFORMAÇÃO SÃO SOBRE AS ODDS A FAVOR DO TIME DA CASA (WIN)
            Win_Home = odd[1::6]
# AS TERCEIRAS INFORMAÇÃO SÃO SOBRE AS ODDS DE EMPATE (DRAW)
            Draw = odd[2::6]
# AS QUATAS INFORMAÇÃO SÃO SOBRE AS ODDS A CONTRA DO TIME DA CASA (LOSE)
            Lose_Home = odd[3::6]
# DELETAR AS OUTRAS INFORMAÇÕES FICA A SEU CRITÉRIO
            del odd[4::6]
            del odd[4::5]
# DADOS SOBRE A DATA DOS JOGOS
            time = data.text.split(" ")
            week = time[0]
            day = time[1]
            month = time[2]
            year = time[4]
            hour = time[5]
# NOMES DOS TIMES
            team = nome[0].text.split("-")
            Home = team[0]
            Away = team[1]
# ORGANIZAR OS DADOS 
            for i in range(0, len(Draw)):
                odds.append({"Team Home":f"{Home}",
                         "Team Away":f"{Away}",
                         "Week day":f"{week}",
                         "Day":f"{day}",
                         "Month":f"{month}",
                         "Year":f"{year}",
                         "Hour":f"{hour}",
                         "Casa":f'{casa[i]}',
                         "Win Home":f"{Win_Home[i].text}",
                         "Draw":f"{Draw[i].text}",
                         "Lose Home":f"{Lose_Home[i].text}"
                })
            print(f"{contador} /Sucesso/ Jogo: {Home}x{Away}, do ano de {year}")
        
        except:
            falhas.append(contador-1)
            print(f"Falha no jogo Número: {contador-1} ")


# ## *RODAR O CÓDIGO*

# In[81]:


driver.get('https://www.oddsportal.com/login/')
driver.find_element(By.XPATH,'//*[@id="user-header-oddsformat-expander"]').click()
driver.find_element(By.XPATH,'//*[@id="user-header-oddsformat"]/li[1]/a').click()
time.sleep(4)
driver.find_element(By.ID,"login-username1").send_keys('LOGIN')
driver.find_element(By.ID,"login-password1").send_keys('SENHA')
driver.find_element(By.XPATH,'//*[@id="col-content"]/div[2]/div/form/div[3]/button').click()


# In[ ]:


all_links()


# In[ ]:


contador = 0
for i in todos_links:
    contador += 1
    coleta(i)

