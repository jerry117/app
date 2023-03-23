from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, MultipleFileField, TextAreaField, EmailField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, Email, URL, Length, Optional
from flask_ckeditor import CKEditorField
from app.models.models import Category


class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={
                           'placeholder': 'Your Username'}, validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(8, 128)])
    remember = BooleanField('Rememberme')
    submit = SubmitField('Login')

# form.username(style='width: 200px;', class_='bar')
# class是Python的保留关键字，在这里我们使用class_来代替class，渲染后 的<input>会获得正确的class属性，在模板中调用时则可以直接使用class。
# 通过上面的方法也可以修改id和name属性，但表单被提交后，WTForms需要通 过name属性来获取对应的数据，所以不能修改name属性值。

# 设置内置错误消息语言为中文


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class HelloForm(MyBaseForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField()

# 也可以在实例化表单类时通过meta关键字传入locales值
# form = HelloForm(meta={'locales': ['en_US', 'en']})


class FortyTwoForm(FlaskForm):
    answer = IntegerField('The Number')
    submit = SubmitField()

    def validate_answer(form, field):
        if field.date != 42:
            raise ValidationError('Must be 42.')


# 另外一种写法全局验证器示例
def is_42(form, field):
    if field.date != 42:
        raise ValidationError('Must be 42')

# 因为在validators列表中传入的验证器必须是可调用对象，所以 这里传入了函数对象，而不是函数调用。


class FortytwoForm(FlaskForm):
    answer = IntegerField('The Number', validators=[is_42])
    submit = SubmitField()


# 验证函数实现城工厂函数
def is_42(message=None):
    if message is None:
        message = 'Must be 42.'

    def _is_42(form, field):
        if field.data != 42:
            raise ValidationError(message)
    return _is_42


class fortyTwoForm(FlaskForm):
    answer = IntegerField('The Number', validators=[is_42()])
    submit = SubmitField()


class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[
                      FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField()


class MultiUploadForm(FlaskForm):
    photo = MultipleFileField('Upload Image', validators={DataRequired()})
    submit = SubmitField()


class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')


class NewNoteForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')


class SubscribeForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('sendemail')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')

# 评论表单


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()
