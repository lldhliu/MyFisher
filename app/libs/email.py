from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    """
    :param to: 发给谁
    :param subject: 邮件标题
    :param template:
    :param kwargs:
    :return:
    """
    msg = Message('【鱼书】' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)

    app = current_app._get_current_object()  # 获取真实的 app 对象

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

