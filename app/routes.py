from app import app
from app import db_service
from flask import make_response, render_template, request
from flask import url_for, redirect

# Homepage with listings for users
@app.route('/')
def home():
    html = render_template('users/owners/home.html',
        title='Home | Spot',
        listings=db_service.all_listings())
    response = make_response(html)
    return response

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

@app.route('/listings/new')
def listing_new():
    html = render_template('users/owners/home.html',
        title='New Listing | Spot')
    response = make_response(html)
    return response

@app.route('/listings/<int:listing_id>')
def listing_details(listing_id):
    return redirect(url_for('home'))