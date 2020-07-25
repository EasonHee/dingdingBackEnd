import re
import hashlib
from users import models
from django.http import JsonResponse
from rest_framework.views import APIView

# Create your views here.

class UsersView(APIView):

    def changeMD5(self, password):
        md5 = hashlib.md5()
        md5.update(password.encode())
        return md5.hexdigest()

    def post(self, request):
        ret = {"code" : "1000",
               "msg" : None}
        try:
            # 参数是datadict 形式
            email = request.data.get('email')
            password = request.data.get('password')
            action = request.data.get('action')

            # 登录部分
            if action == "login":
                password_md5 = self.changeMD5(password)
                print(password_md5)
                # email和password字段与数据的比对看是否一致
                obj = models.UsersInfo.objects.filter(email=email,password=
                password_md5).first()
                if not obj:
                    ret['code'] = '1001'
                    ret['msg'] = '邮箱或者密码错误'
                    return JsonResponse(ret)
                ret['msg'] = '1002'
                ret['msg'] = '登录成功'

            # 注册部分
            elif action == "register":
                # 1. 判断邮箱是否合法
                ex_email = re.compile(r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@'
                                      r'([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$')
                result = ex_email.match(email)
                if not result:
                    ret['code'] = '1003'
                    ret['msg'] = '邮箱不合法' + email
                    return JsonResponse(ret)

                # 2. 判断邮箱是否已注册
                obj = models.UsersInfo.objects.filter(email=email).first()
                if obj:
                    ret['code'] = '1004'
                    ret['msg'] = '邮箱已存在'
                    return JsonResponse(ret)

                # 3. 存入数据库
                # 使用md5加密密码, 不将密码明文暴露在数据库
                password_md5 = self.changeMD5(password)
                models.UsersInfo.objects.create(email=email, password=
                password_md5)
                ret['msg'] = '注册成功'

            else:
                ret['code'] = '1008'
                ret['msg'] = '请求异常, action错误'
        except Exception as e:
            ret['code'] = '1008'
            ret['msg'] = '请求异常'
        return JsonResponse(ret)