from flask import jsonify, Blueprint
import json
from helper import is_isbn_or_key
from yushu_book import YuShuBook

# 蓝图 blueprint
web = Blueprint('web', __name__)


@web.route('/book/search/<q>/<page>')
def search(q, page):
    """
    :param q: 图书名称或者图书的 isbn
    :param page: 显示page
    :return:
    """

    isbn_or_key = is_isbn_or_key(q)
    if isbn_or_key == 'isbn':
        result = YuShuBook.search_by_isbn(q)
    else:
        result = YuShuBook.search_by_keyword(q)

    return jsonify(result)
    # return json.dumps(result), 200, {'content-type': 'application/json'}
    # jsonify(result) 与 json.dumps(result), 200, {'content-type': 'application/json'}
    # 效果等同
