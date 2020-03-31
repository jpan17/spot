from app import app
from app import db_service
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

# login page after user hits 'enter'
@app.route('/login', methods=['POST'])
def user_type():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = db_service.get_user_by_login(email, password)
    if user == None:
        html = render_template('users/login.html',
                                title='Login | Spot')
        response = make_response(html)
        return response
    
    if user.is_owner:
        owner_home(user)
        
    return

# Registration page. Temporarily is the same as Login page.
@app.route('/register', methods=['POST'])
def register_form():
    html = render_template('users/register.html',
        title='Register | Spot')
    response = make_response(html)
    return response

@app.route('/owner', methods=['POST'])
def owner_home(user):
    first_name = user.full_name.split()[0]
    html = render_template('users/owner_home.html',
                           title=first_name+ " | Spot")
    response = make_response(html)
    return response

@app.route('/sitter')
def sitter_home():
    pass