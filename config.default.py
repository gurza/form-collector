#coding: utf-8
import os


basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'my-secret-secret-key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

APP_REDIRECT_URL = 'https://www.facebook.com'
APP_KICKOUT_COOKIE_NAME = 'kickout_redirect'
