from flask import Blueprint, current_app, redirect, url_for, flash, render_template
from flask_login import login_user, current_user, logout_user, login_required
from app.models.models import Admin
from app.form.forms import LoginForm
from app.utils import redirect_back

auth = Blueprint('auth', __name__)

# 用户认证
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # 程序上下文全局变量。
    if current_user.is_authenticated:
        # print(current_app.config.get('ENV'))
        return redirect(url_for('blog.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            # 验证用户名和密码
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember) #登入用户
                flash('welcome back.', 'info')
                return redirect_back() #返回上一个页面
            flash('invalid username or password.', 'warning')
        else:
            flash('no account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout success', 'info')
    return redirect_back()

