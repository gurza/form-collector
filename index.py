#!/usr/bin/env python
#coding: utf-8
from flask import Flask, render_template
import config
from forms import LoginForm


app = Flask('index')
app.config.from_object(config)


@app.route('/api/v1/ping', methods = ['GET'])
def ping():
    return '', 200


@app.route('/', methods = ['GET'])
def form_ctrl():
    form = LoginForm()
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
