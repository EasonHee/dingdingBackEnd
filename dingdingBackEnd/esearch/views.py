from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .plugin import ReportRemoteEs
import pymysql


# Create your views here.

class EsearchView(APIView):
    ret = {
        "code": "2000",
        "msg": None,
        "data": None
    }

    def dbRecords_format(dbRecords):
        """将dbRecords中每支股票的数据进行整合
            因为从数据库中获得的数据，传来多条记录，一条记录是现金分红数据
            另一个是转股数据，所以针对某一支股票，需要将这些数据进行整合
        Args:
            dbRecords: typle(tuple())
                dbRecords:为数据库数据

        Returns:
            list[list[code, ]]
        """
        resultDic = {}
        resultRecords = []
        db = pymysql.connect(host='localhost', user='root', password='123456', port=3306)
        cursor = db.cursor()

        for record in dbRecords:
            # 无这支股票数据
            if (record[0] not in resultDic.keys()):
                resultDic[record[0]] = {record[1]: [record]}
            # 有这只股票数据没有这一日期数据
            elif (record[1] not in resultDic[record[0]].keys()):
                resultDic[record[0]][record[1]] = [record]
            else:
                resultDic[record[0]][record[1]].append(record)

        for codeKey in resultDic.keys():
            for periodKey in resultDic[codeKey].keys():
                cursor.execute("select name from stockinfos.stock_attrs where `code`='{}' limit 1".format(codeKey))
                # 代码 股票名 送股 转股 现金分红 分红比例 公告名字 发布时间
                resultRecords.append(['', '', '', '', '', '', '', '', '', ''])
                resultRecords[-1][0] = resultDic[codeKey][periodKey][0][0]
                title = cursor.fetchall()
                if (title):
                    resultRecords[-1][1] = title[0][0]
                resultRecords[-1][7] = resultDic[codeKey][periodKey][0][3]
                resultRecords[-1][8] = resultDic[codeKey][periodKey][0][4]
                resultRecords[-1][9] = resultDic[codeKey][periodKey][0][5]
                resultRecords[-1][5] = resultDic[codeKey][periodKey][0][9]
                for record in resultDic[codeKey][periodKey]:
                    if (record[7] == 'send'):
                        resultRecords[-1][2] = record[2]
                    if (record[7] == 'conversion'):
                        resultRecords[-1][3] = record[2]
                    if (record[7] == 'cash'):
                        resultRecords[-1][4] = record[2]
                        resultRecords[-1][6] = record[8]

        db.close()
        return resultRecords

    # 包括时间 利率 代码
    def search(period='', code='', rateMin='', rateMax='', dateMin='', dateMax=''):
        db = pymysql.connect(host='localhost', user='root', password='123456', port=3306)
        cursor = db.cursor()
        sql = "SELECT * FROM stockinfos.`our_divis` WHERE TRUE and `code` regexp '^6.*' and `rate`+0 < 0.25"

        if (code):
            sql += " AND `code`='{}'".format(code)
        if (period):
            sql += " AND `period` = '{}'".format(period)
        if (rateMin and rateMax):
            sql += " AND rate+0 between {} and {}".format(rateMin, rateMax)
        if (dateMin and dateMax):
            sql += " AND noticeDate between '{}' and '{}'".format(dateMin, dateMax)

        cursor.execute(sql)
        self.dbRecords_format(cursor.fetchall())


    def get(self, request):
        try:
            email = request.GET.get('email')
            session = request.GET.get('reportType')
            userinfo = KeywordsInfo.objects.filter(email=email, session=session).values()
            self.ret['data'] = list(userinfo)
            self.ret['code'] = "3001"
            self.ret['msg'] = "查询成功"
            return JsonResponse(self.ret)
        except:
            self.ret['code'] = "3008"
            self.ret['msg'] = "查找失败"

        print(self.ret)
        return JsonResponse(self.ret)

    def post(self, request):
        '''获取es数据'''
        ret = {"code": "2000",
               "msg": None,
               "data": None}
        print(request.data)
        try:
            reportType = {
                "first-session-report": "sh_first",
                "mid-year-report": "sh_mid",
                "third-session-report": "sh_third",
                "year-report": "sh_annual",
            }

            # 获取字段
            title_code = request.data.get("nameOrId")
            cash = request.data.get("cash")
            send = request.data.get("send")
            conversion = request.data.get("conversion")
            rate = request.data.get("rate")

            # #检查校验
            # if not title_code:
            #     ret["code"] = "2002"
            #     ret['msg'] = "股票名或股票代码不能为空"
            #     return JsonResponse(ret)
            #
            # #确定搜索体
            # body = {"index" : "", "title_code" : "", "content" : "", "content_max_length" : 100, "link" : "",
            #        "start" : '', "size" : '20', "highlight" : True, "raw" : False}
            # body["title_code"] = title_code
            # body["index"] = index
            # body["content"] = content
            #
            # #搜索
            # remotees = ReportRemoteEs(url='es-cn-oew1qr55r000dbtk6.public.elasticsearch.aliyuncs.com',
            #                     http_auth=('elastic', "HYS526956h"))
            #
            # ret["data"] = remotees.search(index=body["index"], title_code=body["title_code"], content=body["content"],
            #                                     content_max_length=body["content_max_length"], link=body['link'], start=body["start"],
            #                                     size=body['size'], highlight=body['highlight'], raw=body["raw"])
            #
            # if len(ret['data']) == 0:
            #     ret['msg'] = "查询成功，暂无相关数据"
            #     ret['code'] = "2008"
            # else:
            #     ret['msg'] = "查询成功"
            #     ret['code'] = "2001"


        except Exception as e:
            print(e)
            ret['code'] = "2008"
            ret['msg'] = "查询异常"

        # 返回
        return JsonResponse(ret)




