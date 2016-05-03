#coding=utf-8
from models import *
from sms import sendMsg
from __init__ import *
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.view import func
from flask_admin import helpers,expose,BaseView
import flask_admin as admin
from flask_admin.contrib.sqla.filters import BooleanEqualFilter,BaseSQLAFilter,DateBetweenFilter
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask import  session, g, redirect, url_for, flash

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
                        ,is_sign=u'取件'
                        ,sms_status=u'短信'
                        )

    # 导出csv
    can_export = True
    # column_display_pk = True
    can_delete = False
    column_searchable_list = ['phone']
    column_filters = [ DateBetweenFilter( Receipt.delivery_time,u'寄存时间'), \
                    'company', 'delivery_time', 'sms_status']
    form_excluded_columns = ['sms_status']
    # column_exclude_list = ['community']
    # column_export_exclude_list = ['community']
    # column_editable_list = ['express_id','box_number','phone','name','address','']
    # column_hide_backrefs = True
    # form_choices = { 'company': [ ('0', 'Not Showing'), ('1', 'Showing')] }

    # show receipts created by self
    def get_query(self):
        return self.session.query(self.model).filter(self.model.community_id==current_user.community.id)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.community_id==current_user.community.id)


    @login_required
    def is_accessible(self):
        # return current_user.is_authenticated
        return current_user.has_role('user')


    def after_model_change(self, form, model, is_created):
         # tablename = form.tablename
        if is_created: # create the table just once
            sms = sendMsg(model.phone, app.config['SMS_RECEIVE']) 
            if (sms == '2'):
                model.sms_status = 1
                flash(u'短信发送成功')
            else:
                model.sms_status = 0
                flash(u'短信发送失败，请检查手机号码是否正确')
                app.logger.error(model.phone + app.config['SMS_SEND_ERROR'])
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
                        ,amount=u'金额(元)'
                        ,weight=u'重量(kg)'
                        ,is_pick=u'取件'
                        ,sms_status=u'短信'
                        )
    form_excluded_columns = ['sms_status']
    form_args = dict(
        send_time=dict(format='%Y-%m-%d') 
    )
    form_widget_args = dict(
        send_time={'data-date-format': u'YYYY-MM-DD'} 
    )
    # 导出csv
    can_export = True
    # column_display_pk = True
    can_delete = False
    column_filters = [ DateBetweenFilter( Post.send_time,u'发件时间'),\
                     'company','send_time', 'sms_status']
    # column_filters = [ 'company',]
    column_searchable_list = ['phone']
    form_excluded_columns = ['sms_status']

    # show receipts created by self
    def get_query(self):
        return self.session.query(self.model).\
                filter(self.model.community_id==current_user.community.id)

    def get_count_query(self):
        return self.session.query(func.count('*')).\
                filter(self.model.community_id==current_user.community.id)

    @login_required
    def is_accessible(self):
        # return current_user.is_authenticated
        return current_user.has_role('user')

    # send msg
    def after_model_change(self, form, model, is_created):
        if is_created: # create the table just once
            model.community_id = current_user.community.id
        if model.is_pick == 1 and model.sms_status != 1:
            sms = sendMsg(model.phone, app.config['SMS_POST'])
            if (sms == '2'):
                model.sms_status = 1
                flash(u'短信发送成功')
            else:
                model.sms_status = 0
                flash(u'短信发送失败，请检查手机号码是否正确')
                app.logger.error(model.phone + app.config['SMS_SEND_ERROR'])
        self.session.commit()



# 用户管理
class UserView(ModelView):
    column_labels = dict(username=u'小区管理员'
                        ,password=u'密码'
                        ,community=u'小区'
                        )
    # column_display_pk = True
    can_delete = True
    form_excluded_columns = ('roles')
    # column_searchable_list = ['phone']

    @login_required
    def is_accessible(self):
        # return current_user.is_authenticated
        return current_user.has_role('admin')

    def get_query(self):
        return self.session.query(self.model).filter(self.model.username!='admin')

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.username!='admin')

    def after_model_change(self, form, model, is_created):
        if is_created: 
            # add user role
            end_user = self.session.query(Role).filter_by(name='user').first()
            model.roles.append(end_user)
            self.session.commit()
# 小区管理
class CommunityView(ModelView):
    column_list = ['name']
    column_labels = dict(name = u'小区名称')
    column_searchable_list = ['name']
    form_columns = ['name']

    @login_required
    def is_accessible(self):
        return current_user.has_role('admin')

# 小区快递月度报表
class ReceiptReportView(ModelView):
    column_labels = dict(
                        community_name = u'小区名称'
                        ,company = u'快递公司'
                        ,my_month = u'年-月'
                        ,count = u'收件数量'
                        )
    can_export = True
    can_delete = False
    can_edit = False
    can_create = False
    column_searchable_list = ['community_name', 'company', 'my_month']
    @login_required
    def is_accessible(self):
        return current_user.has_role('admin')

# 小区快递月度发件报表
class PostReportView(ModelView):
    column_labels = dict(
                        community_name = u'小区名称'
                        ,company = u'快递公司'
                        ,my_month = u'年-月'
                        ,count = u'发件数量'
                        ,weight = u'重量(kg)'
                        ,amount = u'金额(元)'
                        )
    can_export = True
    can_delete = False
    can_edit = False
    can_create = False
    column_searchable_list = ['community_name', 'company', 'my_month']
    @login_required
    def is_accessible(self):
        return current_user.has_role('admin')

# 未收快递报表
class NotReceiveReportView(ModelView):
    column_labels = dict(
                        community_name = u'小区名称'
                        ,company = u'快递公司'
                        ,my_month = u'年-月'
                        ,count = u'未收快递数量'
                        )
    can_export = True
    can_delete = False
    can_edit = False
    can_create = False
    column_searchable_list = ['community_name', 'company', 'my_month']
    @login_required
    def is_accessible(self):
        return current_user.has_role('admin')

# logout
class MyAdminIndexView(admin.AdminIndexView):
    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('login'))
