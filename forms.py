#coding: utf-8
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class LoginForm(Form):
    login = StringField('login', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
