# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
# from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager


# 扩展类实例化
db = SQLAlchemy()
# moment = Moment()
ckeditor = CKEditor()
mail = Mail()
toolbar = DebugToolbarExtension()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models.models import Admin
    user = Admin.query.get(int(user_id))
    return user

login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

