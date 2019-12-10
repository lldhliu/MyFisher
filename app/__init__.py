"""
 Created by ldh on 19-11-26
"""
from flask import Flask

__author__ = "ldh"


# Flask 核心对象初始化的相关工作
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.setting')
    app.config.from_object('app.secure')
    register_blueprint(app)
    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
