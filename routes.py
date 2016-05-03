#coding=utf-8
from __init__ import *
from views import *
import sys
from flask import Flask, request, session, g, redirect, url_for,abort, render_template, flash
from flask_admin.model import filters
import flask_admin as admin
from flask.ext.security import SQLAlchemyUserDatastore

@app.errorhandler(404)
def pageNotFound(error):
    return "不好意思，该页面不存在，︿(￣︶￣)︿"

@app.errorhandler(500)
def internal_error(error):
    app.logger.ERROR(error)
    return "服务器出现出错，请联系系统管理员"


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
    if registered_user is not None:
        login_user(registered_user)
        flash(u'登陆成功!')
        return redirect(request.args.get('next') or url_for('admin.index'))
    else:
        error = u'不好意思，密码错误'
        return render_template('login.html', error=error)
    return redirect(url_for('.index'))
    # login.login_user(registered_user)

init_login()
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

if __name__ == '__main__':
    reload(sys)  
    sys.setdefaultencoding('utf8')

    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('kuaidi.log', maxBytes=10000000, backupCount=5)
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    admin = admin.Admin(app, name=u'阳成科技', index_view=MyAdminIndexView(),base_template='my_master.html')
    # admin.locale_selector(get_locale)
    admin.add_view(ReceiptView(Receipt, db.session, u'收快递'))
    admin.add_view(PostView(Post, db.session, u'发快递'))
    admin.add_view(CommunityView(Community, db.session, u'小区'))
    admin.add_view(UserView(User, db.session, u'管理员'))
    admin.add_view(ReceiptReportView(ReceiptReport, db.session, u'收件单报表'))
    admin.add_view(PostReportView(PostReport, db.session, u'发件单报表'))
    # admin.add_view(MyView(name='Hello'))
    app.run(debug=True)

    # app.run(host='0.0.0.0',port=8080)