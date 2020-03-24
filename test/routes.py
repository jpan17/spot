from app import app, db
from app.models import User, Listing
from flask import render_template, make_response
from flask import request, redirect
from flask import url_for

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
        errorMsg = e.args[0]

    return redirect(url_for('index', errorMsg=errorMsg))

# User Details
@app.route('/users/<int:id>')
def user_details(id):
    return None