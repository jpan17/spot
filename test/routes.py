from app import app, db
from app.models import User, Listing
from flask import render_template, make_response
from flask import request, redirect
from flask import url_for
import enums

TITLE = 'Spot Testing Environment'

# Homepage with a list of users and some display of listings (hopefully)
@app.route('/')
@app.route('/index')
def index():
    # errorMsg in case we need to display anything there
    errorMsg = request.args.get('errorMsg') or ''

    # Get all the users, so we can display in table
    users = User.query.all()
    users_len = len(users)

    # Make and return response (note that the templates folder is
    # in this (test) directory)
    html = render_template('index.html',
        errorMsg=errorMsg,
        users=users,
        users_len=users_len,
        title = TITLE)
    response = make_response(html)
    return response

@app.route('/clear')
def clear_db():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    return redirect(url_for('index',errorMsg='Database successfully cleared.'))

# Form for creating new users (basic)
# I think it may be best for actual production code, if we use Flask, to have separate files for
# routes for e.g. users, listings, etc
@app.route('/users/new')
def new_user():
    # Make and return response
    html = render_template('users/new_user.html',
        title=TITLE)
    response = make_response(html)
    return response

# Endpoint for creation of new users (when submit button is pressed
# from the new_user page)
@app.route('/users/create', methods=['POST'])
def create_user():
    # Create user from the arguments passed via POST
    user = User(
        is_sitter=bool(request.form.get('is_sitter')),
        is_owner=bool(request.form.get('is_owner')),
        full_name=request.form.get('full_name'),
        email=request.form.get('email'),
        phone_number=request.form.get('phone_number'),
        password_hash=request.form.get('password_hash'),
    )

    # NOTE: This is where we can validate that full_name, email,
    # phone_number, and password_hash are valid immediately before adding to database

    errorMsg = ''

    # Add user to session, and commit to finish transaction (basically push changes to database)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback() # Cancel all invalid changes
        errorMsg = e.args[0]

    # Redirect to main page
    return redirect(url_for('index', errorMsg=errorMsg))

# Delete user with certain id
@app.route('/users/delete/<int:id>')
def delete_user(id):
    errorMsg = 'Deleted successfully'

    # Find user by ID, and delete it
    try:
        User.query.filter_by(id=id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        errorMsg = e.args[0]

    return redirect(url_for('index', errorMsg=errorMsg))

# User Details
@app.route('/users/<int:id>')
def user_details(id):
    errorMsg = request.args.get('errorMsg') or ''

    # Get user by id
    try:
        user = User.query.filter_by(id=id).one()
    except Exception as e:
        errorMsg = 'User does not exist'
        html = render_template('users/user_details.html',
            title=TITLE, errorMsg=errorMsg, user=None)
        response = make_response(html)
        return response

    # Set listings and accepted listings if applicable
    listings = []
    accepted_listings = [] # Currently unused
    if user.is_owner:
        listings = user.listings
    if user.is_sitter:
        accepted_listings = user.accepted_listings
    # For some reason, can't use len in templates, so here:
    listings_len = len(listings)
    accepted_listings_len = len(accepted_listings)

    # Make and return response
    html = render_template('users/user_details.html',
        title=TITLE,
        user=user,
        listings=listings,
        listings_len=listings_len,
        accepted_listings=accepted_listings,
        accepted_listings_len=accepted_listings_len,
        errorMsg=errorMsg)
    response = make_response(html)
    return response
    
# Form for creating new listings (basic)
@app.route('/users/<int:id>/listings/new')
def new_listing(id):
    # Get enums for the form
    pet_types = enums.pet_types
    activities = enums.activities
    pet_types_len = len(pet_types)
    activities_len = len(activities)

    # Make and return response
    html = render_template('listings/new_listing.html',
        title=TITLE,
        id=id,
        pet_types=pet_types,
        pet_types_len=pet_types_len,
        activities=activities,
        activities_len=activities_len)
    response = make_response(html)
    return response

# Form for creating new listings (basic)
@app.route('/listings/update/<int:listing_id>')
def update_listing_form(listing_id):
    # Get enums for the form
    pet_types = enums.pet_types
    activities = enums.activities
    pet_types_len = len(pet_types)
    activities_len = len(activities)

    # get old listing details
    old_listing = Listing.query.filter_by(id = listing_id).first()
    start_time = str(old_listing.start_time).replace(" ", "T")
    end_time = str(old_listing.end_time).replace(" ", "T")

    # Make and return response
    html = render_template('listings/update_listing.html',
        title=TITLE,
        id=listing_id,
        pet_types=pet_types,
        pet_types_len=pet_types_len,
        activities=activities,
        activities_len=activities_len,
        listing = old_listing,
        start_time = start_time,
        end_time = end_time
        )
    response = make_response(html)
    
    return response

# Receives data for updated listing and update it
@app.route('/listings/<int:listing_id>/change', methods = ['POST'])
def update_listing(listing_id):
    errorMsg = 'Listing Updated Successfully'
    
    activities = []
    # Get activities based on form (blegh arrays) (yeah blegh arrays)
    for activity in enums.activities:
        if request.form.get('activity-{0}'.format(activity)) == 'True':
            activities.append(activity)

    try:
        # get the listing that you're trying to update
        listing = Listing.query.filter_by(id = listing_id).first()
        
        # update the fields in the old listing
        listing.pet_name = request.form.get('pet_name')
        listing.pet_type = request.form.get('pet_type')
        listing.start_time = request.form.get('start_time')
        listing.end_time = request.form.get('end_time')
        listing.full_time = bool(request.form.get('full_time'))
        listing.zip_code = request.form.get('zip_code')
        listing.extra_info = request.form.get('extra_info')
        listing.activities = activities
        db.session.commit()
        
    except Exception as e:
        db.session.rollback() # Cancel all invalid changes
        errorMsg = e.args[0]
        
    return redirect(url_for('user_details', id=listing.user_id, errorMsg=errorMsg))


# Receives data for new listing and creates it
@app.route('/users/<int:user_id>/listings/create', methods=['POST'])
def create_listing(user_id):
    errorMsg = 'Listing Created Successfully'
    
    activities = []
    # Get activities based on form (blegh arrays)
    for activity in enums.activities:
        if request.form.get('activity-{0}'.format(activity)) == 'True':
            activities.append(activity)

    # Create listing from form data
    listing = Listing(
        pet_name=request.form.get('pet_name'),
        pet_type=request.form.get('pet_type'),
        start_time=request.form.get('start_time'),
        end_time=request.form.get('end_time'),
        full_time=bool(request.form.get('full_time')),
        zip_code=request.form.get('zip_code'),
        extra_info=request.form.get('extra_info'),
        activities=activities,
        user_id=user_id)

    try:
        db.session.add(listing)
        db.session.commit()
    except Exception as e:
        db.session.rollback() # Cancel all invalid changes
        errorMsg = e.args[0]

    return redirect(url_for('user_details', id=user_id, errorMsg=errorMsg))

    
# Delete listing with certain id
@app.route('/listings/delete/<int:id>')
def delete_listing(id):
    errorMsg = 'Deleted successfully'

    # Find user by ID, and delete it
    try:
        Listing.query.filter_by(id=id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        errorMsg = e.args[0]

    return redirect(url_for('user_details', id = id, errorMsg=errorMsg))