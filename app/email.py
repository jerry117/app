from flask_mail import Message
from app.extensions import mail
from threading import Thread
from flask import current_app

# 不对邮箱进行加密，邮件服务器的端口使用默认的25端口

# def send_mail(subject, to, body):
#     message = Message(subject, recipients=[to], body=body)
#     mail.send(message)

# 异步发送电子邮件


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    app = current_app._get_current_object()
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_async_mail(subject, to, html):
    app = current_app._get_current_object()  # 获取被代理的真实对象
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr

def send_confirm_email(user, token, to=None): # to是为了兼容更新Email的使用场景
    send_mail(subject='Email Confirm', to=to or user.email, template='emails/confirm', user=user, token=token)

def send_reset_password_email(user, token):
    send_mail(subject='Password Reset', to=user.email, template='emails/reset_password', user=user, token=token)