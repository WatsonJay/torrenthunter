# coding=utf8
import requests
import re
import xlwt
from bs4 import BeautifulSoup
from free_proxyIP import proxyip
# 新建excel表格用于存储数据
class geturl():

    def __init__(self, page):
        self.page = int(page)
        self.myfile = xlwt.Workbook()
        self.table = self.myfile.add_sheet(u"信息", cell_overwrite_ok=True)
        self.table.write(0, 0, u"名字")
        self.table.write(0, 1, u"链接")
        self.urlstart = 'https://javmoo.com/cn'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.headers = {
            'User-Agent': user_agent,
        }


    def get_url(self):
        rows = self.page * 50
        for p in range(1, self.page + 1):
            url = self.urlstart+'/actresses/page/' + str(p)
            IP ={'http' : proxyip()}
            r = requests.get(url, headers=self.headers, proxies=IP, timeout=3)
            html = r.text

            soup = BeautifulSoup(html,'lxml')

            i = (p - 1) * 50 + 1
            for tag in soup.find_all(href=re.compile(self.urlstart+"/star")):
                self.table.write(i, 1, tag.attrs['href'])
                i += 1

            j = (p - 1) * 50 + 1
            for tag in soup.find_all(class_='photo-info'):
                for gg in tag.find_all('span'):
                    # print gg.string
                    self.table.write(j, 0, gg.string)
                    j += 1
            print(u"完成读取第%s页信息" % p)

    def savestar(self,timerun):
        filename = timerun+"url.xls"
        self.myfile.save(filename)
        print(u"完成%s的url读取" % timerun)


