"""
 Created by ldh on 19-12-24
"""
__author__ = "刘大怪"

from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required  # 判断用户是否登录的插件
from flask_login import current_user

from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.gift import MyGifts
from . import web


@web.route('/my/gifts')
@login_required  # 必须要用户登录
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyGifts(gifts_of_mine, wish_count_list)

    return render_template('my_gifts.html', gifts=view_model.gifts)


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
@login_required
def redraw_from_gifts(gid):
    """
    赠送清单撤销操作
    :param gid: gift id
    :return:
    """
    # 查询出对应 gift
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    # 查询当前要撤销礼物是否处于等待邮寄的状态
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态, 请先前往鱼漂完成该交易')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
