#coding=utf-8
import requests
import xml.etree.ElementTree as ET
import sys
from __init__ import app

def sendMsg(phone, content):
    payload = {'method':'Submit','account': app.config['SMS_ACCOUNT'] , \
        'password': app.config['SMS_PASSWORD'], 'mobile': phone,'content': content}
    r = requests.get(url = app.config['SMS_URL'], params = payload)
    root = ET.fromstring(r.text)
    sms_code = root.find(app.config['SMS_CODE_SEARCH'])
    return sms_code.text

if __name__ == "__main__":
    # payload = {'method':'Submit','account':'cf_ycnws','password':'hym123456',
    #     'mobile':'18671755701','content':'您的验证码是：【2234】。请不要把验证码泄露给其他人。'}
    reload(sys)  
    sys.setdefaultencoding('utf8')

    phone = '186755701'
    content = '您的验证码是：【2499】。请不要把验证码泄露给其他人。'
    r = sendMsg(phone, content)
    print r
    # payload = {'method':'Submit','account':'cf_ycnws','password':'hym123456',
        # 'mobile': phone,'content': content}
    # r = requests.get(url = 'http://106.ihuyi.cn/webservice/sms.php', params = payload)
    # print(r.status_code, r.reason)    
    # print(r.text)
