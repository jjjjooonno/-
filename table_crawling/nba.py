from selenium import webdriver
from pandas import *
from bs4 import BeautifulSoup
import time
teams = ['ATL','BOS','BRK','CHO','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','NYK','OKC','ORL','PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS','MIN','NOP']
dr = webdriver.Chrome('/Users/joono/chromedriver')

for i in teams:
    dr.get('https://www.basketball-reference.com/teams/{0}/2018.html'.format(i))
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
    dt = DataFrame({'PLAYER_NAME' : player,'MP':mp,'PER':per})
    dt.to_csv('{0}_1718.csv'.format(i),index=None)
    time.sleep(5)