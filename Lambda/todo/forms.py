"""
Todo application forms using WTForms
"""
from wtforms import Form, StringField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length

class TodoForm(Form):
    """Todo作成・編集用フォーム"""
    title = StringField('Title', validators=[
        DataRequired(message='タイトルは必須です'),
        Length(max=200, message='タイトルは200文字以内で入力してください')
    ])
    
    description = TextAreaField('Description', validators=[
        Length(max=1000, message='説明は1000文字以内で入力してください')
    ])
    
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'), 
        ('high', 'High')
    ], default='medium')
    
    completed = BooleanField('Completed', default=False)

class CategoryForm(Form):
    """カテゴリー作成・編集用フォーム"""
    name = StringField('Name', validators=[
        DataRequired(message='カテゴリー名は必須です'),
        Length(max=50, message='カテゴリー名は50文字以内で入力してください')
    ])
    
    color = SelectField('Color', choices=[
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('red', 'Red'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('orange', 'Orange'),
        ('pink', 'Pink'),
        ('gray', 'Gray')
    ], default='blue')