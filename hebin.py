import xlrd
import xlwt


class hebinxls():
    def hebin(self,timerun):
        myfile = xlwt.Workbook()
        wtable = myfile.add_sheet(u"信息", cell_overwrite_ok=True)
        wtable.write(0, 0, u"名字")
        wtable.write(0, 1, u"番号")
        wtable.write(0, 2, u"文件名")
        wtable.write(0, 3, u"文件大小")
        wtable.write(0, 4, u"文件更新日期")
        wtable.write(0, 5, u"链接")
        wtable.write(0, 6, u"磁力链接")
        p=0
        for i in range(1,6):
            data = xlrd.open_workbook(timerun + "link"+str(i)+".xls")
            table = data.sheets()[0]
            nrows = table.nrows
            for j in range(nrows):
                if j == 0 :
                    continue
                else:
                    wtable.write(p + j, 0, table.cell(j, 0).value)
                    wtable.write(p + j, 1, table.cell(j, 1).value)
                    wtable.write(p + j, 2, table.cell(j, 2).value)
                    wtable.write(p + j, 3, table.cell(j, 3).value)
                    wtable.write(p + j, 4, table.cell(j, 4).value)
                    wtable.write(p + j, 5, table.cell(j, 5).value)
                    wtable.write(p + j, 6, table.cell(j, 6).value)
            p += nrows-1

        filename = timerun + "link.xls"
        myfile.save(filename)
        print(u"自动合并%s的磁力链接备份" % timerun)