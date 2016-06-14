# coding=utf-8
import os
from __init__ import *
import unittest

class kuaidiTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:converse@localhost/kuaidi'
        app.config.from_object('config')
        app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
        app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = 'username'

        app.config['TESTING'] = True
        self.app = app.test_client()



    def test_empty_db(self):
        rv = self.app.get('/admin')
        assert '不好意思，您需要登录后才能访问该页面' in rv.data

if __name__ == '__main__':
    unittest.main()
