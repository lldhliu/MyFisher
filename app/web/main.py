"""
 Created by ldh on 19-12-24
"""
__author__ = "刘大怪"

from flask import render_template
from flask_login import login_required, current_user

from app.models.gift import Gift
from app.view_models.book import BookViewModel
from . import web


@web.route('/')
def index():
    rencent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in rencent_gifts]
    return render_template('index.html', recent=books)


@web.route('/personal')
@login_required
def personal_center():
    return render_template('personal.html', user=current_user.summary)
