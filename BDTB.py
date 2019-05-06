# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
from bs4 import BeautifulSoup


class BDTB:
    def __init__(self, baseurl, seelz):
        self.baseURL = baseurl
        self.seeLZ = seelz
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"
        self.headers = {'User-Agent': self.user_agent}

    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + str(pageNum)

            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            page_source = response.read().decode('utf-8')

            return page_source

        except urllib.error.URLError as e:
            print(u"连接百度贴吧失败，错误原因："+str(e.reason))
            return None

    def getPageItems(self, pageNum):
        page_source = self.getPage(pageNum)

        if not page_source:
            print("页面加载失败")
            return None

        soup = BeautifulSoup(page_source, 'lxml')

        links = soup.find_all('div', class_="d_post_content j_d_post_content")

        contents = []

        for link in links:
            contents.append(link.text)

        return contents

    def printOnePage(self, pageNum):
        contents = self.getPageItems(pageNum)
        self.writetofile(contents)
        for link in contents:
            print(link)

    def writetofile(self, contents):
        with open("data.txt", "w", encoding='utf-8') as f:
            f.writelines('\n'.join(contents))


    def start(self):
        while True:
            print(end="输入你想爬取的页数（输入0退出程序）：")
            pageNum = input()
            pageNum = int(pageNum)
            if pageNum == 0:
                print("程序退出！")
                break

            self.printOnePage(pageNum)


baseurl = "https://tieba.baidu.com/p/6112133978"
seelz = "?see_lz=1&pn="

spider = BDTB(baseurl, seelz)
spider.start()
