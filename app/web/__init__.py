"""
 Created by ldh on 19-12-24
"""
__author__ = "刘大怪"

from flask import Blueprint, render_template

# web 蓝图的相关初始化工作
# 蓝图 blueprint

web = Blueprint('web', __name__)


@web.app_errorhandler(404)
def not_found(e):
    # AOP 思想: 面向切片编程
    return render_template('404.html'), 404


from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import wish
from app.web import main
# from app.web import test
