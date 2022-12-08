from flask import render_template, request, redirect, session,flash,url_for
from flask_app import app
from flask_app.models import recipe
from flask_app.models import user
from datetime import datetime
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 
dateFormat = "%B %d,%Y"



@app.route('/recipes')
def recipes():
   if 'user_id' not in session:
      return redirect('/')
   data = {
      'id': session['user_id']
   }
   return render_template('recipes_board.html', current_user = user.Users.getByID(data),
                        recipes = recipe.Recipes.get_users_with_recipes())

@app.route('/recipe/new')
def new_recipe_page():
   return render_template('creating_recipe.html')


@app.route('/creating/recipe', methods=['POST'])
def creating_recipe():
   print(f'this is what we are returning {request.form}')
   if recipe.Recipes.validate_new_recipe(request.form):
      data = {
      'user_id': session['user_id'],
      'recipe_name': request.form['recipe_name'],
      'description': request.form['description'],
      'instructions': request.form['instructions'],
      'date_cooked': request.form['date_cooked'],
      'cooked_in_30': request.form['cooked_in_30']
   }
      recipe.Recipes.save(data)
      return redirect('/recipes')
   else:
      return redirect('/recipe/new')

@app.route('/delete/<int:recipe_id>')
def destroy_recipe(recipe_id):
   recipe.Recipes.deleteById({'id':recipe_id})
   return redirect('/recipes')

@app.route('/edit/<int:recipe_id>', methods=['POST'])
def editing_recipe(recipe_id):
   
   if recipe.Recipes.validate_new_recipe(request.form):
      data = {
         'recipe_name': request.form['recipe_name'],
         'description':request.form['description'],
         "instructions": request.form['instructions'], 
         "date_cooked": request.form['date_cooked'],
         'cooked_in_30' : request.form['cooked_in_30'],
         'id': recipe_id
      }
      recipe.Recipes.edit(data)
      return redirect('/recipes')
   else: 
      recipe_id = recipe_id
      return redirect(url_for('edit_the_recipe', recipe_id= recipe_id))


@app.route('/recipes/edit/<int:recipe_id>')
def edit_the_recipe(recipe_id):
   return render_template('edit_recipe.html', recipe = recipe.Recipes.getByID({'id': recipe_id}))


@app.route('/view/<int:recipe_id>')
def view_recipe(recipe_id):
   data = {
      'id': session['user_id']
   }
   return render_template('view_recipe.html', recipe = recipe.Recipes.getByID({'id':recipe_id}), current_user = user.Users.getByID(data), recipes = user.Users.get_recipe_with_creator({'id': recipe_id}), dates = dateFormat)