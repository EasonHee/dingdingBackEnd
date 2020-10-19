from django.shortcuts import render

# Create your views here.
import os
import time
import zipfile
import pymysql
import smtplib
from email.header import Header  # 定义邮件标题
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from django.http import JsonResponse
from email.encoders import encode_base64
from rest_framework.views import APIView
from email.mime.multipart import MIMEMultipart

def send_email(exchange, session, lists, receiver):
    ''' file_path为要邮件发送的文件路径, receiver为用户邮箱'''
    try:
        table = exchange + '_' + session
        now = time.strftime("%Y-%m-%d", time.localtime())

        user = "13336130340@163.com"
        password = "hys526956h"
        smtpserver = 'smtp.163.com'
        sender = "13336130340@163.com"
        receive = receiver

        # 邮件对象:
        msg = MIMEMultipart()
        msg['From'] = "13336130340@163.com"
        msg['To'] = receiver
        msg['Subject'] = Header("【帮我盯着】{}最新报表".format(now), 'utf-8').encode()

        #文字内容
        text = ''

        #附件内容
        # zip = zipfile.ZipFile('帮我盯着.zip', 'w', zipfile.ZIP_DEFLATED)
        # zip.close()

        if lists:
            for list in lists:

                file_path = "F:/pythonprojects/data/{}/".format(table) + list['link'].split('/')[-1].strip()

                if os.path.exists(file_path):

                    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db=exchange)
                    cursor = db.cursor()
                    sql = "select * from {0} where link = '{1}'".format(table, list['link'].strip())
                    cursor.execute(sql)
                    ll = cursor.fetchall()[0]
                    db.close()

                    text += '    股票代码:{0}\t报表名称:{1}\t下载地址:{2} \n'.format(ll[1], ll[2], ll[4])
                    # zip = zipfile.ZipFile('帮我盯着.zip', 'a', zipfile.ZIP_DEFLATED)
                    # zip.write(file_path, ll[1] + ll[2] + '.pdf')
                    # zip.close()

            content = open("帮我盯着.zip", 'rb').read()
            # filemsg = MIMEBase("application", 'zip')
            # filemsg.set_payload(content)
            # encode_base64(filemsg)
            # filemsg.add_header('Content-Disposition', 'attachment', filename="{}最新报表".format(now) + '.zip')

            message = MIMEText('    [帮我盯着]\n    以下是为您提供的报表信息:\n\n{}'.format(text) +
                               '\n    文件已打包放到附件中，可点击下载\n\n\n', 'plain', 'utf-8')

            #添加
            # msg.attach(filemsg)
            msg.attach(message)

            #发送
            smtp = smtplib.SMTP_SSL(smtpserver, 465)
            smtp.helo(smtpserver)
            smtp.ehlo(smtpserver)  # 服务器返回结果确认
            smtp.login(user, password)  # 登录邮箱服务器用户名和密码
            print("开始发送邮件...")
            smtp.sendmail(sender, receive, msg.as_string())
            smtp.quit()
            print("邮件发送完成！")

            return True

        else:
            print("传递的链接信息无内容\n")
            return False

    except Exception as e:
        print("Exception", e)


class EmailView(APIView):

    def post(self, request):
        ret = {
            "code" : "4000",
            "msg" : None,
            "data" : None
        }
        reportType = {
            "year-report": "annual",
            "mid-year-report": "mid",
            "first-session-report" : "first",
            "third-session-report" : "third"
        }

        #获取数据
        try:

            records = request.data['searchList']
            email = request.data['email']
            # exchange = request.data['exchange']
            exchange = "sh"
            session =  reportType[request.data['reportType']]


            # 判断

            if not records:
                ret["code"] = "4008"
                ret["msg"] = "没有要发送邮件的信息"
                return JsonResponse(ret)

            else:
                if send_email(exchange, session, records, email):
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