# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import urllib.request

class LIB():
    def keydate(self,word):
        date = {"searchPath": "全部","keyword":"1","dbName": "all"}
        date["keyword"] = word
        return date

    def posturl(self):
        url = 'http://ilib.gcu.edu.cn/WebOPAC/search_searchResultView'

        p = input('请输入你的检索信息：')
        date = self.keydate(p)
        response = requests.post(url=url,data=date).content.decode('utf-8')

        soup = BeautifulSoup(response, "html.parser")

        number = soup.find('b', class_="text-danger").text
        books = soup.find_all('a', class_="text-info")

        books_list = []
        for book in books:
            t = re.match( '^to.*?(\d+).*this', book["onclick"], re.S)
            books_list.append(t.group(1))

        book_url1 = "http://ilib.gcu.edu.cn/WebOPAC/searchDetail_detailView?primaryId="
        book_url2 = "&referLocation="

        book_allmessages1 = []
        book_allmessages2 = []
        i = 0
        for book in books_list:
            i += 1

            book_url = book_url1 + book + book_url2
            request = urllib.request.Request(url=book_url)
            book_response = urllib.request.urlopen(request)
            page_source = book_response.read().decode('utf-8')

            soup = BeautifulSoup(page_source, 'html.parser')
            messages = soup.find('div', class_="FLMessageText fl")
            book_message = messages.find_all('li')

            book_allmessages1.append(book_message)

            messages = soup.find('div', class_="FRMessageText fl")
            book_message = messages.find_all('li')

            book_allmessages2.append(book_message)

            if i == 5:
                break

        print("共有"+number+"信息，打印前五条信息")

        for t in range(0, i):
            print()
            print("第"+str(t+1)+"条信息")
            for message in book_allmessages1[t]:
                print(message.text)
            for message in book_allmessages2[t]:
                if message.text == "电子书信息":
                    break
                if message.text == "在线阅读":
                    break
                print(message.text)


s = LIB()
s.posturl()