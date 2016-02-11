#coding: utf-8
import os


CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

APP_REDIRECT_URL = os.environ.get('APP_REDIRECT_URL')
APP_KICKOUT_COOKIE_NAME = 'kickout_redirect'

APP_TPL_NAME = os.environ.get('APP_TPL_NAME')
APP_TPL_LOGIN = os.environ.get('APP_TPL_LOGIN')
APP_TPL_TITLE = os.environ.get('APP_TPL_TITLE')
APP_TPL_MESSAGE = os.environ.get('APP_TPL_MESSAGE')
APP_TPL_ACTION = os.environ.get('APP_TPL_ACTION')
