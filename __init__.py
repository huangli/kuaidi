from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:converse@localhost/kuaidi'
app.config['BABEL_DEFAULT_LOCALE'] = 'zh'
db = SQLAlchemy(app)


