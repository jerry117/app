from flask import render_template, Blueprint, request, current_app
from app.models.models import Post

blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    page = request.args.get('page', 1, type=int) #从查询字符串获取当前页数
    per_page = current_app.config['BLUELOG_POST_PER_PAGE'] #每页数量
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page) #分页对象
    posts = pagination.items #当前页数的记录列表
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@blog.route('/about')
def about():
    return render_template('blog/about.html')


@blog.route('/category/<inst:category_id>')
def show_category(category_id):
    return render_template('blog/category.html')


@blog.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    return render_template('blog/post.html')
