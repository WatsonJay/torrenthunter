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

class getlink():
    def get_link(self, conf, excel,timerun):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
        headers = {
            'Accept':'text/css,*/*;q=0.1',
            'Accept-Encoding':'gzip, deflate, sdch, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'User-Agent': user_agent,
        }
        urlstart = 'https://btso.pw/'
        myfile = xlwt.Workbook()
        wtable = myfile.add_sheet(u"信息", cell_overwrite_ok=True)
        wtable.write(0, 0, u"名字")
        wtable.write(0, 1, u"番号")
        wtable.write(0, 2, u"文件大小")
        wtable.write(0, 3, u"文件更新日期")
        wtable.write(0, 4, u"链接")
        wtable.write(0, 5, u"磁力链接")
        data = xlrd.open_workbook(excel)
        table = data.sheets()[0]
        nrows = table.nrows
        for j in range(nrows):
            try:
                cf = configparser.ConfigParser()
                cf.read(conf)
                p = cf.getint('keynum', 'endpart')
                if j == 0:
                    continue
                else:
                    serial = table.cell(j, 2).value
                    url = urlstart+'search/' + serial
                    # print url
                    r = requests.get(url, headers=headers, timeout=30)
                    html = r.text
                    # print html
                    soup = BeautifulSoup(html,'lxml')

                    for tag in soup.find_all('div', class_='row'):

                        for gg in tag.find_all(class_='col-sm-2 col-lg-1 hidden-xs text-right size'):
                            print(gg.string)
                            wtable.write(p, 0, table.cell(j, 0).value)
                            wtable.write(p, 1, table.cell(j, 2).value)
                            wtable.write(p, 2, gg.string)

                        for aa in tag.find_all(class_='col-sm-2 col-lg-2 hidden-xs text-right date'):
                            print(aa.string)
                            wtable.write(p, 3, aa.string)

                        for xx in tag.find_all(href=re.compile("magnet/detail/hash")):
                            print(xx.attrs['href'])
                            wtable.write(p, 4, xx.attrs['href'])
                            r1 = requests.get(xx.attrs['href'], headers=headers, timeout=30)
                            html1 = r1.text
                            # print html1
                            soup1 = BeautifulSoup(html1)
                            for tag1 in soup1.find_all('textarea', id='magnetLink'):
                                print(tag1.string)
                                wtable.write(p, 5, tag1.string)
                            p += 1
                    cf.set('keynum', 'endpart', str(p))
                    cf.write(open(conf, "w"))

            except:
                print(u"出现异常")

        filename = timerun + "link.xls"
        myfile.save(filename)
        print(u"自动保存%s的磁力链接备份" % timerun)

    def formatini(self):
        cf = configparser.ConfigParser()
        cf.read("liao.ini")
        cf.set('keynum', 'endpart', '1')
        cf.write(open("liao.ini", "w"))



