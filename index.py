#!/usr/bin/env python
#coding: utf-8
from flask import Flask, Response, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import simplejson
import config
from forms import LoginForm


app = Flask('index')
app.config.from_object(config)
db = SQLAlchemy(app)


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=False)
    password = db.Column(db.String(64), index=False, unique=False)

    def __repr__(self):
        return '<Login %r:%r>' % (self.login, self.password)


@app.route('/api/v1/ping', methods = ['GET'])
def ping():
    return '', 200


def jsonify(hash):

    res = simplejson.dumps(hash, ensure_ascii=False)


@app.route('/api/v1/logins', methods = ['GET'])
def logins_list():
    logins = Login.query.all()

    res = []
    for l in logins:
        res.append({
            'login': l.login,
            'password': l.password,
        })

    return Response(
        simplejson.dumps(res, ensure_ascii=False),
        mimetype = 'application/json'
    )


@app.route('/', methods = ['GET', 'POST'])
def form_ctrl():
    form = LoginForm()
    if form.validate_on_submit():
        print form.login.data
        print form.password.data
        login = Login(
                    login = form.login.data,
                    password = form.password.data
        )
        db.session.add(login)
        db.session.commit()
        return redirect('/')
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
