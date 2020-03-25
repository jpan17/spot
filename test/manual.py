import os
import sys
from app import db
from app.models import User, Listing

# Some valid objects, some invalid objects (note that they must be inserted in order, otherwise
# some invalid ones may be valid and vice versa because this tests duplicate field errors)
users = {

    'valid_owner1': User(is_owner=True, 
        full_name='Joe Schmoe',
        email='joe_schmoe@gmail.com',
        phone_number='123-456-7890',
        password_hash='fweaoif@!#$REFGB'),

    'valid_sitter1': User(is_owner=True, 
        full_name='Joe Schmoe',
        email='jschmoe@princeton.edu',
        phone_number='609-333-3333',
        password_hash='afevidhsoq3fovih'),

    # Missing phone number
    'invalid_owner1': User(is_owner=True,
        full_name='Joe Schmoe',
        email='joe_schmoe2@gmail.com',
        password_hash='asdfiewfh$#RTGD'),

    # Duplicate email
    'invalid_sitter1': User(is_sitter=True,
        full_name='Jack Imposter',
        email='joe_schmoe@gmail.com',
        phone_number='333-445-2260',
        password_hash='asdfiewfh$#RTGD')
}

default_stdout = None

# Runs tests on correctness of direct database operations, optionally clearing before and after running the tests
def run_tests(clear_before = True, clear_after = True):
    # Save stdout so we can enable it later on
    global default_stdout
    default_stdout = sys.stdout
    _disable_stdout()

    # Clears the database to avoid undesired duplicate key issues
    if clear_before:
        _clear_data(db.session)
        _print()

    # Run tests
    valid_user_errors = []
    invalid_user_errors = []
    _test_create_valid_user('valid_owner1', valid_user_errors)
    _test_create_valid_user('valid_sitter1', valid_user_errors)
    _test_create_invalid_user('invalid_owner1', invalid_user_errors)
    _test_create_invalid_user('invalid_sitter1', invalid_user_errors)

    # Display errors
    _enable_stdout()
    print()

    # Valid user errors
    if len(valid_user_errors) == 0:
        print('Valid user creation tests passed')
    else:
        msg = 'Valid user creation tests failed with {0} failures'.format(len(valid_user_errors))
        print('=' * len(msg))
        print(msg)
        print('=' * len(msg))
        for error in valid_user_errors:
            print('Test for creation of user {0} failed with error message:\n{1}'.format(error[0], error[1].args[0]))

    # Invalid user errors
    if len(invalid_user_errors) == 0:
        print('Invalid user creation tests passed')
    else:
        msg = 'Invalid user creation tests failed with {0} failures'.format(len(valid_user_errors))
        print('=' * len(msg))
        print(msg)
        print('=' * len(msg))
        for error in invalid_user_errors:
            print('Test for creation of user {0} failed.'.format(error))

    if clear_after:
        _print()
        _clear_data(db.session)
    

# Tests creation of a valid user. Does not do anything to errors if successfully created and
# appends a tuple with the key associated with the user and the exception thrown if creation failed.
def _test_create_valid_user(key, errors):
    _print('Creating new valid user {0}...'.format(key))
    try:
        db.session.add(users[key])
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        errors.append((key, e))

# Tests creation of an invalid user. Returns None if creation fails (which is the expected result) 
# and returns the key associated with the user if creation succeeded (incorrect outcome).
def _test_create_invalid_user(key, errors):
    _print('Creating new invalid user {0}...'.format(key))
    try:
        db.session.add(users[key])
        db.session.commit()
        errors.append(key)
    except Exception as e:
        db.session.rollback()

# Clears the database referenced by database session 'session'
def _clear_data(session):
    _print('Clearing database...')

    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()

# Disables stdout
def _disable_stdout():
    f = open(os.devnull, 'w')
    sys.stdout = f

# Enables stdout
def _enable_stdout():
    sys.stdout = default_stdout

# Enables stdout, prints, then disables stdout
def _print(msg=''):
    _enable_stdout()
    print(msg)
    _disable_stdout()