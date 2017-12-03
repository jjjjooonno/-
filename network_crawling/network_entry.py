from browsermobproxy import Server
import time
import urllib.request, json
from pandas import *
from selenium import webdriver
server = Server("/Users/joono/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

keyword = '혜화역'
webdriver_path = '/Users/joono/chromedriver'
email = 'jjjjooonno@gmail.com'


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=proxy.port))

dr = webdriver.Chrome(webdriver_path,chrome_options=chrome_options)
proxy.new_har("zigbang", options={'captureHeaders': True, 'captureContent': True})

dr.get("https://www.zigbang.com/")
time.sleep(1)
dr.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/button[1]').click()
time.sleep(3)
dr.find_element_by_name('username').send_keys(email)
time.sleep(1)
dr.find_element_by_xpath('/html/body/div[4]/div/form/div[2]/div[2]/button').click()
time.sleep(2)

# alert = dr.switch_to_alert()
time.sleep(1)
# alert.accept()

dr.find_element_by_id('room-textfield').send_keys(keyword)
time.sleep(5)
dr.find_element_by_xpath('//*[@id="search_btn"]').click()
time.sleep(10)
url_json_holder = []
for ent in proxy.har['log']['entries']:
    url_json = str(ent['request']['url'])
    if 'https://api.zigbang.com/v3/items?detail=true&item_ids=' in url_json:
        url_json_holder.append(url_json)
        break
rent = []
deposit = []
floor = []
floor_all = []
size = []
near_subways = []
elevator = []
movein_date = []
description = []
user = []
with urllib.request.urlopen(url_json_holder[0]) as url:
    data = json.loads(url.read().decode())
for i in data['items']:
    rent.append(i['item']['rent'])
    deposit.append(i['item']['deposit'])
    floor.append(i['item']['floor'])
    floor_all.append(i['item']['floor_all'])
    size.append(i['item']['size'])
    near_subways.append(i['item']['near_subways'])
    elevator.append(i['item']['elevator'])
    movein_date.append(i['item']['movein_date'])
    description.append(i['item']['title'])
    user.append(i['item']['agent_name'])
zigbangs = DataFrame({'월세':rent,'보증금/전세':deposit,'층':floor,'건물층수':floor_all,'평수':size,'가까운 역':near_subways,
                      '입주날짜':movein_date,'설명':description,'중개사':user})
zigbangs.to_csv('zigbang_113_{0}.csv'.format(keyword))