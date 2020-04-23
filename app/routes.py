from app import app, login_manager
from app import db_service
from app.logger import Logger
from flask import Flask
from flask import make_response, render_template, request, session
from flask import url_for, redirect, flash
from flask_login import UserMixin, login_required, current_user, login_user, logout_user
from app.models import User, Listing
from app.token import generate_confirmation_token, confirm_token
from app.email import send_email
from werkzeug.utils import secure_filename
from werkzeug.security import pbkdf2_hex
import enums
import os
from datetime import datetime

logger = Logger() 
login_manager.login_view = 'login_form'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# determines which home page to route to based on current_user (login, sitter_home, owner_home)
@app.route('/', methods=['GET'])
@login_required
def home():

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
        
        filtered_activities = []
        for activity in enums.activities:
            if request.args.get('activity_{0}'.format(activity.lower().replace(' ', '_'))) == 'true':
                filtered_activities.append(activity)
    
        filtered_pet_types = []
        for pet_type in enums.pet_types:
            if request.args.get('pet_type_{0}'.format(pet_type.lower().replace(' ', '_'))) == 'true':
                filtered_pet_types.append(pet_type)
        
        if len(filtered_activities) == 0:
            filtered_activities = None
            
        if len(filtered_pet_types) == 0:
            filtered_pet_types = None
            
        zip_code=request.args.get('zip_code')
        
        if zip_code == '':
            zip_code = None

        logger.debug('Query with activities', filtered_activities, ', pet_types', filtered_pet_types, ', and zip code', zip_code, 'made by user', current_user.id)
    
        all_listings = db_service.all_listings(pet_types=filtered_pet_types, activities=filtered_activities, zip_code=zip_code)
        
        html = render_template('users/sitters/home.html',
                            title="Home | Spot",
                            listings=all_listings,
                            listings_len=len(all_listings),
                            pet_types=enums.pet_types,
                            pet_types_len=len(enums.pet_types),
                            activities=enums.activities,
                            activities_len=len(enums.activities),
                            filtered_activities=filtered_activities,
                            filtered_pet_types=filtered_pet_types,
                            zip_code=zip_code,
                            user = current_user)
        
        response = make_response(html)
        return response

    return redirect(url_for('error', error='User is neither owner nor sitter. Please create a new user instead.'))

# apparently necessary, crashes program if removed. Just following what flask says.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login form (for separation from homepage)
@app.route('/login')
def login_form():
    logger.trace('Login form accessed')

    errorMsg = request.args.get('error') or ''

    html = render_template('users/login.html',
        title='Login | Spot',
        errorMsg=errorMsg)
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
    is_confirmed = user.confirmed

    if passwordMatch:
        if is_confirmed:
            login_user(user)
            logger.debug('Logged in user with email', email)
            return redirect(url_for('home'))
        else:
            logger.debug('User with email', email, 'attempted login prior to email confirmation')
            return redirect(url_for('resend_confirmation_landing', user_id=user.id))

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
    
    errorMsg = request.args.get('error') or ''

    html = render_template('users/register.html',
        title='Register | Spot',
        errorMsg=errorMsg)
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
    user.confirmed = False
    
    try:
        logger.debug('Attempting to persist user:', user)
        new_user = db_service.create_user(user)
        if type(new_user) == str:
            logger.info('Error occurred creating user:', new_user)
            return redirect(url_for('register_form', error='Email or phone number already exists.'))
        else:
            logger.info('Created a new user with id', new_user.id)
            token = generate_confirmation_token(new_user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('users/activate.html', confirm_url=confirm_url)
            subject = "Confirm your email to create your Spot account"
            send_email(new_user.email, subject, html)
            
        return redirect(url_for('login_form'))
    except Exception as e:
        logger.warn('Error occurred creating user:', str(e))
        return redirect(url_for('register_form', error=str(e)))

@app.route('/resend-confirmation')
def resend_confirmation_landing():
    user_id = request.args.get('user_id') or ''
    logger.trace('Resend confirmation landing page accessed with user id', user_id)

    if user_id == '':
        return redirect(url_for('login_form'))

    html = render_template('users/unconfirmed_login.html',
                            title="Error | Spot",
                            user_id=user_id)
    response = make_response(html)
    return response

@app.route('/resend-confirmation/<user_id>')
def resend_confirmation(user_id):
    logger.trace('Resend confirmation email about to be attempted for user with id', user_id)
    user = db_service.get_user_by_id(user_id)
    if user is not None:
        logger.trace('Attempting to resend confirmation email to user', user_id)
        try:
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('users/activate.html', confirm_url=confirm_url)
            subject = "Confirm your email to create your Spot account"
            send_email(user.email, subject, html)
            logger.debug('Resent confirmation email to user', user_id)
        except Exception as e:
            logger.warn('Failed to resend confirmation email to user {0}: {1}'.format(user_id, str(e)))
            return redirect(url_for('error', error='Failed to resend confirmation email: {0}'.format(str(e))))
    else:
        logger.info('Attempted to resend confirmation email to non-existent user with id', user_id)
        return redirect(url_for('error', error='Failed to resend confirmation email: user does not exist with id {0}'.format(user_id)))

    return redirect(url_for('login_form'))

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        db_service.confirm_user(user)
        flash('You have confirmed your account. Thanks!', 'success')
        
    return redirect(url_for('login_form'))
    

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
        logger.info('Non-owner {0} attempted to create a listing'.format(current_user.id))
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
    
    pet_image_file = None
    pet_image_url = None
    
    if 'pet_image' in request.files:
        pet_image_file = request.files['pet_image']
        if pet_image_file.filename != '' and allowed_file(pet_image_file.filename):
            parts_of_filename = secure_filename(pet_image_file.filename).split('.')
            filename = '.'.join([pbkdf2_hex('.'.join(parts_of_filename[:-1]), app.config['SECURITY_PASSWORD_SALT']), parts_of_filename[len(parts_of_filename) - 1]])
            pet_image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pet_image_url = url_for('static', filename=os.path.join('/'.join(app.config['UPLOAD_FOLDER'].split('/')[1:]), filename), _external= True)

    
    listing = Listing(
        pet_name=pet_name,
        pet_type=pet_type,
        start_time=start,
        end_time=end,
        full_time=True,
        zip_code=zip_code,
        pet_image_url=pet_image_url,
        extra_info=extra_info,
        activities=activities,
        user_id=current_user.id)

    try:
        logger.debug('Attempting to persist listing with fields: (pet_name={0},pet_type={1},start_time={2},end_time={3},full_time={4},zip_code={5},pet_image_url={6},extra_info={7},activities={8},user_id={9})'.format(
            pet_name,
            pet_type,
            start.isoformat(),
            end.isoformat(),
            True,
            zip_code,
            pet_image_url,
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
        logger.info('User {0} attempted to access update form for non-existent listing {1}'.format(current_user.id, listing_id))
        return redirect(url_for('error', error='Listing not found.'))
    if listing.user_id != current_user.id:
        logger.info('User {0} attempted to access update form for other user\'s listing {1}'.format(current_user.id, listing_id))
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
        logger.INFO('User {0} attempted to update non-existent listing {1}'.format(current_user.id, listing_id))
        return redirect(url_for('error', error='Listing not found.'))
    if listing.user_id != current_user.id:
        logger.info('User {0} attempted to update other user\'s listing {1}'.format(current_user.id, listing_id))
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
        logger.info('User {0} failed to accept listing {1}: not a sitter'.format(current_user.id, listing_id))
        return redirect(url_for('error', error='You must be a sitter to accept a listing.'))

    errorMsg = db_service.accept_listing(current_user.id, listing_id)
    if errorMsg != '':
        logger.warn('User {0} failed to accept listing {1}: {2}'.format(current_user.id, listing_id, errorMsg))
        return redirect(url_for('error', error='Could not accept listing: {0}'.format(errorMsg)))

    logger.info('User {0} accepted listing {1} successfully'.format(current_user.id, listing_id))
    sitter_subject = "You accepted a Spot request!"
    listing = db_service.get_listing_by_id(listing_id)
    pet_name = listing.pet_name
    sitter_html = render_template('users/sitters/accepted_email.html', 
                                  sitter_name=current_user.full_name, 
                                  pet_name=pet_name)
    send_email(current_user.email, sitter_subject, sitter_html)
    print("here")
    owner_subject = current_user.full_name + " accepted your listing for " + pet_name + "!"
    owner = db_service.get_user_by_id(listing.user_id)
    owner_name = owner.full_name
    owner_html = render_template('users/owners/accepted_email.html',
                                 pet_name=pet_name,
                                 sitter_email=current_user.email,
                                 sitter_name=current_user.full_name,
                                 owner_name=owner_name)
    
    print(owner.email)
    send_email(owner.email, owner_subject, owner_html)
    return redirect(url_for('listing_details', listing_id = listing_id))

@app.route('/error')
def error():
    error = request.args.get('error') or ''
    if current_user.get_id() is not None:
        userStr = 'user {0}'.format(current_user.id)
    else:
        userStr = 'anonymous user'

    logger.info('Error page reached/accessed by', userStr, 'with error:', error)
    
    html = render_template('users/error.html',
                            title="Error | Spot",
                            error = error,
                            user = current_user)
    response = make_response(html)
    return response