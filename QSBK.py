# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver

url1 = "https://www.qiushibaike.com/8hr/page/"
url2 = 1
url = url1 + str(url2)

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"}

request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
page_source = response.read().decode('utf-8')

soup = BeautifulSoup(page_source, 'lxml')

links = soup.find_all('a', class_="recmd-left word", target="_blank")

pageStories = []

for link in links:
    article_url1 = "https://www.qiushibaike.com"
    article_url2 = link['href']
    article_url = article_url1 + str(article_url2)

    driver = webdriver.Firefox()
    driver.get(article_url)

    user_name = driver.find_element_by_class_name("side-user-name")
    time = driver.find_element_by_class_name("stats-time")
    number = driver.find_element_by_class_name("number")
    content = driver.find_element_by_class_name("content")

    pageStories.append([user_name.text, time.text, number.text, content.text])
    driver.close()

for story in pageStories:
    print(u"作者：%s\t发布时间：%s\t赞：%s\n%s\n" % (story[0], story[1], story[2], story[3]))
