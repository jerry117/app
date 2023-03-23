from flask import render_template, Blueprint

blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    return render_template('blog/index.html')


@blog.route('/about')
def about():
    return render_template('blog/about.html')


@blog.route('/category/<inst:category_id>')
def show_category(category_id):
    return render_template('blog/category.html')


@blog.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    return render_template('blog/post.html')
