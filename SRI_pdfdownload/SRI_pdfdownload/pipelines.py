from .items import *
import pymysql

class SriPdfdownloadPipeline:

    def process_item(self, item, spider):

        if isinstance(item, SriAnnualItem):
            id = item['link'].split('/')[-1]
            print('\n', "处理SriAnnualItem", '\n')
            with open('F:/pythonprojects/getpdf/shangzheng/{}'.format(id), 'wb') as fp:
                fp.write(item['content'])


        elif isinstance(item, SriMidItem):
            id = item['link'].split('/')[-1]
            print('\n', "处理SriMidItem", '\n')
            url = 'F:/pythonprojects/data/sh_mid/{}'.format(id)
            print("item.url : {}".format(url))
            with open('F:/pythonprojects/data/sh_mid/{}'.format(id), 'wb') as fp:
                fp.write(item['content'])

        else:
            return item
