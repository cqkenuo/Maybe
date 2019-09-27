from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import (
    BooleanField, StringField, SubmitField, SelectField, PasswordField,
    FileField, TextAreaField
)
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[DataRequired(), Length(1, 64)])
    password = PasswordField(
        label='Password',
        validators=[DataRequired(), Length(1, 128)])
    remember_me = BooleanField('Remember me.')
    submit = SubmitField('Log in')


class ArticleForm(FlaskForm):
    title = StringField(
        label='Title',
        validators=[DataRequired(), Length(1, 60)])
    submit = SubmitField('Log in')


class UpdateForm(FlaskForm):
    title = StringField(
        label='Title',
        validators=[DataRequired(), Length(1, 60)])
    # category = SelectField('Category', coerce=int, default=1)
    markdown = FileField(
        label='Markdown-file',
        validators=[FileRequired(), FileAllowed(['md'], 'Only .md')])
    submit = SubmitField()


class VerifyArticleForm(FlaskForm):
    submit = SubmitField()


class LeaveMsgForm(FlaskForm):
    # username = StringField(
    #     label='Username',
    #     validators=[DataRequired(), Length(1, 64)])
    # password = PasswordField(
    #     label='Password',
    #     validators=[DataRequired(), Length(1, 128)])
    body = TextAreaField(
        label="What's on your mind ?",
        validators=[DataRequired()])
    submit = SubmitField()
