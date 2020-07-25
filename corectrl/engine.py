import os

path_cmd = 'cd /d F:/pythonprojects/mbackend/SRI_scrapy'
spidercmd1 = 'scrapy crawl sh_annual'
spidercmd2 = 'scrapy crawl sh_mid'
os.system(path_cmd + ' && ' + spidercmd1)
os.system(path_cmd + ' && ' + spidercmd2)
