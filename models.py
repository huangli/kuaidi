#coding=utf-8
from  __init__ import db

# 系统管理员
class Admin(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(40), unique=True)
  password = db.Column(db.String(20))

  def __init__(self, username, password):
    self.username = username
    self.password = password

  def __repr__(self):
      return '<Admin %r>' % self.username

# 小区管理员
# name: 管理员账号
# pwd:密码
# community_id:小区id
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40))
  password = db.Column(db.String(20))
  # community = db.relationship('Community', backref='Community.name', primaryjoin='User.id==Community.user_id')
  community = db.relationship('Community', backref='Community',uselist=False)

  def __init__(self, name, password):
      self.name = name
      self.password = password

  def __repr__(self):
      return '<User %r>' % self.name

#小区住户
class Inhabitant(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40))
  phone = db.Column(db.String(20))
  born_date = db.Column(db.DateTime)
  interest = db.Column(db.String(80))
  addr = db.Column(db.String(80))

  def __init__(self, name, phone, born_date, interest, addr):
      self.name = name
      self.phone = phone
      self.born_date = born_date
      self.interest = interest
      self.addr = addr

  def __repr__(self):
      return '<Inhabitant %r>' % self.name


# 小区
# name:小区名称
# user_id:外键管理员id
class Community(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __init__(self, name, user_id):
      self.name = name
      self.user_id = user_id

  def __repr__(self):
      return '<Community %r>' % self.name


# 快递收存单
#id: 主键
#express_id: 快递单号
# box_number:箱柜编号
# company：快递公司
# phone：客户电话
# name：客户姓名
# delivery_time:送达时间
# pick_time:取件时间
# community_id: 小区id
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
  community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
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
  community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
  is_pick = db.Column(db.Boolean)

def __init__(self, **kwargs):
    super(Post, self).__init__(**kwargs)
    self.is_pick = False
        # do custom initialization here

def __repr__(self):
    return '<Receipt %r>' % self.id