from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db


# ORM主要实现了三层映射关 系：
# 表→Python类。
# 字段（列）→类属性。 
# 记录（行）→类实例。


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20)) #用户名
    password_hash = db.Column(db.String(128)) #密码散列值

    def set_password(self, password): #用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password) #将生成的密码保持到对应字段

    def validate_password(self, password): #用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password) #返回布尔值


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

class Contact(db.Model):
    __tablename__ = 'contacts'
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(32))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    