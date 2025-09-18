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

class ChangePasswordForm(Form):
  current_password = PasswordField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=8, max=63)],
    label='現在のパスワード'
  )
  new_password = PasswordField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=8, max=63)],
    label='新しいパスワード'
  )
  confirm_password = PasswordField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=8, max=63)],
    label='新しいパスワード（確認）'
  )

  def validate(self):
    if not super().validate():
      return False
    
    if self.new_password.data != self.confirm_password.data:
      self.confirm_password.errors.append('パスワードが一致しません')
      return False
    
    return True

class ForgotPasswordForm(Form):
  username = StringField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=1, max=63)],
    label='ユーザー名'
  )

class ResetPasswordForm(Form):
  username = StringField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=1, max=63)],
    label='ユーザー名'
  )
  confirmation_code = StringField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=6, max=6)],
    label='確認コード'
  )
  new_password = PasswordField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=8, max=63)],
    label='新しいパスワード'
  )
  confirm_password = PasswordField(
    render_kw={'style': 'width: 200px;'},
    validators=[DataRequired(), Length(min=8, max=63)],
    label='新しいパスワード（確認）'
  )

  def validate(self):
    if not super().validate():
      return False
    
    if self.new_password.data != self.confirm_password.data:
      self.confirm_password.errors.append('パスワードが一致しません')
      return False
    
    return True