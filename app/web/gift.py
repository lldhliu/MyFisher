from flask import current_app, flash, redirect, url_for
from flask_login import login_required  # 判断用户是否登录的插件
from flask_login import current_user

from app.models.base import db
from app.models.gift import Gift
from . import web
__author__ = '七月'


@web.route('/my/gifts')
@login_required  # 必须要用户登录
def my_gifts():
    return 'My Gifts'


@web.route('/gifts/book/<isbn>')
@login_required  # 必须要登录
def save_to_gifts(isbn):  # 赠送此书
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id

            # current_user 是实例化了的 user 模型
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']

            db.session.add(gift)

    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单, 请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
