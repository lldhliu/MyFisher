"""
 Created by ldh on 19-11-26
"""
__author__ = "ldh"

DEBUG = False

SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:2255@localhost:3306/fisher'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_TRACK_MODIFICATIONS 如果设置成 True (默认情况)，
# Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
# 这需要额外的内存， 如果不必要的可以禁用它。
