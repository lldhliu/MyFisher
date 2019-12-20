from flask import Blueprint

# web 蓝图的相关初始化工作
# 蓝图 blueprint

web = Blueprint('web', __name__)

from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import wish
from app.web import main
from app.web import test
