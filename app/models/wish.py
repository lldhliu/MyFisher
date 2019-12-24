"""
 Created by ldh on 19-12-20
"""
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
# from app.models.gift import Gift
from app.spider.yushu_book import YuShuBook

__author__ = "ldh"


class Wish(Base):
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

    # 查询用户的所有礼物
    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    # 查询用户所有心愿对应的想送的人的数量
    @classmethod
    def get_gift_counts(cls, isbn_list):
        """
        根据传入的一组 isbn, 到 Wish 表中计算出某个礼物的 Wish 心愿数量
        :param isbn_list:
        :return:
        """
        # 跨表查询 db.session 方式更好
        from app.models.gift import Gift  # 放在上面会导致循环导入
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(Gift.launched == 'False',
                                                                             Gift.isbn.in_(isbn_list),
                                                                             Gift.status == 1).group_by(
            Gift.isbn).all()
        # count_list 是一组包含元祖的列表, 不适合直接返回
        # 适合返回的对象： 1. 对象  2. 字典
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
