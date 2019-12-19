"""
 Created by ldh on 19-12-19
"""
from sqlalchemy import Column, Integer, String, Boolean, Float

from app.models.base import Base
from werkzeug.security import generate_password_hash  # 加密password

__author__ = "ldh"


class User(Base):
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

    _password = Column('password', String(64))

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
