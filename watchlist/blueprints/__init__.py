import os
from flask import Flask, render_template
from watchlist.setting import config
from watchlist.blueprints.auth import auth
from watchlist.extensions import db, mail, ckeditor

# 工厂函数 按照惯例，这个函数被命名为 create_app（）或make_app（）。我们把这个工厂函数称为程序工厂
def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_logging(app) #注册日志处理器
    register_extensions(app) #注册扩展（扩展初始化）
    register_blueprint(app) #注册蓝本
    register_commands(app)  #注册自定义shell命令
    register_errors(app) #注册错误处理函数
    register_shell_context(app) #注册shell上下文处理函数
    register_template_context(app) #注册模版上下文处理函数
    return app



def register_logging(app):
    pass # 后续补充

def register_extensions(app):
    # bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    
def register_blueprint(app):
    # app.register_blueprint(blog)
    # app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)
    

def register_template_context(app):
    pass

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400
    
def register_commands(app):
    pass