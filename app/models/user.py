"""
 Created by ldh on 19-12-19
"""
from sqlalchemy import Column, Integer, String, Boolean, Float

from app import login_manager
from app.models.base import Base
from werkzeug.security import generate_password_hash  # 加密password
from werkzeug.security import check_password_hash  # 密码对比
from flask_login import UserMixin

__author__ = "ldh"


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)  # 昵称
    phone_number = Column(String(18), unique=True)  # 电话号码
    email = Column(String(50), unique=True, nullable=False)  # 邮箱
    confirmed = Column(Boolean, default=False)  #
    beans = Column(Float, default=0)  # 鱼豆
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    _password = Column('password', String(128), nullable=False)

    @property  # 属性读取
    def password(self):
        return self._password

    @password.setter  # 属性赋值
    def password(self, raw):
        """
        :param raw: 原始密码
        :return:
        """
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        """
        对比数据库保存的加密过的密码与用户输入的明文密码是否一致
        :param raw: 用户输入的明文密码
        :return: True 或者 False
        """
        return check_password_hash(self._password, raw)

    # # 告诉 flask_login 需要将用户id存入cookie
    # # flask_login 里面定义的 UserMinxin 已经内置了很多这样的函数
    # # 所以让 User 模型继承 UserMinxin 就可以
    # def get_id(self):
    #     return self.id


@login_manager.user_loader
# 这个函数是给 flask_login 调用的
def get_user(uid):
    return User.query.get(int(uid))  # 主键可以使用get查询
