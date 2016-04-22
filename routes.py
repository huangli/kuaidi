#coding=utf-8
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from __init__ import db
from models import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'
# Initialize babel
babel = Babel(app)

@babel.localeselector
def get_locale():
    override = request.args.get('lang')
    if override:
        session['lang'] = override
    return session.get('lang', 'en')


@app.route('/')
def index():
  return render_template('login.html')
  # return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        login_user = User.query.filter_by(name=username).filter_by(password=password).first()

        if login_user is None:
            error = u'不好意思，密码错误'
            print error
        else:
            return redirect(url_for('admin/'))
    return render_template('login.html', error=error)

# 主页面,收快递
@app.route('/home')
def home():
  return render_template('home.html')

# 收件单View
class UserView(ModelView):
    column_labels = dict(express_id=u'快递单'
                        ,box_number=u'箱柜号'
                        ,company=u'快递公司'
                        ,phone=u'电话号码'
                        ,name=u'收件人'
                        ,delivery_time=u'寄存时间'
                        ,pick_time=u'取件时间'
                        ,is_sign=u'是否取件'
                        )
    # 导出csv
    can_export = True
    # column_display_pk = True
    can_delete = False
    column_searchable_list = ['phone']

    def is_accessible(self):
        return True

# 寄件单View 
class PostView(ModelView):
    column_labels = dict(express_id=u'快递单'
                        ,box_number=u'箱柜号'
                        ,company=u'快递公司'
                        ,phone=u'电话号码'
                        ,name=u'收件人'
                        ,send_time=u'发件时间'
                        ,amount=u'金额'
                        ,is_pick=u'是否取件'
                        )
    # 导出csv
    can_export = True
    # column_display_pk = True
    can_delete = False
    column_searchable_list = ['phone']

    def is_accessible(self):
        return True

if __name__ == '__main__':
    admin = Admin(app, name=u'快件收发', template_mode='bootstrap3')
    admin.add_view(UserView(Receipt, db.session, u'收快递'))
    admin.add_view(PostView(Post, db.session, u'发快递'))
    app.run(debug=True)