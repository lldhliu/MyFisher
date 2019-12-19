"""
 Created by ldh on 19-12-19
"""
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models.base import Base

__author__ = "ldh"


class Gift(Base):
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)  # 书是否被送出

    # 与 user 的关系
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))

    # # 与 book 的关系, 但由于数据库没对 book 数据进行保存, book 数据是调用 api 得到的, 所以不需要这样
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    # 这里使用 book 对应的唯一 isbn 进行关联
    isbn = Column(String(15), nullable=False)  # 图书编号
