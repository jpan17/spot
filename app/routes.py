from app import app, login_manager
from app import db_service
from app.logger import Logger
from flask import Flask
from flask import make_response, render_template, request, session
from flask import url_for, redirect
from flask_login import UserMixin, login_required, current_user, login_user, logout_user
from app.models import User, Listing
import enums
import os
from datetime import datetime

logger = Logger()
login_manager.login_view = 'login_form'

# determines which home page to route to based on current_user (login, sitter_home, owner_home)
@app.route('/')
def home():
    
    user_id = current_user.get_id()

    if user_id is None: 
        return redirect(url_for('login_form'))

    # current_user is now known to be a User object
    logger.trace('Home accessed with user', current_user.id)

    if current_user.is_owner:
        listings = current_user.listings
        html = render_template('users/owners/home.html',
                            title="Home | Spot",
                            listings=listings,
                            listings_len=len(listings),
                            user = current_user)
        response = make_response(html)
        return response

    if current_user.is_sitter:
        all_listings = db_service.all_listings()
        html = render_template('users/sitters/home.html',
                            title="Home | Spot",
                            listings=all_listings,
                            listings_len=len(all_listings),
                            pet_types=enums.pet_types,
                            activities=enums.activities,
                            user = current_user)
        response = make_response(html)
        return response

    return redirect(url_for('error', error='User is neither owner nor sitter. Please create a new user instead.'))

# apparently necessary, crashes program if removed. Just following what flask says lol. 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login form (for separation from homepage)
@app.route('/login')
def login_form():
    html = render_template('users/login.html',
        title='Login | Spot')
    response = make_response(html)
    return response   

# processes login info and redirects to appropriate page (login, sitter home, owner home)
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = db_service.get_user_by_email(email)

    # As much as I like descriptive error messages, it's been a while since I've seen a site specify which one of email and password is wrong.
    # My guess is it's for security purposes, so I'm just going to not specify which is incorrect.
    if user == None:
        logger.debug('Failed login using email', email)
        return redirect(url_for('login_form', error='Email or password is incorrect.'))

    passwordMatch = db_service.check_password_hash(user, password)
    
    if passwordMatch:
        login_user(user)
        logger.debug('Logged in user with email', email)
        return redirect(url_for('home'))

    logger.debug('Failed login using email', email)
    return redirect(url_for('login_form', error='Email or password is incorrect.'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    response = redirect(url_for('login_form'))
    return response

# Registration page with the form
@app.route('/register')
def register_form():
    html = render_template('users/register.html',
        title='Register | Spot')
    response = make_response(html)
    return response

# registers the user and redirects to login page
@app.route('/register', methods=['POST'])
def register_user():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    is_owner = request.form.get('user_type') == 'owner'
    is_sitter = not is_owner
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if password != confirm_password:
        return redirect(url_for('register_form', error='Passwords don\'t match.'))

    user = User()
    user.full_name = full_name
    user.email = email
    user.phone_number = phone_number
    user.is_owner = is_owner
    user.is_sitter = is_sitter
    user.password_hash = db_service.generate_password_hash(password)
    
    user_error = db_service.create_user(user)
    if user_error != '':
        logger.warn('Error occurred creating user:', user_error)
        return redirect(url_for('register_form', error='Email or phone number already exists.'))
    else:
        logger.log('Created a new user:\n', user)
    
    return redirect(url_for('login_form'))

# haven't touched yet, but idt needs cookies. 
@app.route('/listings/new')
@login_required
def listing_new():
    html = render_template('users/owners/listing_new.html',
        title='New Listing | Spot',
        pet_types=enums.pet_types,
        activities=enums.activities,
        user = current_user)
    response = make_response(html)
    return response

# might be okay to have listing id in the url
@app.route('/listings/<int:listing_id>')
@login_required
def listing_details(listing_id):
    listing = db_service.get_listing_by_id(listing_id)
    if listing == None:
        return redirect(url_for('error', error='Listing not found.'))

    if current_user.is_owner:
        if listing.user_id == current_user.id:
            html = render_template('users/owners/listing_details.html',
                title='Listing Details | Spot',
                listing=listing,
                user = current_user)
            response = make_response(html)
            return response
        else:
            return redirect(url_for('error', error='Listing is owned by a different user.'))
    
    if current_user.is_sitter:
        html = render_template('users/sitters/listing_details.html',
            title = 'Listing Details | Spot',
            listing = listing,
            user = current_user)
        response = make_response(html)
        return response

    return redirect(url_for('error', error='User is neither owner nor sitter. Please create a new user instead.'))

# will be implemented after a proper sitter_home.html added
@app.route('/accepted')
@login_required
def accepted_listings():
    user = current_user
    if not user.is_sitter:
        return redirect(url_for('error', error='Invalid URL.'))

    accepted_listings = user.accepted_listings
    html = render_template('users/sitters/accepted_listings.html',
                        title="Accepted Listings | Spot",
                        id=id,
                        accepted_listings=accepted_listings,
                        user = current_user)
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

# Accept or unaccept listing with id listing_id 
@app.route('/listings/<int:listing_id>/accept')
@login_required
def listing_accept(listing_id):
    logger.trace('Attempting user {0} acceptance of listing {1}'.format(current_user.id, listing_id))

    if not current_user.is_sitter:
        logger.debug('User {0} failed to accept listing {1}: not a sitter'.format(current_user.id, listing_id))
        return redirect(url_for('error', error='You must be a sitter to accept a listing.'))

    errorMsg = db_service.accept_listing(current_user.id, listing_id)
    if errorMsg != '':
        logger.debug('User {0} failed to accept listing {1}: {2}'.format(current_user.id, listing_id, errorMsg))
        return redirect(url_for('error', error='Could not accept listing: {0}'.format(errorMsg)))

    logger.debug('User {0} accepted listing {1} successfully'.format(current_user.id, listing_id))
    return redirect(url_for('listing_details', listing_id = listing_id))

@app.route('/error')
def error():
    error = request.args.get('error') or ''
    
    return redirect(url_for('home'))