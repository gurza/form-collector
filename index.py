#!/usr/bin/env python
#coding: utf-8
from flask import Flask, current_app
from flask import Response, render_template, redirect
from flask import request
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask.ext.sqlalchemy import SQLAlchemy
import simplejson
import datetime
import config


app = Flask('index')
app.config.from_object(config)
db = SQLAlchemy(app)


class LoginForm(Form):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class LoginModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=False)
    password = db.Column(db.String(64), index=False, unique=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return '<Login %r:%r>' % (self.login, self.password)


@app.route('/api/v1/ping', methods = ['GET'])
def ping():
    return '', 200


@app.route('/api/v1/logins', methods = ['GET'])
def logins_list():
    logins = LoginModel.query.order_by(db.desc(LoginModel.created_at)).all()

    res = []
    for l in logins:
        res.append({
            'login': l.login,
            'password': l.password,
            'timestamp': l.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return Response(
        simplejson.dumps(res, ensure_ascii=False),
        mimetype = 'application/json'
    )


@app.route('/', methods = ['GET', 'POST'])
def form_ctrl():
    kickout_cookie = config.APP_KICKOUT_COOKIE_NAME
    kickout_url = config.APP_REDIRECT_URL

    if kickout_cookie in request.cookies:
        return redirect(kickout_url)

    error_fl = request.args.get('error', 0)
    try:
        error_fl = int(error_fl)
        error_fl = abs(error_fl)
    except ValueError:
        error_fl = 0

    form = LoginForm()
    if form.validate_on_submit():
        login = LoginModel(
                    login = form.login.data,
                    password = form.password.data
        )
        db.session.add(login)
        db.session.commit()
        if error_fl == 0:
            return redirect('/?error=1')
        else:
            kickout_redirect = redirect(kickout_url)
            response = current_app.make_response(kickout_redirect)
            # Value of cookie doesn't matter
            response.set_cookie(kickout_cookie,value='1',max_age=60*60*24*90)
            return response

    # Show form
    tpl_name = config.APP_TPL_NAME
    title = config.APP_TPL_TITLE
    message = config.APP_TPL_MESSAGE
    action = config.APP_TPL_ACTION
    form.login.data = config.APP_TPL_LOGIN
    return render_template(tpl_name,
        title = title.decode('utf-8'),
        message = message.decode('utf-8'),
        action = action.decode('utf-8'),
        form = form,
        error = error_fl
    )


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
