from watchlist.models import Draft
from watchlist import db

# 传统的参数接收方法
@db.event.listens_for(Draft.body, 'set')
def increment_edit_time(target, value, oldvalue, initiator):
    if target.edit_time is not None:
        target.edit_time += 1

# 在函数中可以使用参数名作为键来从**kwargs字典获取对应的参 数值
# @db.event.listens_for(Draft.body, 'set', name=True)
# def increment_edit_time(**kwargs):
#     if kwargs['target'].edit_time is not None:
#         kwargs['target'].edit_time += 1

# 除了使用listen_for装饰器，我们还可以直接使用它内部调用的listen（）函 数注册事件监听函数时，第三个参数传入被注册的函数对象，比如 db.event.listen（SomeClass，'load'，my_load_listener）。

