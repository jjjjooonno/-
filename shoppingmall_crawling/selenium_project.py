#-*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
from datetime import datetime
import re

dr = webdriver.Chrome('/Users/joono/chromedriver')

dr.implicitly_wait(3)

dr.get('http://store.musinsa.com/app/contents/onsale?d_cat_cd=&brand=&page_kind=onsale&list_kind=small&sort=pop&page=1&'
       'display_cnt=120&free_dlv=&ex_soldout=&sale_goods=&sale_fr_rate=&sale_to_rate=&sex=&sale_yn=&sale_dt_yn=&popup=')
html = dr.page_source
soup = BeautifulSoup(html,'html.parser')

sale_pdt = soup.find_all('p',attrs={'class':'list_info'})
sale_prc = soup.find_all('p',attrs={'class':'price'})
sale_pct = soup.find_all('div',attrs={'class':'used_icon_box'})
pdt = []
prc = []
pct = []
for i in range(0,len(sale_pdt)):
    pdt.append(sale_pdt[i].find('a').text)
    prc.append(re.sub('[^0-9]','',sale_prc[i].text[10:]))
    pct.append(sale_pct[i].find('div').text[4:].split())
data = {'상품명': pdt,
        '가격': prc,
        '할인율': pct}
dt = DataFrame(data)
# print(sale_pct[0])
# print(sale_pdt[0])
# print(sale_prc[0])
print(dt.head())

dt.to_csv('무신사_할인상품_{0}.csv'.format(datetime.today().strftime('%Y%m%d')),encoding='utf-8',index=False)
dr.quit()

ndt = pd.read_csv('무신사_할인상품_{0}.csv'.format(datetime.today().strftime('%Y%m%d')), encoding = 'utf-8')
print(ndt.head())