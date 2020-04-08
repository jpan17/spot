from app import app
from app import db_service
from flask import make_response, render_template, request
from flask import url_for, redirect
import enums

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
    html = render_template('users/owners/listing_new.html',
        title='New Listing | Spot',
        pet_types=enums.pet_types,
        activities=enums.activities)
    response = make_response(html)
    return response

@app.route('/listings/<int:listing_id>')
def listing_details(listing_id):
    listing = db_service.get_listing_by_id(listing_id)
    if listing == None:
        return redirect(url_for('error', error='Listing not found.'))

    html = render_template('users/owners/listing_details.html',
        title='Listing Details | Spot',
        listing=listing)
    response = make_response(html)
    return response

@app.route('/listings/<int:id>/accepted')
def accepted_listings(id):
    user = db_service.get_user_by_id(id)
    if user is not None:
        accepted_listings = db_service.get_user_listings(user = user, accepted = True)
        html = render_template('users/sitters/accepted_listings.html',
                            title="Accepted Listings | Spot",
                            id=id,
                            accepted_listings=accepted_listings)
        response = make_response(html)
        return response
    else:
        return redirect(url_for('error', error='User does not exist.'))

@app.route('/listings/<int:listing_id>/delete')
def listing_delete(listing_id):
    return redirect(url_for('home'))

@app.route('/listings/<int:listing_id>/update')
def listing_update(listing_id):
    return redirect(url_for('home'))

@app.route('/error')
def error():
    error = request.args.get('error') or ''
    
    return redirect(url_for('home'))