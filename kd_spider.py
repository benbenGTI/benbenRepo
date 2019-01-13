#-*- coding: UTF-8 -*-

import sys
import time
import urllib.request
import urllib.error
import urllib
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from bs4 import BeautifulSoup
from imp import reload
from openpyxl import Workbook
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

reload(sys)
#sys.setdefaultencoding('utf8')

#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

mail_info = {
    "from": "493797069@qq.com",
    "to": "wangyue1988cnu@163.com",
    "hostname": "smtp.qq.com",
    "username": "",
    "password": "",
    "mail_encoding": "utf-8"
}

sms_info = {
    "appid": "",
    "appkey": "",
    "sms_sign": ""
}

def kd_spider():
    url = 'http://sjssffy.zhihuixinghe.com/'
    try:
        req = urllib.request.Request(url, headers=hds[1])
        source_code = urllib.request.urlopen(req).read()
        type = sys.getfilesystemencoding()
        source_code = source_code.decode(type)
        #print(source_code)
        plain_text = str(source_code)
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        print (error)

    soup = BeautifulSoup(plain_text)
    notice = soup.find('div', {'class': 'notice'})
    notice_ul = notice.find('ul')
    for notice_title in notice_ul.findAll('a'):
        if notice_title.text.find('2018年') > 0:
            print(notice_title.text)
            #发邮件#
            #send_mail("石景山师范附幼2019年申报已开始")
            #发短信#
            send_sms(["18810450157"], '265617', ['石景山师范妇幼'])
    return

def send_mail(msg):
    smtp = smtplib.SMTP(mail_info["hostname"])
    smtp.set_debuglevel(1)
    
    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])

    msg = MIMEText(msg, "plain", "utf-8")
    msg["Subject"] = Header('kd_notice', "utf-8")
    msg["from"] = mail_info["from"]
    msg["to"] = mail_info["to"]
    
    smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())

    smtp.quit()

# phone_number 接收手机号
# template_id 腾讯云短信模板
def send_sms(phone_number, template_id, sms_param):
    sms_sender = SmsSingleSender(sms_info["appid"], sms_info["appkey"])
    try:
        result = sms_sender.send_with_param(86, phone_number[0],
            template_id, sms_param, sign=sms_info["sms_sign"], extend="", ext="")
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    print(result)
    return

if __name__=='__main__':
    kd_spider()
