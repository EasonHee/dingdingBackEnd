""""""
import os
import pymysql
from pdf_to_txt import pdf2txt
from es_functions import ReportRemoteEs
from Mysql_functions import ReportLocalDB


#年报
def an_rpt_updata(cir_bg_time):
    """年报es更新"""
    #1、连接
    rptdb = ReportLocalDB("sh")

    #2、查找
    condition = "where date > {}".format(cir_bg_time)
    results = rptdb.find("sh", "sh_annual", condition=condition)

    #3、判断
    if len(results) == 0:
        return False

    #4、更新es
    es = ReportRemoteEs(url='es-cn-oew1qr55r000dbtk6.public.elasticsearch.aliyuncs.com',
                        http_auth=('elastic', "HYS526956h"), index="test")

    for result in results:
        #1、获取pdf内容
        url = 'F:/pythonprojects/data/sh_annual/{}'.format(result[4].split('/')[-1])
        if os.path.exists(url):
            content = pdf2txt(url=url)
            #2、确认添加体
            body = {}
            body['code'] = result[1]
            body['title'] = result[2]
            body['date'] = result[3]
            body['link'] = result[4]
            body['content'] = content
            #3、添加
            es.add(index="test", body=body)

#中报
def mid_rpt_updata(cir_bg_time):
    """年中报es更新"""
    #1、连接
    rptdb = ReportLocalDB("sh")

    #2、查找
    condition = "where date > {}".format(cir_bg_time)
    results = rptdb.find("sh", "sh_mid", condition=condition)

    #3、判断
    if len(results) == 0:
        return False

    #4、更新es
    es = ReportRemoteEs(url='es-cn-oew1qr55r000dbtk6.public.elasticsearch.aliyuncs.com',
                        http_auth=('elastic', "HYS526956h"), index="test")

    for result in results:
        #1、获取pdf内容
        url = 'F:/pythonprojects/data/sh_mid/{}'.format(result[4].split('/')[-1])
        if os.path.exists(url):
            content = pdf2txt(url=url)
            #2、确认添加体
            body = {}
            body['code'] = result[1]
            body['title'] = result[2]
            body['date'] = result[3]
            body['link'] = result[4]
            body['content'] = content
            #3、添加
            es.add(index="test", body=body)

if __name__ == "__main__":
    mid_rpt_updata(1595402779.27874)