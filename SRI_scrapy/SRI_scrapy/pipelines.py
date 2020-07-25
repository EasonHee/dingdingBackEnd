import pymysql
from .items import *


class SriScrapyPipeline:

    def __init__(self):

        self.db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='sh')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):

        print('\n---------------理应写入一个数据数据库----------------\n')

        # 年报表 (id, code, title, date, link)
        if isinstance(item, SriAnnualItem):
            sql = "insert into sh.sh_annual(`code`, `title`, `date`, `link`) values(%s,%s,%s,%s);"
            self.cursor.execute(sql, (item['code'], item['title'], item['date'], item['link']))
            self.db.commit()
            return item

        # 中报表 (id, code, title, date, link)
        elif isinstance(item, SriMidItem):
            sql = "insert into sh.sh_mid(`code`, `title`, `date`, `link`) values(%s,%s,%s,%s);"
            self.cursor.execute(sql, (item['code'], item['title'], item['date'], item['link']))
            self.db.commit()
            return item

        else:
            return item


    def close_spider(self, spider):
        self.db.close()