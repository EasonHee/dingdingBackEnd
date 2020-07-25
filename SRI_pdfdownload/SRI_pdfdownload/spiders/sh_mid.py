# -*- coding: utf-8 -*-
import scrapy
import os
import pymysql
from SRI_pdfdownload.items import SriMidItem

class ShMidSpider(scrapy.Spider):
    name = 'sh_mid'

    def start_requests(self):
        # 获取下载链接
        self.db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='sh')
        cursor = self.db.cursor()
        sql = "select * from sh.sh_mid"
        cursor.execute(sql)  # 查找
        infos = cursor.fetchall()

        for info in infos:
            id = info[4].split('/')[-1]
            print("id  :", id, '\n')
            print('info[4] : ', info[4], '\n')
            if not os.path.exists('F:/pythonprojects/data/sh_mid/{}'.format(id).strip()):
                yield scrapy.Request(url=info[4], callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = SriMidItem()
        item['content'] = response.body
        item['link'] = response.url
        print('link123', item['link'], '\n')
        yield item

    def closed(self, spider):
        self.db.close()
