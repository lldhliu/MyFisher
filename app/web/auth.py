from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user  # 可以保存用户的票据信息的库
from app.forms.auth import RegisterForm, LoginForm
from app.models.base import db
from app.models.user import User
from app.web import web

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)  # form.data 包含客户端提交过来的所有参数
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 将用户信息写入cookie, 需要在用户模型内部定义一个函数(get_id)来告诉login_user是将用户那些信息存入cookie, 比如用户id
            # 使用 login_user 存储的是一次性 cookie, 在整个浏览器关闭后 cookie 会消失
            # 如果设置参数 remember=True, 就会变成一定时间内持续性的 cookie, 默认记住时间是 365 天
            # 如果需要更改默认时间, 需要在 flask 配置文件中加入配置项 REMEMBER_COOKIE_DURATION
            # REMEMBER_COOKIE_DURATION: cookie 过期时间, 为一个 `datetime.timedelta` 对象
            login_user(user, remember=True)
            # 用户登录后跳转到哪
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                # not next.startswith('/') 防止重定向攻击 http://localhost:3333/login?next=http://www.baidu.com
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    pass
