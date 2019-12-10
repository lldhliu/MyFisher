from flask import Blueprint

# web 蓝图的相关初始化工作
# 蓝图 blueprint

web = Blueprint('web', __name__)

from app.web import book
