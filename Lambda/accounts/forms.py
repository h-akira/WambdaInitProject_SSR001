from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
  username = StringField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=1, max=63)],
    label='ユーザー名'
  )
  password = PasswordField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=8, max=63)],
    label='パスワード'
  )

class SignupForm(Form):
  username = StringField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=1, max=63)],
    label='ユーザー名　　'
  )
  password = PasswordField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=8, max=63)],
    label='パスワード　　'
  )
  email = StringField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=1, max=63)],
    label='メールアドレス'
  )

class VerifyForm(Form):
  username = StringField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=1, max=63)],
    label='ユーザー名'
  )
  code = StringField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=6, max=6)],
    label='確認コード'
  )