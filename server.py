from flask import Flask, render_template, request, redirect

from user import User

app = Flask(__name__)
app.secret_key = 'key1'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/users')
def read():
    return render_template('read.html', users=User.get_all())

@app.route('/create_user', methods=['POST'])
def create_user():
    data = { 
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            }
    new_user = User.save(data)
    return redirect(f'/user/show/{new_user}')

@app.route('/user/show/<int:id>')
def show_one(id):
    data = {
        'id': id
    }
    return render_template('user.html', user = User.get_one(data))

@app.route('/user/edit/<int:id>')
def edit(id):
    data = {
        'id': id
    }
    return render_template('edit_user.html', user = User.get_one(data))

@app.route('/user/update', methods = ['POST'])
def update():
    updated_id = request.form['id']
    User.update(request.form)
    return redirect(f'/user/show/{updated_id}')

@app.route('/user/delete/<int:id>')
def delete(id):
    data = {
        'id': id
    }
    User.delete(data)
    return redirect('/users')
    
@app.route('/create')
def user_create():
    return render_template('create.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)