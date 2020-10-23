import time
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import KeywordsInfo

# Create your views here.

class KeywordsView(APIView):
    """对用户的关键词进行操作"""
    ret = {
        "code" : "3000",
        "msg" : None,
        "data" : None
    }

    # 请求数据
    def get(self, request):
        try:
            email = request.GET.get('email')
            userinfo = KeywordsInfo.objects.filter(email=email).values()
            self.ret['data'] = list(userinfo)
            self.ret['code'] = "3001"
            self.ret['msg'] = "查询成功"
            return JsonResponse(self.ret)
        except:
            self.ret['code'] = "3008"
            self.ret['msg'] = "查找失败"

        print(self.ret)
        return JsonResponse(self.ret)


    # 添加
    def post(self, request):
        try:
            exchange = 'sh'
            nameOrId = request.data['nameOrId']
            cashMin = request.data['cashMin']
            cashMax = request.data['cashMax']
            sendMin = request.data['sendMin']
            sendMax = request.data['sendMax']
            conversionMin = request.data['conversionMin']
            conversionMax = request.data['conversionMax']
            rateMin = request.data['rateMin']
            rateMax = request.data['rateMax']
            email = request.data['email']



            # 判断 处理    看是否已经有了，是否合法
            result = KeywordsInfo.objects.filter(exchange=exchange,
                                                 nameOrId=nameOrId,
                                                 email=email,
                                                 cashMin=cashMin,
                                                 cashMax=cashMax,
                                                 sendMin=sendMin,
                                                 sendMax=sendMax,
                                                 conversionMin=conversionMin,
                                                 conversionMax=conversionMax,
                                                 rateMin=rateMin,
                                                 rateMax=rateMax,
                                                 ).first()
            if result:
                """已经存在"""
                self.ret['code'] = "3008"
                self.ret['msg'] = "已存在"

            else:
                KeywordsInfo.objects.create(exchange=exchange,
                                            nameOrId=nameOrId,
                                            email=email,
                                            cashMin=cashMin,
                                            cashMax=cashMax,
                                            sendMin=sendMin,
                                            sendMax=sendMax,
                                            conversionMin=conversionMin,
                                            conversionMax=conversionMax,
                                            rateMin=rateMin,
                                            rateMax=rateMax,
                                            createDate=time.time(),
                                            updateDate=time.time()
                                            )
                self.ret['code'] = "3001"
                self.ret['msg'] = "添加成功"


        except Exception as e:
            print(e)
            self.ret['code'] = "3008"
            self.ret['msg'] = "添加异常"

        return JsonResponse(self.ret)

    #删除
    def delete(self, request):
        try:
            id = request.data['id']
            print(self.ret)

            #判断 处理
            result = KeywordsInfo.objects.filter(id=id).first()

            if result:
                result.delete()
                self.ret['code'] = "3001"
                self.ret['msg'] = "删除成功"
            else:
                self.ret['msg'] = "删除失败"
                self.ret['code'] = "3008"

        except:
            self.ret['msg'] = "删除异常"
            self.ret['code'] = "3008"

        return JsonResponse(self.ret)


