from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, AnonymousUserMixin
from flask_wtf.csrf import CSRFProtect
from flask_dropzone import Dropzone
from flask_whooshee import Whooshee
from flask_avatars import Avatars


# 扩展类实例化
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
toolbar = DebugToolbarExtension()
login_manager = LoginManager()
csrf = CSRFProtect()
dropzone = Dropzone()
bootstrap = Bootstrap4()
whooshee = Whooshee()
avatars = Avatars()

@login_manager.user_loader
def load_user(user_id):
    from app.models.models import Admin
    user = Admin.query.get(int(user_id))
    return user

login_manager.login_view = 'auth.login'
login_manager.login_message = 'first login'
login_manager.login_message_category = 'warning'

class Guest(AnonymousUserMixin):

    def can(self, permission_name):
        return False

    @property
    def is_admin(self):
        return False
    
login_manager.anonymous_user = Guest