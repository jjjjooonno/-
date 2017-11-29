from selenium import webdriver
from pandas import *
from bs4 import BeautifulSoup
import time

dr = webdriver.Chrome('/Users/joono/chromedriver')
dr.get('https://www.basketball-reference.com/teams/BOS/2017.html')
for i in range(0,17):
    drt = dr.page_source
    soup = BeautifulSoup(drt,'html.parser')
    data = []
    table = soup.find('table', attrs={'id':'advanced'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    print(data)
    player = []
    mp = []
    per = []
    dws = []
    for j in data:
        player.append(j[0])
        mp.append(j[3])
        per.append(j[4])
        dws.append(j[17])
    dt = DataFrame({'PLAYER_NAME' : player,'MP':mp,'PER':per,'DWS':dws})
    dt.to_csv('Boston_1617.csv',index=None)
    time.sleep(5)