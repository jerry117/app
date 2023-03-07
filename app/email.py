from flask_mail import Message
from app import mail, app
from threading import Thread

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
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr