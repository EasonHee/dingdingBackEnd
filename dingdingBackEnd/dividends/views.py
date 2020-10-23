from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
import pymysql
from dividends import models
import datetime

# Create your views here.

class DividendsView(APIView):
    ret = {
        "code": "2000",
        "msg": None,
        "data": None
    }
    pageSize = 20


    def get(self, request):
        try:
            currentPage = int(request.GET.get('page'))
            startRow = (currentPage - 1) * self.pageSize
            endRow = currentPage * self.pageSize
            currentYear = datetime.datetime.now().year

            queryResult = models.DividendsInfo.objects.filter(noticeDate__gte=currentYear).order_by("-noticeDate").values()
            total = len(queryResult)
            dividendsInfos = queryResult[startRow: endRow]
            # dividendsInfos = tuple(tuple([x[y] for y in x]) for x in dividendsInfos)
            # dividendsInfos = self._dbRecords_format(dividendsInfos)
            self.ret['data'] = list(dividendsInfos)
            self.ret['total'] = total
            if len(self.ret['data']) == 0:
                self.ret['msg'] = "查询成功，暂无相关数据"
                self.ret['code'] = "3008"
            else:
                self.ret['msg'] = "查询成功"
                self.ret['code'] = "3001"
        except Exception as e:
            print("eee")
            print(e)
            self.ret['code'] = "3008"
            self.ret['msg'] = "查找失败"
        return JsonResponse(self.ret)

    def post(self, request):

        try:
            # 获取字段
            title_code = request.data.get("nameOrId")
            cashMin = request.data.get("cashMin")
            cashMax = request.data.get("cashMax")
            sendMin = request.data.get("sendMin")
            sendMax = request.data.get("sendMax")
            conversionMin = request.data.get("conversionMin")
            conversionMax = request.data.get("conversionMax")
            rateMin = request.data.get("rateMin")
            rateMax = request.data.get("rateMax")
            currentPage = int(request.data.get("page"))
            startRow = (currentPage - 1) * self.pageSize
            endRow = currentPage * self.pageSize
            currentYear =datetime.datetime.now().year
            print(title_code)
            print(cashMin)
            print(cashMax)
            if title_code:
                queryResult = models.DividendsInfo.objects.filter(noticeDate__gte=currentYear,
                                                                  value__range=(cashMin, cashMax),
                                                                  code=title_code).order_by("-noticeDate").values()
            else:
                queryResult = models.DividendsInfo.objects.filter(noticeDate__gte=currentYear,
                                                                  value__range=(cashMin, cashMax)
                                                                  ).order_by("-noticeDate").values()
            total = len(queryResult)
            print(total)
            dividendsInfos = queryResult[startRow: endRow]
            print(dividendsInfos)
            self.ret['data'] = list(dividendsInfos)
            self.ret['total'] = total
            if len(self.ret['data']) == 0:
                self.ret['msg'] = "查询成功，暂无相关数据"
                self.ret['code'] = "2008"
            else:
                self.ret['msg'] = "查询成功"
                self.ret['code'] = "2001"
        except Exception as e:
            print(e)
            self.ret['code'] = "2008"
            self.ret['msg'] = "查询异常"

        # 返回
        return JsonResponse(self.ret)

    def _dbRecords_format(self, dbRecords):
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
                cursor.execute("select name from fromfrontend.stock_attrs where `code`='{}' limit 1".format(codeKey))
                # 代码 股票名 送股 转股 现金分红 分红比例 公告名字 发布时间 报告所属时间阶段
                resultRecords.append(['', '', '', '', '', '', '', '', '', '', ''])
                resultRecords[-1][0] = resultDic[codeKey][periodKey][0][0]
                title = cursor.fetchall()
                if (title):
                    resultRecords[-1][1] = title[0][0]
                resultRecords[-1][7] = resultDic[codeKey][periodKey][0][3]
                resultRecords[-1][8] = resultDic[codeKey][periodKey][0][4]
                resultRecords[-1][9] = resultDic[codeKey][periodKey][0][5]
                resultRecords[-1][5] = resultDic[codeKey][periodKey][0][9]
                resultRecords[-1][10] = resultDic[codeKey][periodKey][0][1]
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
    def search(self, period='', code='', rateMin='', rateMax='', dateMin='', dateMax=''):
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
        return self.dbRecords_format(cursor.fetchall())







