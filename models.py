#coding=utf-8
from  __init__ import db
from flask.ext.security import SQLAlchemyUserDatastore,UserMixin, RoleMixin, login_required


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE')))


# Role class
class Role(db.Model, RoleMixin):
    # Our Role has three fields, ID, name and description
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(100))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)

# 小区管理员
# username: 管理员账号
# password:密码
# community_id:小区id
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(20))
    # community = db.relationship('Community', backref='Community.name', primaryjoin='User.id==Community.user_id')
    community = db.relationship('Community', backref='Community',uselist=False)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, **kwargs):
      super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.username

  # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

  # Required for administrative interface
    def __unicode__(self):
        return self.username

#小区住户
class Inhabitant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    phone = db.Column(db.String(20))
    born_date = db.Column(db.DateTime)
    interest = db.Column(db.String(80))
    addr = db.Column(db.String(80))

    def __init__(self, **kwargs):
        super(Inhabitant, self).__init__(**kwargs)


    def __repr__(self):
        return '<Inhabitant %r>' % self.name


# 小区
# name:小区名称
# user_id:外键管理员id
class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super(Community, self).__init__(**kwargs)

    def __repr__(self):
        return '%s' % self.name


# 快递收存单
#id: 主键
#id: 快递单号
# box_number:箱柜编号
# company：快递公司
# phone：客户电话
# name：客户姓名
# delivery_time:送达时间
# pick_time:取件时间
# community_id: 小区id
# address: 详细地址
# is_sign:是否签收0未签，1已经签收
class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    express_id = db.Column(db.String(60), index=True)
    box_number = db.Column(db.String(20)) 
    company = db.Column(db.String(40))
    phone = db.Column(db.String(20),index=True)
    name = db.Column(db.String(40))
    delivery_time = db.Column(db.DateTime,index=True)
    pick_time = db.Column(db.DateTime)
    address = db.Column(db.String(40))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    # community = db.relationship('Community', backref='Receipt')
    is_sign = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.is_sign = False

    def __repr__(self):
        return '<Receipt %r>' % self.id

# 快递发件单
# id:主键
#express_id: 快递单号
# company:快递公司
# name：客户姓名
# phone：客户电话
# send_time:寄件时间
# amount: 金额
# address:详细地址
# community_id: 小区id
# is_pick: 0快递员未取件，1快递员已经取件
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    express_id = db.Column(db.String(60),index=True)
    company = db.Column(db.String(40))
    phone = db.Column(db.String(20), index=True)
    name = db.Column(db.String(40))
    send_time = db.Column(db.DateTime, index=True)
    amount = db.Column(db.Float)
    address = db.Column(db.String(40))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    is_pick = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
        self.is_pick = False
        # do custom initialization here

    def __repr__(self):
        return '<Receipt %r>' % self.id

# 小区快递月度报表
class ReceiptReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_name = db.Column(db.String(30))
    company = db.Column(db.String(40)) 
    count = db.Column(db.Integer)
    my_month = db.Column(db.String(20))

    def __init__(self, **kwargs):
        super(Receipt_Report, self).__init__(**kwargs)

    def __repr__(self):
        return '<Report %r>' % self.id
