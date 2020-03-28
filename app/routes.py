from app import app
from flask import make_response, render_template, request
from flask import url_for, redirect

# Temporary - just redirects to login page as of now
@app.route('/')
def home():
    return redirect(url_for('login_form'))

# Login page. Should redirect automatically to homepage if logged in already, but currently does not
@app.route('/login')
def login_form():
    html = render_template('users/login.html',
        title='Login | Spot')
    response = make_response(html)
    return response

# Registration page. Temporarily is the same as Login page.
@app.route('/register')
def register_form():
    html = render_template('users/register.html',
        title='Register | Spot')
    response = make_response(html)
    return response