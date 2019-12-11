"""
 Created by ldh on 19-12-11
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired

__author__ = "ldh"


class SearchForm(Form):
    # DataRequired 防止用户只传一个空格情况
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
