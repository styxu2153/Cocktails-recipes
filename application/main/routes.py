from flask import render_template, redirect, request, url_for, flash
from application import db
from application.main import bp
from application.main.forms import RecipeAddForm, RecipeUpdateForm
from application.models import Recipe, Alcohol
from sqlalchemy import and_

@bp.route('/')
@bp.route('/index', methods=['GET', 'POST'])
def index():
    recipes = Recipe.query.order_by(Recipe.name.asc()).all()
    alcohols = Alcohol.query.order_by(Alcohol.name.asc()).all()
    alcohols_names = [alcohol.name for alcohol in alcohols]

    if request.method == 'POST' and request.form.getlist('alcohols_filter') != []:
        checked_boxes = request.form.getlist('alcohols_filter')
            
        filter_values = [filter for filter in alcohols_names if filter not in checked_boxes]
            
        recipes = Recipe.query.filter(and_(Recipe.ingredients.notlike(f"%{filter}%") for filter in filter_values)).all()
                
        return render_template('index.html', recipes=recipes, alcohols=alcohols)
    
    return render_template('index.html', recipes=recipes, alcohols=alcohols)

@bp.route('/add-recipe', methods=['GET', 'POST'])
def add_recipe():
    form = RecipeAddForm()
    
    if form.validate_on_submit():
        recipe_name = form.name.data.capitalize()
        shaker_needed = form.need_shaker.data
        ingredients = []
        alcohols = []
        
        if form.alcohol_name.data:
            for item in zip(form.alcohol_name.data, form.alcohol_amount.data):
                if item[0] != "":
                    alcohols.append(item[0].capitalize())
                    ingredient = " ".join(item)
                    ingredients.append(ingredient)
                
        if form.ingredient_name.data:
            for item in zip(form.ingredient_name.data, form.ingredient_amount.data):
                if item[0] != "" and item[1] != "":
                    ingredient = " ".join(item)
                    ingredients.append(ingredient)
                
        ingredients_to_insert = ", ".join(ingredients)
        
        recipe = Recipe(recipe_name, ingredients_to_insert, shaker_needed)
        db.session.add(recipe)
        
        for alcohol in alcohols:
            alcohol_exist = Alcohol.query.filter_by(name=alcohol).first()
            if alcohol_exist is None:
                new_alcohol = Alcohol(name=alcohol)
                db.session.add(new_alcohol)
                
        db.session.commit()
        return redirect(url_for('main.index'))
    
    return render_template('add_recipe.html', form=form)

@bp.route('/update-recipe/<recipe_name>', methods=['GET', 'POST'])
def update_recipe(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first()
    form = RecipeUpdateForm()
    
    if form.validate_on_submit():
        recipe_name = form.name.data.capitalize()
        shaker_needed = form.need_shaker.data
        ingredients = []
        alcohols = []
        
        if form.alcohol_name.data:
            for item in zip(form.alcohol_name.data, form.alcohol_amount.data):
                if item[0] != "":
                    alcohols.append(item[0].capitalize())
                    ingredient = " ".join(item)
                    ingredients.append(ingredient)
                    
        if form.ingredient_name.data:
            for item in zip(form.ingredient_name.data, form.ingredient_amount.data):
                if item[0] != "" and item[1] != "":
                    ingredient = " ".join(item)
                    ingredients.append(ingredient)
    
        ingredients_to_insert = ", ".join(ingredients)
        
        recipe.name = recipe_name
        recipe.ingredients = ingredients_to_insert
        recipe.need_for_shaker = shaker_needed
        db.session.commit()
        flash('Changes have been saved!')
        return redirect(url_for('main.index'))
    
    elif request.method == 'GET':
        form.name.data = recipe.name
        form.need_shaker.data = recipe.need_for_shaker
    return render_template('update_recipe.html', form=form, recipe=recipe)
        
        

@bp.route('/delete-recipe/<recipe_name>')
def delete_recipe(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first()
    
    db.session.delete(recipe)
    db.session.commit()
    
    return redirect(url_for('main.index'))
    