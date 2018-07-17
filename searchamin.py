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
from hebin import hebinxls
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
            test = geturl(star_num)
            test.get_url()
            test.savestar(timerun)
            serial = getserial(timerun)
            serial.formatini()
            serial.threadstarted()
            link = getlink()
            link.formatini()
            # link.get_link('liao.ini', '20180717091430' + 'serial.xls', timerun)
            threads = []
            t1 = threading.Thread(target=link.get_link, args=('link1.ini', '20180717091430' + 'serial.xls', timerun,1))
            threads.append(t1)
            t2 = threading.Thread(target=link.get_link, args=('link2.ini', '20180717091430' + 'serial.xls', timerun,2))
            threads.append(t2)
            t3 = threading.Thread(target=link.get_link, args=('link3.ini', '20180717091430' + 'serial.xls', timerun,3))
            threads.append(t3)
            t4 = threading.Thread(target=link.get_link, args=('link4.ini', '20180717091430' + 'serial.xls', timerun,4))
            threads.append(t4)
            t5 = threading.Thread(target=link.get_link, args=('link5.ini', '20180717091430' + 'serial.xls', timerun,5))
            threads.append(t5)
            for t in threads:
                t.setDaemon(True)
                t.start()
            for t in threads:
                t.join()
            time.sleep(5)
            hb = hebinxls()
            hb.hebin(timerun)
            print(u"完成所有进程")