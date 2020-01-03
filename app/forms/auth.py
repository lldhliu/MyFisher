"""
 Created by ldh on 19-12-12
"""
__author__ = "刘大怪"

from wtforms import Form, StringField, IntegerField, PasswordField, ValidationError
from wtforms.validators import Length, NumberRange, DataRequired, Email, EqualTo

from app.models.user import User


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email('电子邮箱不符合规范')])


# 注册表单校验
class RegisterForm(EmailForm):
    password = PasswordField(validators=[DataRequired(message='密码不可以为空, 请输入你的密码'), Length(6, 32)])

    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少需要2个字符, 最多10个字符')])

    # 函数名字 validate 后面跟上 email, wtforms 就会知道是在对 email 做校验
    def validate_email(self, field):
        """
        判断数据库有没有重复email
        :param field: 用户输入的email
        :return:
        """
        # filter_by 类似于 查询语句的 where
        if User.query.filter_by(email=field.data).first():  # .first() 是触发语句，只有触发语句才开始执行查询
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field).first():
            raise ValidationError('昵称已存在')


class LoginForm(EmailForm):
    password = PasswordField(validators=[DataRequired(message='密码不可以为空, 请输入你的密码'), Length(6, 32)])


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[DataRequired(),
                                          Length(6, 32, message='密码长度至少需要在6到32个字符之间'),
                                          EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField(validators=[DataRequired(),
                                          Length(6, 32)])


class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[DataRequired(message='原密码不可以为空, 请输入你的密码'), Length(6, 32)])
    new_password1 = PasswordField(validators=[DataRequired(message='新密码不可以为空, 请输入你的密码'),
                                              Length(6, 32, message='密码长度至少需要在6到32个字符之间'),
                                              EqualTo('new_password2', message='两次输入的密码不相同')])
    new_password2 = PasswordField(validators=[DataRequired(), Length(6, 32)])
