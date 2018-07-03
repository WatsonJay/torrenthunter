# coding=utf8
import requests
import re
import os
import xlrd
import xlwt
import time
try:  # python3
    import configparser
except:  # python2
    import ConfigParser as configparser
from bs4 import BeautifulSoup


class getserial():

    def __init__(self,timerun):
        self.timerun = timerun
        self.myfile = xlwt.Workbook()
        self.wtable = self.myfile.add_sheet(u"信息", cell_overwrite_ok=True)
        self.wtable.write(0, 0, u"名字")
        self.wtable.write(0, 1, u"链接")
        self.wtable.write(0, 2, u"番号")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.headers = {
            'User-Agent': user_agent,
        }

    def get_serial(self):
        data = xlrd.open_workbook(self.timerun+'url.xls')
        table = data.sheets()[0]
        try:
            cf = configparser.ConfigParser()
            cf.read("liao.ini")
            nrows=table.nrows
            for j in range(nrows):
                p = cf.getint('starnum', 'startotal')
                if j == 0:
                    continue
                else:
                    url = table.cell(j, 1).value

                    r = requests.get(url+'/page/3', headers=self.headers)
                    html = r.text
                    soup = BeautifulSoup(html, 'lxml')
                    i = 0

                    for tag in soup.find_all('date'):
                        if i % 2 == 0:
                            # print tag.string
                            self.wtable.write(p, 2, tag.string)
                            self.wtable.write(p, 0, table.cell(j, 0).value)
                            self.wtable.write(p, 1, table.cell(j, 1).value)
                            p += 1
                        i += 1
                    print(table.cell(j, 0).value + '读取结束 ')
                    cf.set('starnum', 'startotal', str(p))
                    cf.write(open("liao.ini", "w"))

        except:
            print(u"出现异常")

    def saveserial(self):
        filename = self.timerun + "serial.xls"
        self.myfile.save(filename)
        print(u"完成%s的番号读取" % self.timerun)

    def formatini(self):
        cf = configparser.ConfigParser()
        cf.read("liao.ini")
        cf.set('starnum', 'startotal', '1')
        cf.write(open("liao.ini", "w"))

    def threadstarted(self):
        self.get_serial()
        self.saveserial()
