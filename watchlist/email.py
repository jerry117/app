from flask_mail import Message
from watchlist import mail, app

# ssl/tls加密
MAIL_USE_SSL = True
MAIL_PORT = 465

# starttls加密
MAIL_USE_TLS = True
MAIL_PORT = 587

# 不对邮箱进行加密，邮件服务器的端口使用默认的25端口

def send_mail(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)

@app.route('/email')
def email():
    send_mail('hello','xxx@qq.com','world')
    return {'code':200}