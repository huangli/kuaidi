#coding=utf-8

import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('login.html')
  # return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username', None) == 'admin':
            # error = 'Invalid Credentials. Please try again.'
            return "it works" + request.form.get('password', None)
        else:
            return request.form.get('username', None)
            # return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/home')
def home():
  return 'Home page'

if __name__ == '__main__':
    app.run(debug=True)