from flask import Flask, render_template, request, redirect

from user import User

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('create.html')

@app.route('/read')
def read():
    users = User.get_all()
    return render_template('read.html', all_users = users)

@app.route('/create_user', methods=['POST'])
def create_user():
    data = { 
            'fname': request.form['fname'],
            'lname': request.form['lname'],
            'email': request.form['email'],
            }
    User.save(data)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)