from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.views import APIView
import pymysql
import smtplib
from email.header import Header  # 定义邮件标题
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
import os

def send_mail(exchange, session, lists, receiver):
    ''' file_path为要邮件发送的文件路径, receiver为用户邮箱'''
    user = "13336130340@163.com"
    password = "hys526956h"
    smtpserver = 'smtp.163.com'
    sender = "13336130340@163.com"
    receive = receiver

    #DEBUG 1
    print(1)
    # 邮件对象:
    msg = MIMEMultipart()
    msg['From'] = "13336130340@163.com"
    msg['To'] = receiver
    msg['Subject'] = Header("帮我盯着检测到新报表", 'utf-8').encode()

    table = exchange + '_' + session

    for list in lists:

        file_path = r"F:/pythonprojects/data/{}/".format(table) + list['link'].split('/')[-1].strip()

        if os.path.exists(file_path):
            content = open(file_path, 'rb').read()  # 读取内容
            filemsg = MIMEBase("application", 'pdf')
            filemsg.set_payload(content)
            encode_base64(filemsg)
            db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db=exchange)
            cursor = db.cursor()
            sql = "select * from {0} where link = '{1}'".format(table, list['link'].strip())
            cursor.execute(sql)
            ll = cursor.fetchall()[0]
            db.close()
            filemsg.add_header('Content-Disposition', 'attachment', filename=ll[1] + ll[2] + '.pdf')
            msg.attach(filemsg)

    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    smtp.helo(smtpserver)
    smtp.ehlo(smtpserver)  # 服务器返回结果确认
    smtp.login(user, password)  # 登录邮箱服务器用户名和密码
    print("开始发送邮件...")
    smtp.sendmail(sender, receive, msg.as_string())
    smtp.quit()
    print("邮件发送完成！")
    return True


class EmailView(APIView):

    def post(self, request):
        ret = {
            "code" : "4000",
            "msg" : None,
            "data" : None
        }

        #获取数据
        try:

            records = request.data['records']
            email = request.data['email']
            extrance = request.data['extrance']
            session = request.data['session']


            # 判断

            if not records:
                ret["code"] = "4008"
                ret["msg"] = "没有要发送邮件的信息"
                return JsonResponse(ret)

            else:
                if send_mail(extrance, session, records, email):
                    ret['code'] = "4001"
                    ret['msg'] = "发送成功"
                else:
                    ret['code'] = "4008"
                    ret['msg'] = "发送失败"
                    return JsonResponse(ret)
        except:
            ret['code'] = "4008"
            ret['msg'] = "发送异常"

        return JsonResponse(ret)