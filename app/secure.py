"""
 Created by ldh on 19-11-26
"""
__author__ = "刘大怪"


DEBUG = True
SECRET_KEY = 'this is a secret key'

SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:2255@localhost:3306/fisher'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_TRACK_MODIFICATIONS 如果设置成 True (默认情况)，
# Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
# 这需要额外的内存， 如果不必要的可以禁用它。

# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '1151375085@qq.com'
MAIL_PASSWORD = 'hwugclkfxtgdfghj'
# MAIL_SUBJECT_PREFIX = '[鱼书]'
# MAIL_SENDER = '鱼书 <hello@yushu.im>'
