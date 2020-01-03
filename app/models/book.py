"""
 Created by ldh on 19-12-12
"""
__author__ = "刘大怪"

from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)  # 书名
    author = Column(String(30), default='未名')  # 作者
    binding = Column(String(20))  # 装帧版本：精装, 平装
    publisher = Column(String(50))  # 出版社
    price = Column(String(20))  # 价格
    pages = Column(Integer)  # 页数
    pubdate = Column(String(20))  # 出版日期
    isbn = Column(String(15), nullable=False, unique=True)  # 图书编号
    summary = Column(String(1000))  # 图书简介
    image = Column(String(50))  # 图片

    def sample(self):
        pass
