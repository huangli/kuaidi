#coding=utf-8
import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from __init__ import db
from models import *

app = Flask(__name__)

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
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# 主页面
@app.route('/home')
def home():
  return 'Home page'

if __name__ == '__main__':
    app.run(debug=True)