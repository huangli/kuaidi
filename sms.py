#coding=utf-8
import requests

def sendMsg(phone, content):
    payload = {'method':'Submit','account':'cf_ycnws','password':'hym123456',
        'mobile': phone,'content': content}
    r = requests.get(url = 'http://106.ihuyi.cn/webservice/sms.php', params = payload)

if __name__ == "__main__":
    # payload = {'method':'Submit','account':'cf_ycnws','password':'hym123456',
    #     'mobile':'18671755701','content':'您的验证码是：【2234】。请不要把验证码泄露给其他人。'}
    phone = '18671755701'
    content = '您的验证码是：【2499】。请不要把验证码泄露给其他人。'
    # payload = {'method':'Submit','account':'cf_ycnws','password':'hym123456',
        # 'mobile': phone,'content': content}
    # r = requests.get(url = 'http://106.ihuyi.cn/webservice/sms.php', params = payload)
    # print(r.status_code, r.reason)    
    # print(r.text)
