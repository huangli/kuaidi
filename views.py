# coding=utf-8
from models import *
from sms import sendMsg
from __init__ import *
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.view import func
from flask_admin import helpers, expose, BaseView
import flask_admin as admin
from flask_admin.contrib.sqla.filters import BooleanEqualFilter, BaseSQLAFilter, DateBetweenFilter
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask import session, g, redirect, url_for, flash
from wtforms.validators import DataRequired, Length, Regexp
from datetime import datetime, timedelta
from flask_admin.model import typefmt


def date_format(view, value):
    return value.strftime('%Y-%m-%d')

MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({datetime: date_format})


# 收件单View
class ReceiptView(ModelView):
    column_labels = dict(
        express_id=u'快递单',
        box_number=u'箱柜号',
        company=u'快递公司',
        phone=u'电话号码',
        name=u'收件人',
        address=u'详细地址',
        delivery_time=u'寄存时间',
        pick_time=u'取件时间',
        is_sign=u'取件',
        sms_status=u'短信'
    )
    form_args = dict(
        express_id=dict(validators=[DataRequired()]),
        box_number=dict(validators=[DataRequired()]),
        company=dict(validators=[DataRequired()]),
        phone=dict(validators=[
            DataRequired(),
            Regexp(
                regex='^1\d{10}$',
                flags=0,
                message=app.config['PHONE_LENGTH_ERROR']
            )]),
        name=dict(validators=[DataRequired()]),
        delivery_time=dict(
            validators=[DataRequired()],
            format='%Y-%m-%d %H:%M'
        ),
        pick_time=dict(format='%Y-%m-%d %H:%M')
    )

    # datetime format
    form_widget_args = dict(
        delivery_time={'data-date-format': u'YYYY-MM-DD HH:mm'},
        pick_time={'data-date-format': u'YYYY-MM-DD HH:mm'}
    )
    column_type_formatters = MY_DEFAULT_FORMATTERS

    # 最新创建的sort
    column_default_sort = ('delivery_time', True)

    # 导出csv
    can_export = True
    # column_display_pk = True
    can_delete = False
    column_searchable_list = ['phone']
    column_filters = [
        DateBetweenFilter(Receipt.delivery_time, u'寄存时间'),
        'company', 'delivery_time', 'sms_status'
    ]
    form_excluded_columns = ['sms_status']
    # column_exclude_list = ['community']
    # column_export_exclude_list = ['community']
    # column_editable_list = ['express_id','box_number','phone','name','address','']
    # column_hide_backrefs = True
    # form_choices = { 'company': [ ('0', 'Not Showing'), ('1', 'Showing')] }

    def is_accessible(self):
        # return current_user.is_authenticated
        return current_user.has_role('user')

    # show receipts created by self and last 3 months, and not picked yet
    def get_query(self):
        last_90_day = datetime.now() + timedelta(days=-90)
        last_90_receipes = self.session.query(self.model).\
            filter(self.model.community_id == current_user.community.id).\
            filter(self.model.delivery_time >= last_90_day)
        not_pick = self.session.query(self.model).\
            filter(self.model.community_id == current_user.community.id).\
            filter(self.model.is_sign == 0)
        return last_90_receipes.union(not_pick)

    # if there are receipes not picked before 3 month eariler,
    # that would be a mistake
    def get_count_query(self):
        last_90_day = datetime.now() + timedelta(days=-90)
        num_last_90_receipes = self.session.query(func.count('*')).\
            filter(self.model.community_id == current_user.community.id).\
            filter(self.model.delivery_time >= last_90_day)
        return num_last_90_receipes

    def after_model_change(self, form, model, is_created):
        # tablename = form.tablename
        if is_created:  # create the table just once
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
    column_labels = dict(
        express_id=u'快递单',
        box_number=u'箱柜号',
        company=u'快递公司',
        phone=u'电话号码',
        name=u'收件人',
        address=u'详细地址',
        send_time=u'发件时间',
        amount=u'金额(元)',
        weight=u'重量(kg)',
        is_pick=u'寄件',
        sms_status=u'短信'
    )

    form_args = dict(
        express_id=dict(validators=[DataRequired()]),
        box_number=dict(validators=[DataRequired()]),
        company=dict(validators=[DataRequired()]),
        phone=dict(
            validator=[
                DataRequired(),
                Regexp(
                    regex="^1\d{10}$",
                    flags=0,
                    message=app.config['PHONE_LENGTH_ERROR']
                )
            ]
        ),
        name=dict(validators=[DataRequired()]),
        address=dict(validators=[DataRequired()]),
        send_time=dict(validators=[DataRequired()], format='%Y-%m-%d %H:%M'),
        amount=dict(validators=[DataRequired()]),
        weight=dict(validators=[DataRequired()])
    )
    # datetime format
    form_widget_args = dict(
        send_time={'data-date-format': u'YYYY-MM-DD HH:mm'}
    )
    column_type_formatters = MY_DEFAULT_FORMATTERS

    # 最近创建的on top
    column_default_sort = ('send_time', True)

    form_excluded_columns = ['sms_status']
    # form_args = dict(
    #     send_time=dict(format='%Y-%m-%d')
    # )
    # form_widget_args = dict(
    #     send_time={'data-date-format': u'YYYY-MM-DD'}
    # )
    # 导出csv
    can_export = True
    # column_display_pk = True
    can_delete = False
    column_filters = [
        DateBetweenFilter(Post.send_time, u'发件时间'),
        'company', 'send_time', 'sms_status'
    ]
    # column_filters = [ 'company',]
    column_searchable_list = ['phone']
    form_excluded_columns = ['sms_status']

    # show receipts created by self
    def get_query(self):
        last_90_day = datetime.now() + timedelta(days=-90)
        last_90_post = self.session.query(self.model).\
            filter(self.model.community_id == current_user.community.id).\
            filter(self.model.send_time >= last_90_day)
        return last_90_post

    def get_count_query(self):
        last_90_day = datetime.now() + timedelta(days=-90)
        num_last_90_post = self.session.query(func.count('*')).\
            filter(self.model.community_id == current_user.community.id).\
            filter(self.model.send_time >= last_90_day)
        return num_last_90_post

    def is_accessible(self):
        # return current_user.is_authenticated
        return current_user.has_role('user')

    # send msg
    def after_model_change(self, form, model, is_created):
        if is_created:  # create the table just once
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
    column_labels = dict(
        username=u'小区管理员',
        password=u'密码',
        community=u'小区'
    )
    # column_display_pk = True
    can_delete = True
    form_excluded_columns = ('roles')
    column_hide_backrefs = True
    # column_searchable_list = ['phone']

    def is_accessible(self):
        # return current_user.is_authenticated
        # if not current_user.is_authenticated(): return False
        return current_user.has_role('admin')

    def get_query(self):
        return self.session.query(self.model).filter(self.model.username != 'admin')

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.username != 'admin')

    def after_model_change(self, form, model, is_created):
        if is_created:
            # add user role
            end_user = self.session.query(Role).filter_by(name='user').first()
            model.roles.append(end_user)
            self.session.commit()


# 小区管理
class CommunityView(ModelView):
    column_list = ['name']
    column_labels = dict(name=u'小区名称')
    column_searchable_list = ['name']
    form_columns = ['name']

    def is_accessible(self):
        return current_user.has_role('admin')


# 小区快递月度报表
class ReceiptReportView(ModelView):
    column_labels = dict(
        community_name=u'小区名称',
        company=u'快递公司',
        my_month=u'年-月',
        count=u'收件数量'
    )
    can_export = True
    can_delete = False
    can_edit = False
    can_create = False
    column_searchable_list = ['community_name', 'company', 'my_month']

    def is_accessible(self):
        return current_user.has_role('admin')


# 小区快递月度发件报表
class PostReportView(ModelView):
    column_labels = dict(
        community_name=u'小区名称',
        company=u'快递公司',
        my_month=u'年-月',
        count=u'发件数量',
        weight=u'重量(kg)',
        amount=u'金额(元)'
    )
    can_export = True
    can_delete = False
    can_edit = False
    can_create = False
    column_searchable_list = ['community_name', 'company', 'my_month']

    def is_accessible(self):
        return current_user.has_role('admin')


# 未收快递报表
class NotReceiveReportView(ModelView):
    column_labels = dict(
        community_name=u'小区名称',
        company=u'快递公司',
        my_month=u'年-月',
        count=u'未收快递数量'
    )
    can_export = True
    can_delete = False
    can_edit = False
    can_create = False
    column_searchable_list = ['community_name', 'company', 'my_month']

    def is_accessible(self):
        return current_user.has_role('admin')


# logout
class MyAdminIndexView(admin.AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('login'))
