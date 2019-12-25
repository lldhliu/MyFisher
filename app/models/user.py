"""
 Created by ldh on 19-12-19
"""
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float

from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from werkzeug.security import generate_password_hash  # 加密password
from werkzeug.security import check_password_hash  # 密码对比
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from math import floor  # 向下取整  floor(3/2)=1

from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


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

    def can_send_drift(self):
        """
        检查用户是否可以发送鱼漂：
        1.鱼豆是否满足条件
        2. 每索要两本书，必须送出一本书
        :return:
        """
        if self.beans < 1:
            return False
        # 成功送出图书数量
        success_gifts_count = Gift.query.filter_by(uid=self.id,
                                                   launched=True).count()
        # 成功收到书籍数量
        success_recive_count = Drift.query.filter_by(requester_id=self.id,
                                                     pending=PendingStatus.Success).count()
        return True if \
            floor(success_recive_count/2) <= \
            floor(success_gifts_count) else False

    def check_password(self, raw):
        """
        对比数据库保存的加密过的密码与用户输入的明文密码是否一致
        :param raw: 用户输入的明文密码
        :return: True 或者 False
        """
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        """
        判断用户是否可以将图书添加到赠送清单
        :param isbn:
        :return: True 或 False
        """
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 不允许一个用户同时赠送多本相同的图书
        # 判断是否在用户未赠送出去的（launched=False)赠送清单中
        gifting = Gift.query.filter_by(
            uid=self.id, isbn=isbn, launched=False).first()
        # 一个用户不能同时成为同一本书的赠送者和索要者
        # 判断是否在用户正在索要的（launched=False）的心愿清单中
        wishing = Wish.query.filter_by(
            uid=self.id, isbn=isbn, launched=False).first()

        # 既不在赠送清单，也不在心愿清单才能添加
        if not gifting and not wishing:
            return True
        else:
            return False

    # # 告诉 flask_login 需要将用户id存入cookie
    # # flask_login 里面定义的 UserMinxin 已经内置了很多这样的函数
    # # 所以让 User 模型继承 UserMinxin 就可以
    # def get_id(self):
    #     return self.id

    def geneate_token(self, expiration=600):
        """
        用户重置密码时发送重置密码链接的时候需要将用户id加密成token
        生成 token
        :param expiration: 过期时间
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')  # 把 byte decode

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        print(uid)
        with db.auto_commit():
            user = User.query.get(uid)
            if user:
                print(user.email)
                user.password = new_password
            else:
                return False
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


@login_manager.user_loader
# 这个函数是给 flask_login 调用的
# current_user 会返回一个实例化 user 模型
# 这个函数的内部实现 把id号转化成了user模型
def get_user(uid):
    return User.query.get(int(uid))  # 主键可以使用get查询
