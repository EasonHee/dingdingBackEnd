from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .plugin import ReportRemoteEs

# Create your views here.

class EsearchView(APIView):

    def get(self, request):
        '''获取es数据'''
        ret = {"code" : "2000",
               "msg" : None,
               "data" : None}

        try:
            #获取字段
            str = request.GET.get('fields')
            fields = str.split(',')

            #检查校验
            if not ("index" in fields and "title_code" in fields):
                ret["code"] = 2002
                ret['msg'] = "查找格式错误"
                return JsonResponse(ret)

            #确定搜索体
            body = {"index" : "", "title_code" : "", "content" : "", "content_max_length" : 300, "link" : "",
                   "start" : '', "size" : '10', "highlight" : True, "raw" : False}
            for field in fields:
                value = request.GET.get(field)
                body[field] = value

            #搜索
            remotees = ReportRemoteEs(url='es-cn-oew1qr55r000dbtk6.public.elasticsearch.aliyuncs.com',
                                http_auth=('elastic', "HYS526956h"), index='test')
            ret["data"] = remotees.search(index=body["index"], title_code=body["title_code"], content=body["content"],
                                                content_max_length=body["content_max_length"], link=body['link'], start=body["start"],
                                                size=body['size'], highlight=body['highlight'], raw=body["raw"])
            ret['code'] = 2001
            ret['msg'] = "查询成功"

        except:
            ret['code'] = "2008"
            ret['msg'] = "查询失败"

        #返回
        return JsonResponse(ret)

