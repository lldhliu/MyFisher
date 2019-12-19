"""
 Created by ldh on 19-12-19
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, SmallInteger, Integer

db = SQLAlchemy()


class Base(db.Model):
    # 不想去创建这个表，做法如下
    __abstract__ = True
    status = Column(SmallInteger, default=1)
    # create_time = Column(Integer)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':  # 判断是否拥有 key 属性
                setattr(self, key, value)  # 给 key 属性设置属性值 value
