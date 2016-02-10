#!/usr/bin/env python
#coding: utf-8
from config import SQLALCHEMY_DATABASE_URI
from index import db


if __name__ == '__main__':
    db.create_all()
