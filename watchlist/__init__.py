import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_mail import Mail

# SQLite不支持ALTER语 句，而这正是迁移工具依赖的工作机制。

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__, static_url_path='/static')
# 配置的名称必须是全部大写形式，小写的变量将不会被读取。
# 使用update（）方法可以一次加载多个值。
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False #来设置是否开启CSRF保护 Flask- WTF会自动在实例化表单类时添加一个包含CSRF令牌值的隐藏字段，字段名为 csrf_token。
app.config['WTF_I18N_ENABLED'] = False #设置内置错误消息语言为中文
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024 #最大长度限制为3M
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')

# 邮箱的配置
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('jerry', os.getenv('MAIL_USERNAME'))

db = SQLAlchemy(app)
migrate = Migrate(app, db) # 在db对象创建后调用
ckeditor = CKEditor(app)
login_manager = LoginManager(app) #实例化扩展类
mail = Mail(app)

@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User # 用 ID 作为 User 模型的 主键查询对应的用户
    user = User.query.get(int(user_id))
    return user # 返回用户对象


login_manager.login_view = 'login' #和@login_required搭配使用，为了让这个重定向操作正确执行，设为我们程序的登录视图端点（函数名）
# login_manager.login_message = 'Your custom message'

# 对于多个模板内都需要使用的变量，我们可以使用 app.context_processor 装饰器注册一个模板上下文处理函数
@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)

# 注册shell上下文处理函数
# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, Note=Note) #等同于{'db': db, 'Note': Note}

from watchlist import views, errors, commands, database
from watchlist.form.forms import LoginForm
