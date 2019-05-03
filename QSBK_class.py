# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver


class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = "https://www.qiushibaike.com/8hr/page/" + str(pageIndex)

            request = urllib.request.Request(url=url, headers=self.headers)
            response = urllib.request.urlopen(request)
            page_source = response.read().decode('utf-8')

            return page_source

        except urllib.error.URLError as e:
            print("连接糗事百科失败,错误原因"+e.reason)
            return None

    def getPageItems(self,pageIndex):
        page_source = self.getPage(pageIndex)
        if not page_source:
            print("页面加载失败")
            return None

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

        return pageStories

    def loadPage(self):
        if self.enable == True:
            pageStories = self.getPageItems(self.pageIndex)
            if pageStories:
                self.stories = pageStories
                self.pageIndex += 1

    def getOnestory(self, pageStories):
        print("第%d页" % (self.pageIndex-1))
        for story in pageStories:
            print(u"作者：%s\t发布时间：%s\t赞：%s\n%s\n" % (story[0], story[1], story[2], story[3]))

        flag = input()
        if flag == "Q":
            self.enable = False
            return

    def start(self):
        print(u"正在读取糗事百科,按回车查看新段子，Q退出")

        self.enable = True

        while self.enable:
            self.loadPage()
            if len(self.stories) > 0:
                self.getOnestory(self.stories)


spider = QSBK()
spider.start()
