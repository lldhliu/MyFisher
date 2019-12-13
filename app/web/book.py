from flask import jsonify, request

from app.forms.book import SearchForm
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
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == 'isbn':
            result = YuShuBook.search_by_isbn(q)
        else:
            result = YuShuBook.search_by_keyword(q, page)

        return jsonify(result)
        # return json.dumps(result), 200, {'content-type': 'application/json'}
        # jsonify(result) 与 json.dumps(result), 200, {'content-type': 'application/json'}
        # 效果等同
    else:
        return jsonify(form.errors)
