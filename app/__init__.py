"""
 Created by ldh on 19-11-26
"""
from flask import Flask

from app.models.book import db

__author__ = "ldh"


# Flask 核心对象初始化的相关工作
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.setting')
    app.config.from_object('app.secure')
    register_blueprint(app)

    db.init_app(app)

    # db.create_all()
    # 上面这样写会报错： RuntimeError: No application found.
    # Either work inside a view function or push an application
    # 方案一： 将app核心对象作为关键字参数传入 db.create_all(app=app)

    with app.app_context():
        db.create_all()

    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
