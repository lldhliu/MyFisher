"""
 Created by ldh on 19-12-20
"""
__author__ = "刘大怪"

from flask import make_response, session

from app.web import web


@web.route('/set/cookie')
def set_cookie():
    response = make_response('Hello 刘大怪')
    response.set_cookie('name', '刘大怪', 100)
    return response


@web.route('/set/session')
def set_session():
    session['t'] = 1
    return 'over'


@web.route('/get/session')
def get_session():
    return str(session['t'])
