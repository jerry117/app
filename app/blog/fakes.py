from app.models.models import Admin, Category, Post, Comment
from app.extensions import db
from faker import Faker
import random

fake = Faker()

# 虚拟管理员


def fakeAdmin():
    admin = Admin(username='admin', blog_title='Blog', blgo_sub_title='no, i`m the real thing.',
                  name='mima kirigoe', about='um, l, mima kirigoe, had a fun time as a member of cham...')
    admin.set_password('jerry')
    db.session.add(admin)
    db.session.commit()

# 分类


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()

        except db.IntegrityError:
            db.session.rollback()

# 生成虚拟文章


def fake_posts(count=50):
    for i in range(count):
        post = Post(title=fake.sentence(), body=fake.text(2000), category=Category.query.get(
            random.randint(1, Category.query.count())), timestamp=fake.date_time_this_year())
        db.session.add(post)
    db.session.commit()

# 生成虚拟评论


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(author=fake.name(), email=fake.email(), site=fake.url(), body=fake.sentence(),
                          timestamp=fake.date_time_this_year(), reviewed=True, post=Post.query.get(random.randint(1, Post.query.count())))
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # 未审核评论
        comment = Comment(author=fake.name(), email=fake.email(), site=fake.url(), body=fake.sentence(),
                          timestamp=fake.date_time_this_year(), reviewed=False, post=Post.query.get(random.randint(1, Post.query.count())))
        db.session.add(comment)

        # 管理员发表的评论
        comment = Comment(author='Mima Kirigoe', email='mima@example.com', site='example.com', body=fake.sentence(),
                          timestamp=fake.date_time_this_year(), from_admin=True, reviewed=True, post=Post.query.get(random.randint(1, Post.query.count())))
        db.session.add(comment)
    db.session.commit()
    # 回复
    for i in range(salt):
        comment = Comment(author=fake.name(), email=fake.email(), site=fake.url(), body=fake.sentence(), timestamp=fake.date_time_this_year(
        ), reviewed=True, replied=Comment.query.get(random.randint(1, Comment.query.count())), post=Post.query.get(random.randint(1, Post.query.count())))
        db.session.add(comment)
    db.session.commit()
