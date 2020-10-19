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

    #删除
    def delete(self, request):
        print("aaa222")
        print("tag:", request.data)
        try:
            #获取数据       交易所信息，两个关键词，邮箱
            # exchange = request.data['exchange']
            # exchange = 'sh'
            # title_code = request.data['title_code']
            # content = request.data['content']
            # email = request.data['email']
            # session = request.data['session']
            id = request.data['id']

            # self.ret['data'] = []
            # self.ret["data"].append(exchange)
            # self.ret["data"].append(title_code)
            # self.ret["data"].append(content)
            # self.ret["data"].append(email)
            # self.ret["data"].append(session)
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

    #添加
    def post(self, request):
        print("aaa")
        try:
            #获取数据
            reportType = {
                "first-session-report": "first",
                "mid-year-report": "mid",
                "third-session-report": "third",
                "year-report": "annual",
            }
            exchange = 'sh'
            title_code = request.data['nameOrId']
            content = request.data['keywords']
            email = request.data['email']
            session = reportType[request.data['reportType']]

            print(title_code, content, email, session)

            if not title_code:
                self.ret["code"] = "3008"
                self.ret['msg'] = "股票名或股票代码不能为空"
                return JsonResponse(self.ret)

            self.ret['data'] = [{}]
            self.ret["data"][0]["exchange"] = exchange
            self.ret["data"][0]["session"] =session
            self.ret["data"][0]["title_code"] =title_code
            self.ret["data"][0]["content"] = content
            self.ret["data"][0]["email"] = email

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
                self.ret['code'] = "3001"
                self.ret['msg'] = "添加成功"


        except Exception as e:
            self.ret['code'] = "3008"
            self.ret['msg'] = "添加异常"

        return JsonResponse(self.ret)
