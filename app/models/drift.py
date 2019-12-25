"""
 Created by ldh on 19-12-25
"""
from sqlalchemy import Column, Integer, String, SmallInteger

from app.models.base import Base

__author__ = "ldh"


class Drift(Base):
    """
    一次具体的交易信息
    """
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)  # 收件人姓名
    address = Column(String(100), nullable=False)  # 收件人地址
    message = Column(String(200))  # 附带消息
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)  # 请求人id
    gift_id = Column(Integer)  # 交易对应礼物的id
    gifter_nickname = Column(String(20))

    # 鱼漂状态 （等待、成功、拒绝、撤销）
    pending = Column('pending', SmallInteger, default=1)
