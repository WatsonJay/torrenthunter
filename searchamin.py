# coding=utf8
import time
try:  # python3
    import configparser
except:  # python2
    import ConfigParser as configparser
import threading
from search import geturl
from searchkey import getserial
from searchtorrent import getlink

class torrenthunter():
    def __init__(self):
        print('[INFO]:Japanese star（女优）torrent downloader...')
        print('[Version]: V1.0')
        print('[Author]: 花二爷')
    #创建函数run():外部调用运行
    def run(self):
        # 输入页数(爬取几页的女优数据)
        timerun =str(time.strftime('%Y%m%d%H%M%S', time.localtime()))
        star_num = input('Enter the page(per page 50 star):')
        try:
            #验证ID是否为数字
            int(star_num)
        #错误输出
        except:
            print('[ERROR]:ID error...')
            return
        if int(star_num)>10:
            print('too large!')
        else:
            # test = geturl(star_num)
            # test.get_url()
            # test.savestar(timerun)
            # serial = getserial(timerun)
            # serial.formatini()
            # serial.threadstarted()
            link = getlink()
            link.formatini()
            link.get_link('liao.ini','20180627204823'+'serial.xls',timerun)
            print(u"完成所有进程")