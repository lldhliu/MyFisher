"""
 Created by ldh on 19-12-19
"""
from wtforms import Form, StringField, IntegerField, PasswordField, ValidationError
from wtforms.validators import Length, NumberRange, DataRequired, Email

from app.models.user import User

__author__ = "ldh"


# 注册表单校验
class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])

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


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email('电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不可以为空, 请输入你的密码'), Length(6, 32)])

