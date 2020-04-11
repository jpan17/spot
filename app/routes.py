from app import app
from app import db_service
from flask import Flask
from flask import make_response, render_template, request, session
from flask import url_for, redirect
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from app.models import User, Listing
import enums
import os
from datetime import datetime

app.secret_key = os.environ.get('SPOT_SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)

# determines which home page to route to based on current_user (login, sitter_home, owner_home)
@app.route('/')
def home():

    user_id = current_user.get_id()

    if user_id is None: 
        html = render_template('users/login.html',
        title='Login | Spot')
        response = make_response(html)
        return response    

    if current_user.is_owner:
        print (current_user.id)
        first_name = current_user.full_name.split()[0]
        listings = db_service.get_user_listings(user_id)
        html = render_template('users/owner_home.html',
                            title=first_name+" | Spot",
                            id=user_id,
                            listings=listings,
                            listings_len=len(listings),
                            user = current_user)
        response = make_response(html)
        return response

    if current_user.is_sitter:
        print (current_user.id)
        first_name = current_user.full_name.split()[0]
        all_listings = db_service.all_listings()
        html = render_template('users/sitter_home.html',
                            title=first_name+" | Spot",
                            id=user_id,
                            listings=all_listings,
                            listings_len=len(all_listings),
                            user = current_user)
        response = make_response(html)
        return response

    return redirect(url_for('login_form'))

# apparently necessary, crashes program if removed. Just following what flask says lol. 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# processes login info and redirects to appropriate page (login, sitter home, owner home)
@app.route('/login', methods=['POST'])
def user_type():

    print("you wanna be here")

    email = request.form.get('email')
    password = request.form.get('password')
    
    user = db_service.get_user_by_login(email)

    if user == None:
        return redirect(url_for('login_form'))

    passwordMatch = db_service.check_password(user, password)
    
    if passwordMatch:
        login_user(user)
        response = redirect(url_for('home'))
        return response
    else:
        return redirect(url_for('login_form'))

@app.route('/logout')
def logout():
    logout_user()
    response = redirect(url_for('home'))
    return response


# Registration page with the form
@app.route('/register')
def register_form():
    print("fucked up")
    html = render_template('users/register.html',
        title='Register | Spot')
    response = make_response(html)
    return response

# registers the user and redirects to login page
@app.route('/register', methods=['POST'])
def register_user():
    print("registering user now")
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone_number = request.form.get('password')
    # print(request.form.get('user_type'))
    is_owner = request.form.get('user_type') == 'owner'
    is_sitter = not is_owner
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if password != confirm_password:
        html = render_template('users/register.html',
                                 title='Register | Spot')
        response = make_response(html)
        return response

    user = User()
    user.full_name = full_name
    user.email = email
    user.phone_number = phone_number
    user.is_owner = is_owner
    user.is_sitter = is_sitter
    user.password_hash = db_service.set_password(user, password)
    print(user.password_hash)
    
    new_user = db_service.create_user(user)
    if new_user != '':
        print(new_user)
    else:
        print('Created a new user ', user.full_name)
    
    html = render_template('users/login.html',
                            title='Login | Spot')
    response = make_response(html)
    return response 

# haven't touched yet, but idt needs cookies. 
@app.route('/listings/new')
@login_required
def listing_new():
    html = render_template('users/owners/listing_new.html',
        title='New Listing | Spot',
        pet_types=enums.pet_types,
        activities=enums.activities)
    response = make_response(html)
    return response

# might be okay to have listing id in the url
@app.route('/listings/<int:listing_id>')
@login_required
def listing_details(listing_id):
    listing = db_service.get_listing_by_id(listing_id)
    if listing == None:
        return redirect(url_for('error', error='Listing not found.'))

    html = render_template('users/owners/listing_details.html',
        title='Listing Details | Spot',
        listing=listing)
    response = make_response(html)
    return response

# will be implemented after a proper sitter_home.html added
@app.route('/sitter/<int:id>/accepted')
@login_required
def accepted_listings(id):
    user = db_service.get_user_by_id(id)
    first_name = user.full_name.split()[0]
    accepted_listings=db_service.get_user_listings(user, True)
    html = render_template('listings/accepted_listings.html',
                           title="Accepted Listings | Spot",
                           id=id,
                           accepted_listings=accepted_listings,
                           accepted_listings_len=len(accepted_listings))
    response = make_response(html)
    return response

# implemented once delete functionality added 
@app.route('/listings/<int:listing_id>/delete')
@login_required
def listing_delete(listing_id):
    return redirect(url_for('home'))

# implemented once update funcitonality added
@app.route('/listings/<int:listing_id>/update')
@login_required
def listing_update(listing_id):
    return redirect(url_for('home'))

@app.route('/error')
def error():
    error = request.args.get('error') or ''
    
    return redirect(url_for('home'))