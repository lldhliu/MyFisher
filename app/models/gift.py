"""
 Created by ldh on 19-12-19
"""
from flask import current_app
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

    # 对象代表一个礼物, 具体
    # 类代表礼物这个事物, 它是抽象, 不是具体的 "一个"
    @classmethod  # 最近的礼物属于礼物这个事物, 不属于具体的某一个礼物, 所以类方法比较合适
    def recent(cls):
        # 只显示一定数量（30）
        # 按照时间倒序排列, 最近的排在最前面
        # 去重, 同一本书籍的礼物不重复出现
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            Gift.create_time).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        # distinct 去重, 但是要实现 distinct 之前必须要先分组
        # 链式调用, 好处: 极大的灵活性
        # 主题 Query
        # 子函数 order_by  group_by limit distinct ...
        # 触发语句 first() all()...
        return recent_gift
