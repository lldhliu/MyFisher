"""
 Created by ldh on 19-11-26
"""
__author__ = "刘大怪"

from flask import Flask
from flask_login import LoginManager  # 用来管理用户登录信息 如 cookie
from app.models.base import db
from flask_mail import Mail


login_manager = LoginManager()
mail = Mail()


# Flask 核心对象初始化的相关工作
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.setting')
    app.config.from_object('app.secure')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'web.login'  # login_required验证用户没登录时引导用户到登录页面
    login_manager.login_message = '请先登录或注册'  # 替换引导到登录界面的提示信息

    mail.init_app(app)

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
