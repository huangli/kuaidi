#coding=utf-8
class BaseConfig(object):
    SMS_SEND_ERROR = '短信发送失败'
    SMS_ACCOUNT = 'cf_ycnws'
    SMS_PASSWORD = 'hym123456'
    SMS_URL = 'http://106.ihuyi.cn/webservice/sms.php'
    SMS_CODE_SEARCH = '{http://106.ihuyi.cn/}code'
    ERROR_404 = '不好意思，该页面不存在，︿(￣︶￣)︿'
    ERROR_500 = '服务器出现出错，请联系系统管理员'
    ERROR_403 = '您需要登录后才能访问该页面'
    PHONE_LENGTH_ERROR = '电话号码格式不正确'

    BABEL_DEFAULT_LOCALE = 'zh_CN'
    SECURITY_USER_IDENTITY_ATTRIBUTES = 'username'
    SECRET_KEY = 'X9wgSXgS4$!fZ8yf9kPf6FCWF$z6#f*ph*Zva6YPtGXhkRaVa'

class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:converse@localhost/kuaidi'
    SMS_RECEIVE = '您的验证码是：【6699】。请不要把验证码泄露给其他人。'
    SMS_POST = '您的验证码是：【4499】。请不要把验证码泄露给其他人。'

class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:converse@localhost/kuaidi'
    SMS_RECEIVE = '您的验证码是：【6699】。请不要把验证码泄露给其他人。'
    SMS_POST = '您的验证码是：【4499】。请不要把验证码泄露给其他人。'
