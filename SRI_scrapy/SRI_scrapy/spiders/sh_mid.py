# -*- coding: utf-8 -*-
import scrapy
import selenium
import time
import os
import random
import pymysql
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from SRI_scrapy.items import *
from selenium.webdriver.chrome.options import Options



class ShMidSpider(scrapy.Spider):
    name = 'sh_mid'

    def __init__(self):
        #打开第一页
        self.start_urls = ['http://www.sse.com.cn/disclosure/listedinfo/regular/']

        #打开浏览器
        chrome_opt = Options()
        chrome_opt.add_argument('--headless')
        chrome_opt.add_argument('--disable-gpu')
        chrome_opt.add_argument("--no-sandbox")  # 使用沙盒模式运行
        self.driver = webdriver.Chrome()
        self.driver.get('http://www.sse.com.cn/disclosure/listedinfo/regular/')
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="tabs-658545"]/ul/li[4]/a').click()

        #更新标记位
        self.flag = True

        # 打开数据库
        self.db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='sh')
        self.cursor = self.db.cursor()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # 获取一页的记录
        dd_list = self.driver.find_elements_by_xpath('//*[@id="tabs-658545"]/div[1]/dl//dd/a')
        for dd in dd_list:
            # 提取单个数据
            item = SriMidItem()
            item['link'] = dd.get_attribute('href')
            item['code'] = dd.text.split(':')[0]
            item['title'] = dd.text.split(':')[1]
            item['date'] = time.time()

            # 数据库查找
            sql = "select * from sh.sh_mid WHERE link='{}';".format(item['link'])
            self.cursor.execute(sql)  # 查找
            fetchall = self.cursor.fetchall()
            print(fetchall)
            # 已存在，则说明之后的也已经存在
            if fetchall != ():
                # print("\n---------已存在\n")
                self.flag = False
                break
            # 不存在 则要存入数据库
            else:
                print('\n--------------理应返回一个item-------------\n')
                yield item

        #2020/7/22半年报页面暂时没有翻页，但是通过xpath路径又能够找到它，暂时采用对这个单页面进行经常性的读取，以此不需要用上翻页
        # next_page = self.driver.find_elements_by_xpath('//*[@id="idStr"]')[-1]
        #
        # if next_page.get_attribute('page') != None and self.flag:  # 存在下一页并且本页均不在数据库中
        #
        #     next_page.click()
        #     time.sleep(1)
        #     yield scrapy.Request(url=self.start_urls[0], callback=self.parse, dont_filter=True)
