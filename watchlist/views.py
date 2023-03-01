import os
import uuid
from flask import render_template, request, url_for, redirect, flash, abort, make_response, jsonify, json, session, g
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movie
from watchlist.form.forms import UploadForm, SubscribeForm
from watchlist.email import send_mail

#会过滤掉文件名中的非ASCII字符。 但如果文件名完全由非ASCII字符组成，那么会得到一个空文件名
# from werkzeug import secure_filename



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


# 下面的代码是demo

@app.route('/home/<name>')
def home(name):
    return url_for('home', name='jerry',_external=True) #返回完整的URL地址

@app.route('/')
@app.route('/hello')
def hello():
    # name = request.args.get('name')
    response = f'hello,{g.name}'
    if g.name is None:
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

# g的用法
@app.before_request
def get_name():
    g.name = request.args.get('name')

# 激活上下文。
# 使用flask run命令启动程序
# 使用旧的app.run()方法启动程序
# 使用@app.cli.command()装饰器注册的flask命令时
# 使用flask shell命令启动python shell时

# 手动激活上下文
# from app import app
# from flask import current_app
# with app.app_context():
#     current_app.name

# 显示手动激活上下文
# from app import app
# from flask import current_app
# app_ctx = app.app_context()
# app_ctx.push()
# current_app.name
# app_ctx.pop()

# 请求上下文可以通过test_request_context()方法临时创建：
# from app import app
# from flask import request
# with app.test_request_context('/hello'):
#     request.method

# 上下文钩子
# @app.teardown_appcontext
# def teardown_db(exception):
#     db.close()

# 返回上一个页面。
# return redirect(request.referrer or url_for('hello'))

# 返回上一个页面的另外一种写法。
# from flask import request

# @app.route('/foo')
# def foo():
#     return '<h1>foo page</h1><a href="%s">do something and redirect</a>' %url_for('do_something', next=request.full_path)

# @app.route('/bar')
# def bar():
#     return '<h1>bar page</h1><a href="%s">do something and redirect</a>' %url_for('do_something', next=request.full_path)

# 通过获取这个next值，然后重定向到对应的路径：
# return redirect(request.args.get('next')) 

# 需要添加备选项，如果为空就重定向到hello视图：
# return redirect(request.args.get('next', url_for('hello')))

# 重定向回上一个页面
# def redirect_back(default='hello', **kwargs):
#     for target in request.args.get('next'), request.referrer: #for循环独特的写法。
#         if target:
#             return redirect(target)
#     return redirect(url_for(default, **kwargs))

@app.route('/do_something_and_redirect')
def do_something():
    return redirect_back()

# 开放重定向漏洞
# 验证URL安全性

from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# 加了验证的重定向回上一个页面
def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

# 显示虚拟文章 
# from jinja2.utils import generate_lorem_ipsum

# @app.route('/post')
# def show_post():
#     post_body = generate_lorem_ipsum(n=2) #生成两段随机文本
#     return '''<h1>A very long post</h1> <div class="body">%s</div> <button id="load">Load More</button> <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script> <script type="text/javascript"> $(function() { $('#load').click(function() { $.ajax({ url: '/more', // 目标URL type: 'get', // 请求方法 success: function(data){ // 返回2XX响应后触发的回调函数 $('.body').append(data); // 将返回的响应插入到页面中 } }) }) })</script>''' % post_body

# 处理/more的视图函数会返回随机文章正文
# @app.route('/more')
# def load_post():
#     return generate_lorem_ipsum(n=1)

# 使用jinja2提供的escape()函数对用户传入的数据进行转义，为了安全性。
# from jinja2 import escape

# @app.route('/hello1')
# def hello1():
#     name = request.args.get('name')
#     response = '<h1>Hello, %s!</h1>' % escape(name)

# 生成随机文件名
# def random_filename(filename):
#     ext = os.path.splitext(filename)[1]
#     new_filename = uuid.uuid4().hex + ext
#     return new_filename

# # 处理上传文件
# @app.route('/upload', method=['GET', 'POST'])
# def upload():
#     form = UploadForm()
#     if form.validate_on_submit():
#         f = form.photo.data
#         filename = random_filename(f.filename)
#         f.save(os.path.join(app.config['UPLOAD_PATH'], filename)) 
#         flash('Upload success.') 
#         session['filenames'] = [filename] 
#         return redirect(url_for('show_images')) 
#     return render_template('upload.html', form=form)

# 发送邮件
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        flash('Welcome on board!')
        send_mail('Subscribe Successs!', email, 'Hello, thank you for subscribing Flask Weekly!')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.route('/email')
def email():
    data = send_mail('Subscribe Successs!','XXX@qq.com','hello world')
    print(data)
    return {'code':200}

