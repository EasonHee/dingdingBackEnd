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

    #请求数据   邮件
    def get(self, request):
        try:
            email = request.GET.get('email')
            userinfo = KeywordsInfo.objects.filter(email=email).values()
            self.ret['data'] = list(userinfo)
            self.ret['code'] = "3001"
            self.ret['msg'] = "查询成功"
            print(self.ret)
            return JsonResponse(self.ret)
        except:
            self.ret['code'] = "3008"
            self.ret['msg'] = "查找失败"

        print(self.ret)
        return JsonResponse(self.ret)

    #删除
    def delete(self, request):
        try:
            #获取数据       交易所信息，两个关键词，邮箱
            exchange = request.data['exchange']
            title_code = request.data['title_code']
            content = request.data['content']
            email = request.data['email']
            session = request.data['session']

            self.ret['data'] = []
            self.ret["data"].append(exchange)
            self.ret["data"].append(title_code)
            self.ret["data"].append(content)
            self.ret["data"].append(email)
            self.ret["data"].append(session)
            print(self.ret)

            #判断 处理
            result = KeywordsInfo.objects.filter(exchange=exchange, title_code=title_code,
                                                 content=content,email=email, session=session).first()

            if result:
                result.delete()
                self.ret['code'] = "3002"
                self.ret['msg'] = "删除成功"
            else:
                self.ret['msg'] = "删除失败"
                self.ret['code'] = "3008"

        except:
            self.ret['msg'] = "请求异常"
            self.ret['code'] = "3008"

        return JsonResponse(self.ret)

    #添加
    def post(self, request):
        try:
            #获取数据
            exchange = request.data['exchange']
            title_code = request.data['title_code']
            content = request.data['content']
            email = request.data['email']
            session = request.data['session']

            self.ret['data'] = []
            self.ret["data"].append(exchange)
            self.ret["data"].append(title_code)
            self.ret["data"].append(content)
            self.ret["data"].append(email)
            self.ret["data"].append(session)
            #判断 处理    看是否已经有了，是否合法
            result = KeywordsInfo.objects.filter(exchange=exchange, title_code=title_code,
                                                 content=content, email=email, session=session).first()
            if result:
                """已经存在"""
                self.ret['code'] = "3008"
                self.ret['msg'] = "已存在"

            else:
                KeywordsInfo.objects.create(exchange=exchange, title_code=title_code,
                                            content=content, email=email, session=session,
                                            create_date=time.time(), update_date=time.time())
                self.ret['code'] = "3003"
                self.ret['msg'] = "添加成功"

        except:
            self.ret['code'] = "3008"
            self.ret['msg'] = "添加异常"

        return JsonResponse(self.ret)
