from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .plugin import ReportRemoteEs

# Create your views here.

class EsearchView(APIView):

    def post(self, request):
        '''获取es数据'''
        ret = {"code" : "2000",
               "msg" : None,
               "data" : None}
        print(1)
        try:
            reportType = {
                "first-session-report" : "sh_first",
                "mid-year-report": "sh_mid",
                "third-session-report" : "sh_third",
                "year-report": "sh_annual",
            }
            print("GET Type:",request.data.get("reportType"))
            #获取字段
            title_code = request.data.get("nameOrId")
            content = request.data.get("keywords")
            index = reportType[request.data.get("reportType")]
            print(request.data.get("reportType"))

            print(str)

            #检查校验
            if not title_code:
                ret["code"] = "2002"
                ret['msg'] = "股票名或股票代码不能为空"
                return JsonResponse(ret)

            #确定搜索体
            body = {"index" : "", "title_code" : "", "content" : "", "content_max_length" : 100, "link" : "",
                   "start" : '', "size" : '20', "highlight" : True, "raw" : False}
            body["title_code"] = title_code
            body["index"] = index
            body["content"] = content

            #搜索
            remotees = ReportRemoteEs(url='es-cn-oew1qr55r000dbtk6.public.elasticsearch.aliyuncs.com',
                                http_auth=('elastic', "HYS526956h"))

            ret["data"] = remotees.search(index=body["index"], title_code=body["title_code"], content=body["content"],
                                                content_max_length=body["content_max_length"], link=body['link'], start=body["start"],
                                                size=body['size'], highlight=body['highlight'], raw=body["raw"])

            if len(ret['data']) == 0:
                ret['msg'] = "查询成功，暂无相关数据"
                ret['code'] = "2008"
            else:
                ret['msg'] = "查询成功"
                ret['code'] = "2001"


        except Exception as e:
            print(e)
            ret['code'] = "2008"
            ret['msg'] = "查询异常"

        #返回
        return JsonResponse(ret)

