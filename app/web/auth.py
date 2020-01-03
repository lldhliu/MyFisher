"""
 Created by ldh on 19-12-24
"""
__author__ = "刘大怪"

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user  # 可以保存用户的票据信息的库
from flask_login import logout_user
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm, ChangePasswordForm
from app.libs.email import send_mail
from app.models.base import db

from app.models.user import User

from app.web import web


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)  # form.data 包含客户端提交过来的所有参数
            db.session.add(user)

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
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        account_email = form.email.data
        user = User.query.filter_by(email=account_email).first_or_404()

        send_mail(form.email.data,
                  '重置你的密码',
                  'email/reset_password.html',
                  user=user,
                  token=user.geneate_token())
        flash('一封邮件已发送到邮箱' + account_email + ', 请及时查收')

    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        print(success)
        if success:
            flash('你的密码已更新, 请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if form.old_password.data == form.new_password1.data:
        flash('新密码与旧密码一致, 请确认后重新输入')
    else:
        if request.method == 'POST' and form.validate():
            success = current_user.check_password(form.old_password.data)
            if success:
                with db.auto_commit():
                    current_user.password = form.new_password1.data
                flash('你的密码已修改, 请使用新密码登录')
                return redirect(url_for('web.login'))
            else:
                flash('原密码输入有误')
    return render_template('auth/change_password.html', form=form)


@web.route('/logout')
def logout():
    logout_user()  # 其实就是清空了浏览器里面的 cookie
    return redirect(url_for('web.index'))
