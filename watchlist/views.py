from flask import render_template, request, url_for, redirect, flash, abort, make_response, jsonify, json, session
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movie


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # 判断是否是 POST 请求
        if not current_user.is_authenticated: #判断当前用户是否登陆
            return redirect(url_for('index'))
        # 获取表单数据
        title = request.form['title'] # 传入表单对应输入字段的 name 值
        year = request.form['year']  
        # 验证数据
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('index')) # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)
        db.session.add(movie) # 添加到数据库会话
        db.session.commit() # 提交数据库会话
        flash('Item created.') # 显示成功创建的提示
        return redirect(url_for('index')) # 重定向回主页

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST': # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id)) # 重定向回对应的编辑页面

        movie.title = title # 更新标题
        movie.year = year # 更新年份
        db.session.commit() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index')) # 重定向回主页

    return render_template('edit.html', movie=movie) # 传入被编辑 的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required #登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        # current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象 
        #  等同于下面的用法 
        #  user = User.query.first() 
        #  user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user) #登入用户
            flash('Login success.')
            return redirect(url_for('index')) # 重定向到主页

        flash('Invalid username or password.') # 如果验证失败，显示错误消息
        return redirect(url_for('login')) # 重定向回登录页面

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user() # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index')) # 重定向回首页

@app.route('/home/<name>')
def home(name):
    return url_for('home', name='jerry',_external=True) #返回完整的URL地址

@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'flask') #从cookie中获取name值
        response = f'hello,{name}'
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
    return response

@app.route('/colors/<any(blue,white,red):color>') #如果将<color> 部分替换为any转换器中设置的可选值以外的任意字符，均会获得404错误响应。
def three_colors(color):
    return f'{color}'

@app.route('/location')
def location():
    # return redirect('http://www.baidu.com') # 重定向写法
    return redirect(url_for('home', name='tom')) # 重定向到有参数的视图

@app.route('/404')
def not_found():
    abort(404)

@app.route('/foo')
def foo():
    # data = {'name': 'jerry', 'gender':'male'}
    # response = make_response(json.dumps(data))
    # response.mimetype = 'application/json'
    # return response
    return jsonify(name='jerry', gender='male'), 404

# HTTP是无状态（stateless）协议

@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response

@app.route('/login1')
def login1():
    session['logged_in'] = True # 写入session
    return redirect(url_for('hello'))

@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'welcome to admin page.'

@app.route('/logout1')
def logout1():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))

# 这四个变量都是代理对象（proxy），即指向真实对象的代理。一般情况下，我 们不需要太关注其中的区别。在某些特定的情况下，如果你需要获取原始对象，可 以对代理对象调用_get_current_object（）方法获取被代理的真实对象。
# current_app 程序上下文
# g   程序上下文
# request  请求上下文
# session  请求上下文

