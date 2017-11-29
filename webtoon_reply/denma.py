#-*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
from datetime import datetime
import re
import time


dr = webdriver.Chrome('/Users/joono/Downloads/chromedriver')
comments=[]
episode = []
dr.implicitly_wait(1000)
for i in range(1,1045):
    dr.get('http://comic.naver.com/webtoon/detail.nhn?titleId=119874&no={0}&weekday=tue'.format(i))
    dr.switch_to.frame(dr.find_element_by_id("commentIframe"))
    drt = dr.page_source
    soup = BeautifulSoup(drt,'html.parser')
    comment = soup.find_all('span',attrs={'class':'u_cbox_contents'})
    for j in range(0,len(comment)):
        episode.append(i)
        comments.append(comment[j].text)

dt = DataFrame(comments,index=episode)
dt.to_csv('denma_comments_current.csv')