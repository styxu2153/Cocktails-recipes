from flask import request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, FieldList
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from application.models import Recipe

class RecipeForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    alcohol_name = FieldList(StringField())
    alcohol_amount = FieldList(StringField())
    ingredient_name = FieldList(StringField())
    ingredient_amount = FieldList(StringField())
    need_shaker = BooleanField('Shaker needed')
    submit = SubmitField('')

class RecipeAddForm(RecipeForm):
    submit = SubmitField('Add Recipe')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def validate_name(self, name):
        recipe = Recipe.query.filter_by(name=name.data).first()
        if recipe is not  None:
            flash('Recipe already exists!')
            raise ValidationError('Recipe with this name already exists')
        
class RecipeUpdateForm(RecipeForm):
    submit = SubmitField('Update Recipe')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        