from flask import Blueprint, current_app

auth = Blueprint('auth', __name__)

# 用户认证
@auth.route('/login')
def login():
    # 程序上下文全局变量。
    print(current_app.config.get('ENV'))
    return {'code':200}

@auth.route('/logout')
def logout():
    return {'code':200}

