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
    logger.trace('Login form accessed')

    html = render_template('users/login.html',
        title='Login | Spot')
    response = make_response(html)
    return response   

# processes login info and redirects to appropriate page (login, sitter home, owner home)
@app.route('/login', methods=['POST'])
def login():
    logger.trace('Attempting to login user with email', request.form.get('email'))

    email = request.form.get('email')
    password = request.form.get('password')
    user = db_service.get_user_by_email(email)

    # As much as I like descriptive error messages, it's been a while since I've seen a site specify which one of email and password is wrong.
    # My guess is it's for security purposes, so I'm just going to not specify which is incorrect.
    if user is None:
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
    logger.trace('Logging out user', current_user.id)
    logout_user()
    response = redirect(url_for('login_form'))
    return response

# Registration page with the form
@app.route('/register')
def register_form():
    logger.trace('Register form accessed')
    
    html = render_template('users/register.html',
        title='Register | Spot')
    response = make_response(html)
    return response

# registers the user and redirects to login page
@app.route('/register', methods=['POST'])
def register_user():
    logger.trace('User attempting to register with fields', request.form)

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
    
    try:
        logger.debug('Attempting to persist user:', user)
        new_user = db_service.create_user(user)
        if type(new_user) == str:
            logger.info('Error occurred creating user:', new_user)
            return redirect(url_for('register_form', error='Email or phone number already exists.'))
        else:
            logger.info('Created a new user with id', new_user.id)
    
        return redirect(url_for('login_form'))
    except Exception as e:
        logger.warn('Error occurred creating user:', str(e))
        return redirect(url_for('register_form', error=str(e)))

# haven't touched yet, but idt needs cookies. 
@app.route('/listings/new')
@login_required
def listing_new():
    logger.trace('User', current_user.id, 'accessed new listing form')

    html = render_template('users/owners/listing_form.html',
        title='New Listing | Spot',
        pet_types=enums.pet_types,
        activities=enums.activities,
        user = current_user)
    
    response = make_response(html)
    return response

@app.route('/listings/new', methods=['POST'])
@login_required
def listing_new_endpoint():
    logger.trace('User', current_user.id, 'attempting to create new listing with form values', str(request.form))
    if not current_user.is_owner:
        logger.warn('Non-owner {0} attempted to create a listing'.format(current_user.id))
        return redirect(url_for('error', error='User must be owner to create a listing'))
    
    activities = []
    for activity in enums.activities:
        if request.form.get('activity_{0}'.format(activity.lower().
                                                  replace(' ', '_'))) == 'true':
            activities.append(activity)
    
    pet_name = request.form.get('pet_name')
    # split and construct start_date
    start_date = request.form.get('start_date')
    start_time = request.form.get('start_time')
    start_date_array = start_date.split('/')
    start_time_array = start_time.split(':')
    
    start = datetime(int(start_date_array[2]), int(start_date_array[0]),
                              int(start_date_array[1]), int(start_time_array[0]),
                              int(start_time_array[1]))    
    
    # split and construct end_date
    end_date = request.form.get('end_date')
    end_time = request.form.get('end_time')
    end_date_array = end_date.split('/')
    end_time_array = end_time.split(':')
    
    end = datetime(int(end_date_array[2]), int(end_date_array[0]),
                              int(end_date_array[1]), int(end_time_array[0]),
                              int(end_time_array[1]))
    
    pet_type = request.form.get('pet_type')
    zip_code = request.form.get('zip_code')
    extra_info = request.form.get('extra_info')
    
    listing = Listing(
        pet_name=pet_name,
        pet_type=pet_type,
        start_time=start,
        end_time=end,
        full_time=True,
        zip_code=zip_code,
        extra_info=extra_info,
        activities=activities,
        user_id=current_user.id)

    try:
        logger.debug('Attempting to persist listing with fields: (pet_name={0},pet_type={1},start_time={2},end_time={3},full_time={4},zip_code={5},extra_info={6},activities={7},user_id={8})'.format(
            pet_name,
            pet_type,
            start.isoformat(),
            end.isoformat(),
            True,
            zip_code,
            extra_info,
            activities,
            current_user.id
        ))
        new_listing = db_service.create_listing(listing)
        
        if type(new_listing) != str:
            logger.info('Listing created for user {0} with id {1}'.format(current_user.id, new_listing.id))
            return redirect(url_for('listing_details', listing_id=new_listing.id))
        else:
            logger.warn('Listing creation failed for user {0}: {1}'.format(current_user.id, new_listing))
            return redirect(url_for('error', error='Listing creation failed: {0}'.format(new_listing)))
    
    except Exception as e:
        logger.warn('Listing creation failed for user {0}: {1}'.format(current_user.id, str(e)))
        return redirect(url_for('error', error='Listing creation failed: {0}'.format(str(e))))

# might be okay to have listing id in the url
@app.route('/listings/<int:listing_id>')
@login_required
def listing_details(listing_id):
    logger.trace('User', current_user.id, 'accessing details for listing', listing_id)

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
    logger.trace('User', current_user.id, 'accessing accepted listings')

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
    logger.trace('User', current_user.id, 'attempting to delete listing', listing_id)

    result = db_service.delete_listing(listing_id)
    if result != '':
        logger.warn('User', current_user.id, 'failed to delete listing', listing_id)
        return redirect(url_for('error', error='Listing deletion failed: {0}'.format(result)))
    logger.info('User', current_user.id, 'deleted listing', listing_id)
    return redirect(url_for('home'))

# implemented once update funcitonality added
@app.route('/listings/<int:listing_id>/update')
@login_required
def listing_update(listing_id):
    logger.trace('User', current_user.id, 'accessing form to update listing', listing_id)

    listing = db_service.get_listing_by_id(listing_id)
    if listing is None:
        logger.warn('User {0} attempted to access update form for non-existent listing {1}'.format(current_user.id, listing_id))
        return redirect(url_for('error', error='Listing not found.'))
    if listing.user_id != current_user.id:
        logger.warn('User {0} attempted to access update form for other user\'s listing {1}'.format(current_user.id, listing_id))
        return redirect(url_for('error', error='Listing is owned by a different user.'))

    html = render_template('users/owners/listing_form.html',
        title='New Listing | Spot',
        pet_types=enums.pet_types,
        activities=enums.activities,
        user = current_user,
        listing = listing)
    
    response = make_response(html)
    return response

@app.route('/listings/<int:listing_id>/update', methods=['POST'])
@login_required
def listing_update_endpoint(listing_id):
    logger.trace('User', current_user.id, 'attempting to update listing', listing_id)

    listing = db_service.get_listing_by_id(listing_id)
    if listing is None:
        logger.warn('User {0} attempted to update non-existent listing {1}'.format(current_user.id, listing_id))
        return redirect(url_for('error', error='Listing not found.'))
    if listing.user_id != current_user.id:
        logger.warn('User {0} attempted to update other user\'s listing {1}'.format(current_user.id, listing_id))
        return redirect(url_for('error', error='Listing is owned by a different user.'))

    activities = []
    for activity in enums.activities:
        if request.form.get('activity_{0}'.format(activity.lower().
                                                  replace(' ', '_'))) == 'true':
            activities.append(activity)
    
    pet_name = request.form.get('pet_name')
    # split and construct start_date
    start_date = request.form.get('start_date')
    start_time = request.form.get('start_time')
    start_date_array = start_date.split('/')
    start_time_array = start_time.split(':')
    
    start = datetime(int(start_date_array[2]), int(start_date_array[0]),
                              int(start_date_array[1]), int(start_time_array[0]),
                              int(start_time_array[1]))    
    
    # split and construct end_date
    end_date = request.form.get('end_date')
    end_time = request.form.get('end_time')
    end_date_array = end_date.split('/')
    end_time_array = end_time.split(':')
    
    end = datetime(int(end_date_array[2]), int(end_date_array[0]),
                              int(end_date_array[1]), int(end_time_array[0]),
                              int(end_time_array[1]))
    
    pet_type = request.form.get('pet_type')
    zip_code = request.form.get('zip_code')
    extra_info = request.form.get('extra_info')

    try:
        new_listing = db_service.update_listing(listing_id,
            pet_name=pet_name,
            pet_type=pet_type,
            start_time=start,
            end_time=end,
            full_time=True,
            zip_code=zip_code,
            extra_info=extra_info,
            activities=activities)
        
        if type(new_listing) != str:
            logger.info('Listing updated for user {0} with id {1}'.format(current_user.id, new_listing.id))
            return redirect(url_for('listing_details', listing_id=new_listing.id))
        else:
            logger.warn('Listing update failed for user {0}: {1}'.format(current_user.id, new_listing))
            return redirect(url_for('error', error='Listing update failed: {0}'.format(new_listing)))
    
    except Exception as e:
        logger.warn('Listing update failed for user {0}: {1}'.format(current_user.id, str(e)))
        return redirect(url_for('error', error='Listing update failed: {0}'.format(str(e))))


# Accept or unaccept listing with id listing_id 
@app.route('/listings/<int:listing_id>/accept')
@login_required
def listing_accept(listing_id):
    logger.trace('Attempting user {0} acceptance of listing {1}'.format(current_user.id, listing_id))

    if not current_user.is_sitter:
        logger.warn('User {0} failed to accept listing {1}: not a sitter'.format(current_user.id, listing_id))
        return redirect(url_for('error', error='You must be a sitter to accept a listing.'))

    errorMsg = db_service.accept_listing(current_user.id, listing_id)
    if errorMsg != '':
        logger.warn('User {0} failed to accept listing {1}: {2}'.format(current_user.id, listing_id, errorMsg))
        return redirect(url_for('error', error='Could not accept listing: {0}'.format(errorMsg)))

    logger.info('User {0} accepted listing {1} successfully'.format(current_user.id, listing_id))
    return redirect(url_for('listing_details', listing_id = listing_id))

@app.route('/error')
def error():
    error = request.args.get('error') or ''
    if current_user.get_id() is not None:
        userStr = 'user {0}'.format(current_user.id)
    else:
        userStr = 'anonymous user'

    logger.warn('Error page reached/accessed by', userStr, 'with error:', error)
    return redirect(url_for('home'))