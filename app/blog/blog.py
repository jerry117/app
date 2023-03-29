from flask import render_template, Blueprint, request, current_app
from app.models.models import Post, Category, Comment

blog = Blueprint('blog', __name__)


@blog.route('/', defaults={'page': 1})
@blog.route('/page/<int:page>')
def index(page):
    # page = request.args.get('page', 1, type=int) #从查询字符串获取当前页数
    # per_page = current_app.config['BLUELOG_POST_PER_PAGE'] #每页数量
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['BLUELOG_POST_PER_PAGE']) #分页对象
    posts = pagination.items #当前页数的记录列表
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@blog.route('/about')
def about():
    return render_template('blog/about.html')


@blog.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.asc()).paginate(page, per_page)
    comments = pagination.items
    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments)

@blog.route('/post/<slug>')
def show_post1(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('post.html', post=post)
