from flask import jsonify, Blueprint, request
import json

from app.web import web
from helper import is_isbn_or_key
from yushu_book import YuShuBook


@web.route('/book/search')
def search():
    """
    :param q: 图书名称或者图书的 isbn
    :param page: 显示page
    :return:
    ?q=金庸&page=1
    """
    # request.args 返回的是一个不可变字典，要转为普通字典使用：
    # request.args.to_dict()
    q = request.args['q']
    # q至少要有一个字符，也要有长度限制
    page = request.args['page']
    # page必须是正整数，也要有一个最大值的限制
    isbn_or_key = is_isbn_or_key(q)
    if isbn_or_key == 'isbn':
        result = YuShuBook.search_by_isbn(q)
    else:
        result = YuShuBook.search_by_keyword(q)

    return jsonify(result)
    # return json.dumps(result), 200, {'content-type': 'application/json'}
    # jsonify(result) 与 json.dumps(result), 200, {'content-type': 'application/json'}
    # 效果等同
