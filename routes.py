#coding=utf-8
import sys
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from __init__ import *
from models import *
from flask_admin.contrib.sqla import ModelView
# from flask_admin import admin, BaseView, expose
import flask_admin as admin
from flask_admin import helpers,expose,BaseView
from flask_babelex import Babel
from sms import sendMsg
# import flask_login as login
from flask.ext.login import login_user , logout_user , current_user , login_required
from flask.ext.login import LoginManager
from flask_admin.contrib.sqla.filters import BooleanEqualFilter


app = Flask(__name__)
app.config['SECRET_KEY'] = 'afsdkj12345678'
# Initialize babel
babel = Babel(app)


@babel.localeselector
def get_locale():
    return session.get('lang', 'zh_CN')

# Initialize flask-login
def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)
    # login_manager.login_view = 'login'
    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(int(user_id))


@app.route('/')
def index():
  return render_template('login.html')
  # return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    registered_user = User.query.filter_by(username=username,password=password).first()
    # if registered_user is None:
    #     error = u'不好意思，密码错误'
    #     return render_template('login.html', error=error)
    if registered_user is not None:
        login_user(registered_user)
        flash(u'登陆成功!')
        return redirect(request.args.get('next') or url_for('admin.index'))
    else:
        error = u'不好意思，密码错误'
        return render_template('login.html', error=error)
    return redirect(url_for('.index'))
    # login.login_user(registered_user)

# @app.route('/logout')
# def logout_view(self):
#     login_manager.logout_user()
#     return redirect(url_for('index')) 

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         login_user = User.query.filter_by(name=username).filter_by(password=password).first()

#         if login_user is None:
#             error = u'不好意思，密码错误'
#             print error
#         else:
#             return redirect(url_for('admin/'))
#     return render_template('login.html', error=error)


# 收件单View
class ReceiptView(ModelView):
    column_labels = dict(express_id=u'快递单'
                        ,box_number=u'箱柜号'
                        ,company=u'快递公司'
                        ,phone=u'电话号码'
                        ,name=u'收件人'
                        ,address=u'详细地址'
                        ,delivery_time=u'寄存时间'
                        ,pick_time=u'取件时间'
                        ,is_sign=u'是否取件'
                        )
    # column_filters = (BooleanEqualFilter(column=User.company, name='顺风'),)

    # 导出csv
    can_export = True
    # column_display_pk = True
    can_delete = False
    column_searchable_list = ['phone','delivery_time']
    column_filters = ['company']
    # column_exclude_list = ['community']
    # column_export_exclude_list = ['community']
    # column_editable_list = ['express_id','box_number','phone','name','address','']
    column_hide_backrefs = True
    # form_choices = { 'company': [ ('0', 'Not Showing'), ('1', 'Showing')] }

    # show receipts created by self
    def get_query(self):
        return self.session.query(self.model).filter(self.model.community_id==current_user.community.id)

    @login_required
    def is_accessible(self):
        return current_user.is_authenticated


    def after_model_change(self, form, model, is_created):
         # tablename = form.tablename
        if is_created: # create the table just once
            # sendMsg(model.phone,'您的验证码是：【2499】。请不要把验证码泄露给其他人。') 
            model.community_id = current_user.community.id
            self.session.commit()

# 寄件单View 
class PostView(ModelView):
    column_labels = dict(express_id=u'快递单'
                        ,box_number=u'箱柜号'
                        ,company=u'快递公司'
                        ,phone=u'电话号码'
                        ,name=u'收件人'
                        ,address=u'详细地址'
                        ,send_time=u'发件时间'
                        ,amount=u'金额'
                        ,is_pick=u'是否取件'
                        )
    # 导出csv
    can_export = True
    # column_display_pk = True
    can_delete = False
    column_searchable_list = ['phone']

    @login_required
    def is_accessible(self):
        return current_user.is_authenticated

    # send msg
    # def after_model_change(self, form, model, is_created):
         # tablename = form.tablename
        # if is_created: # create the table just once
            # sendMsg(model.phone,'您的验证码是：【2499】。请不要把验证码泄露给其他人。') 

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('test.html')

# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('login'))

init_login()

if __name__ == '__main__':
    reload(sys)  
    sys.setdefaultencoding('utf8')
    admin = admin.Admin(app, name=u'快件收发', index_view=MyAdminIndexView(),base_template='my_master.html')
    # admin.locale_selector(get_locale)
    admin.add_view(ReceiptView(Receipt, db.session, u'收快递'))
    admin.add_view(PostView(Post, db.session, u'发快递'))
    # admin.add_view(MyView(name='Hello'))
    app.run(debug=True)

    # app.run(host='0.0.0.0',port=8080)