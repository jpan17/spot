from app import app
from app import db_service
from flask import make_response, render_template, request
from flask import url_for, redirect
from app.models import User, Listing
import enums
from datetime import datetime

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
        return redirect(url_for('owner_home', id=user.id))
        # return owner_home(user)
    elif user.is_sitter:
        return redirect(url_for('sitter_home', id=user.id))
    else:
        return ''

# Registration page.
@app.route('/register')
def register_form():
    html = render_template('users/register.html',
        title='Register | Spot')
    response = make_response(html)
    return response

@app.route('/register', methods=['POST'])
def register_user():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone_number = request.form.get('password')
    # print(request.form.get('user_type'))
    is_owner = request.form.get('user_type') == 'owner'
    is_sitter = not is_owner
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    # if password != confirm_password:
    #     html = render_template('users/register.html',
    #                             title='Register | Spot')
    #     response = make_response(html)
    #     return response

    user = User()
    user.full_name = full_name
    user.email = email
    user.phone_number = phone_number
    user.is_owner = is_owner
    user.is_sitter = is_sitter
    user.password_hash = password
    
    new_user = db_service.create_user(user)
    if new_user != '':
        print(new_user)
    else:
        print('Created a new user ', user.full_name)
    
    html = render_template('users/login.html',
                            title='Login | Spot')
    response = make_response(html)
    return response 

@app.route('/owner/<int:id>')
def owner_home(id):
    user = db_service.get_user_by_id(id)
    first_name = user.full_name.split()[0]
    listings = db_service.get_user_listings(user,id)
    html = render_template('users/owner_home.html',
                           title=first_name+" | Spot",
                           id=id,
                           listings=listings,
                           listings_len=len(listings))
    response = make_response(html)
    return response

@app.route('/sitter/<int:id>')
def sitter_home(id):
    user = db_service.get_user_by_id(id)
    first_name = user.full_name.split()[0]
    html = render_template('users/sitter_home.html',
                           title=first_name+" | Spot",
                           id=id)
    response = make_response(html)
    return response

@app.route('/newlisting/<int:id>')
def new_listing(id):
    pet_types = enums.pet_types
    activities = enums.activities
    pet_types_len = len(pet_types)
    activities_len = len(activities)
    
    html = render_template('listings/new_listing.html',
                         title="New Listing | Spot",
                         id=id,
                         pet_types=pet_types,
                         pet_types_len=pet_types_len,
                         activities=activities,
                         activities_len=activities_len)
    response = make_response(html)
    return response

@app.route('/owner/<int:id>', methods=['POST'])
def create_listing(id):
    
    activities = []
    for activity in enums.activities:
        if request.form.get('activity-{0}'.format(activity)) == 'True':
            activities.append(activity)
    
    listing = Listing(
        pet_name=request.form.get('pet_name'),
        pet_type=request.form.get('pet_type'),
        start_time=datetime.fromisoformat(request.form.get('start_time')),
        end_time=datetime.fromisoformat(request.form.get('end_time')),
        full_time=bool(request.form.get('full_time')),
        zip_code=request.form.get('zip_code'),
        extra_info=request.form.get('extra_info'),
        activities=activities,
        user_id=id)
    
    new_listing = db_service.create_listing(listing)
    
    if new_listing == '':
        return redirect(url_for('owner_home', id=id))
    else:
        print("Listing not created")
        return ''
    