"""
 Created by ldh on 19-12-12
"""
__author__ = "刘大怪"

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


# 图书查询参数校验
class SearchForm(Form):
    # DataRequired 防止用户只传一个空格情况
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)


class DriftForm(Form):
    recipient_name = StringField(validators=[DataRequired(),
                                             Length(min=2, max=20, message='收件人姓名长度必须在2到20个字符之间')])

    mobile = StringField(validators=[DataRequired(),
                                     Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])

    message = StringField()

    address = StringField(validators=[DataRequired(),
                                      Length(min=10, max=70, message='地址还不到10个字吗？尽量写详细一点吧')])
