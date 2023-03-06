from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_class import User

@app.route('/')
def index():
    return render_template('home.html')


#VIEW ALL USERS 
@app.route('/users')
def read():
    return render_template('read.html', users=User.get_all())

#CREATE USER FORM
@app.route('/create_user', methods=['POST'])
def create_user():
    data = { 
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            }
    if not User.validate_user(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        return redirect('/create')
    else:
        session.clear()
    new_user = User.save(data)
    return redirect(f'/user/show/{new_user}')

#SHOW USER BY ID
@app.route('/user/show/<int:id>')
def show_one(id):
    data = {
        'id': id
    }
    return render_template('user.html', user = User.get_one(data))

#EDIT USER
@app.route('/user/edit/<int:id>')
def edit(id):
    data = {
        'id': id
    }
    return render_template('edit_user.html', user = User.get_one(data))

#UPDATE USER FORM
@app.route('/user/update', methods = ['POST'])
def update():
    updated_id = request.form['id']
    User.update(request.form)
    return redirect(f'/user/show/{updated_id}')

#DELETE USER
@app.route('/user/delete/<int:id>')
def delete(id):
    data = {
        'id': id
    }
    User.delete(data)
    return redirect('/users')
    
    
#CREATE USER PAGE
@app.route('/create')
def user_create():
    print('session:', session)
    return render_template('create.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_user_email(request.form['email']):
        return redirect('/create')
    return redirect('/')
    
