# coding=utf8
import requests
import re
import xlrd
import xlwt
import time
try:  # python3
    import configparser
except:  # python2
    import ConfigParser as configparser
import threading
from bs4 import BeautifulSoup
from free_proxyIP import  proxyip

class getlink():
    def get_link(self, conf, excel,timerun,i):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'User-Agent': user_agent,
        }
        urlstart = 'https://btso.pw/'
        myfile = xlwt.Workbook()
        wtable = myfile.add_sheet(u"信息", cell_overwrite_ok=True)
        wtable.write(0, 0, u"名字")
        wtable.write(0, 1, u"番号")
        wtable.write(0, 2, u"文件名")
        wtable.write(0, 3, u"文件大小")
        wtable.write(0, 4, u"文件更新日期")
        wtable.write(0, 5, u"链接")
        wtable.write(0, 6, u"磁力链接")
        data = xlrd.open_workbook(excel)
        table = data.sheets()[0]
        nrows = table.nrows
        cf = configparser.ConfigParser()
        cf.read(conf)
        sp = cf.getint('keynum', 'startpart')
        ep = cf.getint('keynum', 'endpart')+1
        np = 1
        for j in range(sp,ep):
            try:
                if j == 0:
                    continue
                else:
                    serial = table.cell(j, 2).value
                    url = urlstart+'search/' + serial
                    # print url
                    IP = {'http': proxyip()}
                    r = requests.get(url, headers=headers, proxies=IP, timeout=30)
                    html = r.text
                    # print html
                    soup = BeautifulSoup(html,'lxml')

                    for tag in soup.find_all('div', class_='row'):

                        for gg in tag.find_all(class_='col-sm-2 col-lg-1 hidden-xs text-right size'):
                            print(gg.string)
                            wtable.write(np, 0, table.cell(j, 0).value)
                            wtable.write(np, 1, table.cell(j, 2).value)
                            wtable.write(np, 3, gg.string)

                        for aa in tag.find_all(class_='col-sm-2 col-lg-2 hidden-xs text-right date'):
                            print(aa.string)
                            wtable.write(np, 4, aa.string)

                        for xx in tag.find_all(href=re.compile("https://btso.pw/magnet/detail/hash")):
                            print(xx.attrs['href'])
                            wtable.write(np, 2, xx.attrs['title'])
                            wtable.write(np, 5, xx.attrs['href'])
                            r1 = requests.get(xx.attrs['href'], headers=headers, timeout=30)
                            html1 = r1.text
                            # print html1
                            soup1 = BeautifulSoup(html1)
                            for tag1 in soup1.find_all('textarea', id='magnetLink'):
                                print(tag1.string)
                                wtable.write(np, 6, tag1.string)
                            np += 1
                    cf.set('keynum', 'nowpart', str(np))
                    cf.write(open(conf, "w"))

            except:
                print(u"出现异常")

        filename = timerun + "link" + str(i) + ".xls"
        myfile.save(filename)
        print(u"自动保存%s的磁力链接备份" % timerun)

    def formatini(self):
        cf = configparser.ConfigParser()
        cf.read("liao.ini")
        p = int(cf.getint('starnum', 'startotal'))
        cf1 = configparser.ConfigParser()
        for i in range(1,6):
            cf1.read("link"+str(i)+".ini")
            cf1.set('keynum', 'startpart', str(int(p/5)*(i-1)+1))
            cf1.set('keynum', 'endpart', str(int(p/5)*(i)))
            cf1.set('keynum', 'nowpart', str(int(p / 5) * (i - 1) + 1))
            cf1.write(open("link"+str(i)+".ini", "w"))



