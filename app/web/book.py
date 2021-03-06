"""
 Created by ldh on 19-12-24
"""
__author__ = "刘大怪"

import json

from flask import jsonify, request, flash, render_template
from flask_login import current_user

from app.forms.book import SearchForm
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo
from app.web import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook


# 测试flask线程隔离
# @web.route('/test')
# def test():
#     from flask import request
#     from app.libs.none_local import n
#     print(n.v)
#     n.v = 2
#     print('----------------------')
#     print(getattr(request, 'v', None))
#     setattr(request, 'v', 2)
#     # print(getattr(request, 'v', None))
#     print('------------------')
#     return ''


@web.route('/book/search')
def search():
    """
    :param q: 图书名称或者图书的 isbn
    :param page: 显示page
    :return:
    ?q=金庸&page=1
    """
    # 方法一：
    # # request.args 返回的是一个不可变字典，要转为普通字典使用：
    # # request.args.to_dict()
    # q = request.args['q']
    # # q至少要有一个字符，也要有长度限制
    # page = request.args['page']
    # # page必须是正整数，也要有一个最大值的限制
    # 然后加入自己逻辑对 q, page 进行校验

    # 方法二：
    form = SearchForm(request.args)  # 验证器验证成功返回 True, 失败返回 False
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # books 是一个对象，无法序列化
        """
        return jsonify(books)
        return json.dumps(result), 200, {'content-type': 'application/json'}
        jsonify(result) 与 json.dumps(result), 200, {'content-type': 'application/json'}
        效果等同
        """
        # return json.dumps(books, default=lambda o: o.__dict__)

    else:
        # return jsonify(form.errors)
        flash('搜索的关键字不符合要求，请重新输入关键字！')
    return render_template('search_result.html', books=books, form=form)


# 书籍详情页面
@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:  # 如果用户登录 True 否则 False
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()  # 查询所有赠送者的信息
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()  # 查询所有索要者的信息

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template('book_detail.html',
                           book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_wishes=has_in_wishes,
                           has_in_gifts=has_in_gifts)
