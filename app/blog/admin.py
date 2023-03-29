from flask_login import login_required
from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from app.models.models import Post, Category
from app.form.forms import PostForm
from app.extensions import db
from app.utils import redirect_back

admin = Blueprint('admin', __name__)

@admin.route('/settings')
@login_required
def settings():
    return render_template('admin/settings.html')

# 有一个小技巧可以避免这些重复：为admin蓝本注册一个 before_request处理函数，然后为这个函数附加login_required装饰器。因为使 用before_request钩子注册的函数会在每一个请求前运行，所以这样就可以为该蓝 本下所有的视图函数添加保护，函数内容可以为空
@admin.before_request
@login_required
def login_protect():
    pass


@admin.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', page=page, pagination=pagination, posts=posts)

@admin.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash('post created.', 'success')
        return redirect(url_for('.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('post update.', 'success')
        return redirect(url_for('.show_post', post_id=post.id))
    form.title.data = post.title #预定义表单中的title字段值
    form.body.data = post.body #预定义表单中的body字段值
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)


@admin.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('post deleted.', 'success')
    return redirect_back()


@admin.route('/set-comment/<int:post_id>')
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('comment disabled.', 'info')
    else:
        post.can_comment = True
        flash('comment enabled.', 'info')
    db.session.commit()
    return redirect(url_for('.show_post', post_id=post_id))


@admin.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not delete the default category.', 'warning')
        return redirect(url_for('blog.index'))
    category.delete() # 调用category对象的delete()方法删除分类
    flash('Category deleted.', 'success')
    return redirect(url_for('.manage_category'))
