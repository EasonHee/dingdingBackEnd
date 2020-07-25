from .items import *
import pymysql

class SriPdfdownloadPipeline:

    def process_item(self, item, spider):

        if isinstance(item, SriAnnualItem):

            print('\n', "处理SriAnnualItem : {}".format(item['link']), '\n')

            id = item['link'].split('/')[-1]
            url = 'F:/pythonprojects/data/sh_annual/{}'.format(id)
            with open(url, 'wb') as fp:
                fp.write(item['content'])


        elif isinstance(item, SriMidItem):

            print('\n', "处理SriMidItem : {}".format(item['link']), '\n')

            id = item['link'].split('/')[-1]
            url = 'F:/pythonprojects/data/sh_mid/{}'.format(id)
            with open(url, 'wb') as fp:
                fp.write(item['content'])

        else:
            return item
