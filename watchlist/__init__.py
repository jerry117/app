import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app) #实例化扩展类


@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User # 用 ID 作为 User 模型的 主键查询对应的用户
    user = User.query.get(int(user_id))
    return user # 返回用户对象


login_manager.login_view = 'login' #和@login_required搭配使用，为了让这个重定向操作正确执行，设为我们程序的登录视图端点（函数名）
# login_manager.login_message = 'Your custom message'

# 对于多个模板内都需要使用的变量，我们可以使用 app.context_processor 装 饰器注册一个模板上下文处理函数
@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


from watchlist import views, errors, commands
