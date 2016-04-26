from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:converse@localhost/kuaidi'
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = 'username'
app.config['SECRET_KEY'] = 'afsdkj12345678'
babel = Babel(app)
db = SQLAlchemy(app)


