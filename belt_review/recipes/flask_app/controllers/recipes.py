from flask import render_template, session, redirect, request, flash
from flask_app.models import recipe, user
from flask_app import app

@app.route('/recipes/new')
def create_recipe():
    if 'user_id' in session:
        return render_template('add-recipe.html', user_id=session['user_id'])
    return redirect('/')

@app.route('/recipes/new/push', methods=['POST'])
def push_recipe():
    if 'user_id' in session:
        if not recipe.Recipe.recipe_validation(request.form):
            session['name'] = request.form['name']
            session['description'] = request.form['description']
            session['instructions'] = request.form['instructions']
            session['date'] = request.form['date']
            return redirect('/recipes/new')
        recipe.Recipe.save(request.form)
        return redirect('/recipes')
    return redirect('/')

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if 'user_id' in session:
        recipe.Recipe.delete_recipe(recipe_id)
        return redirect('/recipes')
    return redirect('/')

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' in session:
        session['recipe_id'] = recipe_id
        return render_template('edit-recipe.html', recipe=recipe.Recipe.one_recipe(recipe_id))
    return redirect('/')

@app.route('/recipes/edit/push', methods=['POST'])
def edit_recipe_push():
    if 'user_id' in session:
        if not recipe.Recipe.recipe_validation(request.form):
            recipe_id = request.form['recipe_id']
            return redirect(f'/recipes/edit/{recipe_id}')
        recipe.Recipe.edit_recipe(request.form)
        return redirect('/recipes')
    return redirect('/')

@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    if 'user_id' in session:
        return render_template('view-recipe.html', user=user.User.get_one(session['user_id']), recipe=recipe.Recipe.one_recipe(recipe_id))
    return redirect('/')
