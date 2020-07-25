import os
import time
from toes import *


while True:
    now = time.time()
    #记录爬取
    print("开始爬取网页记录\n")
    path_cmd = 'cd /d F:/pythonprojects/mbackend/SRI_scrapy'
    spidercmd1 = 'scrapy crawl sh_annual'
    spidercmd2 = 'scrapy crawl sh_mid'
    os.system(path_cmd + ' && ' + spidercmd1)
    os.system(path_cmd + ' && ' + spidercmd2)

    #pdf下载
    print("开始下载pdf\n")
    path_cmd2 = 'cd /d F:/pythonprojects/mbackend/SRI_pdfdownload'
    os.system(path_cmd2 + " && " + spidercmd1)
    os.system(path_cmd2 + " && " + spidercmd2)

    #es更新
    print("开始更新es")
    an_rpt_updata(now)
    mid_rpt_updata(now)

    #自动发送


