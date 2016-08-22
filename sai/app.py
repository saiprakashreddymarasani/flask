# import required classes from flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g

import os, sqlite3
from functools import wraps

# create instance
app = Flask(__name__)
app.database = 'small.db'

app.secret_key=os.urandom(64)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# connecting to database

def connect_db():
    return sqlite3.connect(app.database)


# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(username=row[0]) for row in cur.fetchall()]
    g.db.close()
    return render_template('index.html', posts=posts)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# route for login

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'sai' or request.form['password'] != 'Daniel':
            error = 'Invalid details, please try again.'
        else:
            session['logged_in'] = True
            flash('Congrats, You were logged in')

            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True)