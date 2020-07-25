# -*- coding: utf-8 -*-
import scrapy
import os
import pymysql
from SRI_pdfdownload.items import SriAnnualItem

class ShAnnualSpider(scrapy.Spider):
    name = 'sh_annual'

    def start_requests(self):
        # 获取下载链接
        self.db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='sh')
        cursor = self.db.cursor()
        sql = "select * from sh.sh_annual"
        cursor.execute(sql)  # 查找
        infos = cursor.fetchall()

        for info in infos:
            print(info)
            id = info[4].split('/')[-1]
            if not os.path.exists('F:/pythonprojects/getpdf/shangzheng/{}'.format(id).strip()):
                yield scrapy.Request(url=info[4], callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = SriAnnualItem()
        item['content'] = response.body
        item['link'] = response.url
        yield item

    def closed(self, spider):
        self.db.close()
