"""
db_service.py
=============================================================================
A file containing useful methods for querying the database of Users/Listings,
specifically methods that will be used throughout the application.
 """

from app import app, db
from app.models import User, Listing
from datetime import datetime
import enums

# TODO: Add specific validation such as empty strings, valid format for phone number, email, etc into functions!

def user_exists(user_id):
    """
    Returns True if a User object exists with ID *user_id*, or False otherwise.

    Parameters
    ----------
    user_id : int or str
        ID of the User

    Returns
    -------
    bool
        True if a User object exists with ID *user_id*, or False otherwise

    Raises
    ------
    TypeError
        If *user_id* is not an integer or string.
    ValueError
        If *user_id* is a string that cannot be parsed to an integer.

    Examples
    --------
    >>> db_service.user_exists(3)
    True

    >>> db_service.user_exists('-1')
    False

    >>> db_service.user_exists([2, 4, 6])
    TypeError('user_id must be an integer or string')

    """

    id = user_id

    if type(user_id) != int:
        if type(user_id) != str:
            raise TypeError('user_id must be an integer or string')
        else:
            if _str_is_integer(user_id):
                id = int(user_id)
            else:
                raise ValueError('user_id is a string, but cannot be parsed into an integer')

    return User.query.filter_by(id=id).scalar() is not None

def listing_exists(listing_id):
    """
    Returns True if a Listing object with ID *listing_id* exists, or False otherwise.

    Parameters
    ----------
    listing_id : int or str
        ID of the Listing

    Returns
    -------
    bool
        True if a Listing object with ID *listing_id* exists, or False otherwise.

    Raises
    ------
    TypeError
        If *listing_id* is not an integer or string.
    ValueError
        If *listing_id* is a string that cannot be parsed to an integer.

    Examples
    --------
    >>> db_service.listing_exists(3)
    True

    >>> db_service.listing_exists('-1')
    False

    >>> db_service.get_listing_by_id([2, 4, 6])
    TypeError('listing_id must be an integer or string')

    """
    id = listing_id

    if type(listing_id) != int:
        if type(listing_id) != str:
            raise TypeError('listing_id must be an integer or string')
        else:
            if _str_is_integer(listing_id):
                id = int(listing_id)
            else:
                raise ValueError('listing_id is a string, but cannot be parsed into an integer')
    
    return Listing.query.filter_by(id=id).scalar() is not None

def get_user_by_id(user_id):
    """
    Returns a User object with ID *user_id*, or None if no such user exists.

    Parameters
    ----------
    user_id : int or str
        ID of the User

    Returns
    -------
    User or None
        The User with ID *user_id* or None if no user exists with that ID

    Raises
    ------
    TypeError
        If *user_id* is not an integer or string.
    ValueError
        If *user_id* is a string that cannot be parsed to an integer.

    Examples
    --------
    >>> db_service.get_user_by_id(3)
    User(id=3)

    >>> db_service.get_user_by_id('-1')
    None

    >>> db_service.get_user_by_id([2, 4, 6])
    TypeError('user_id must be an integer or string')

    """
    id = user_id

    if type(user_id) != int:
        if type(user_id) != str:
            raise TypeError('user_id must be an integer or string')
        else:
            if _str_is_integer(user_id):
                id = int(user_id)
            else:
                raise ValueError('user_id is a string, but cannot be parsed into an integer')

    return User.query.filter_by(id=id).first()


def get_user_by_login(email, password):

    if type(email) != str:
        raise TypeError('email must be string')
    
    if type(password) != str:
        raise TypeError('password must be a string')
    
    user = User.query.filter_by(email=email).first()
    
    if user == None:
        print('No user exists with this email')
        return None
        
    # get_password = user.password_hash
    
    # if password != get_password:
    #     print('incorrect password')
    #     return None
    
    return user    

def get_user_listings(user = None, user_id = -1, accepted = False):
    """
    Returns a list of listings associated with a user. Note that at least one of
    *user* and *user_id* must be specified when calling this function.

    If *user* parameter is given, uses that user directly. If *user* is not
    provided, attempts to get a User by *user_id* instead. *accepted* is used to determine
    which listings to return if a user is both an owner and a sitter and is ignored otherwise.

    Parameters
    ----------
    user : User or None, optional
        The user to return the listings of. Note that one of *user* and *user_id* must
        be specified in a call to this function.
    user_id : int or str, optional
        The ID of the user to return the listings of, if *user* is not specified or None. 
        Note that one of *user* and *user_id* must be specified in a call to this function.
    accepted : bool, optional
        If the user is both an owner and a sitter, the accepted listings will be returned if
        *accepted* is True. Defaults to False, in which case the listings that the user owns
        are returned.

    Returns
    -------
    list of Listing
        A (potentially empty) list of all of the user's Listings. For owners, this is a list of
        their posted Listings; for sitters, a list of their accepted Listings; and for users that are
        both owners and sitters, depends on the value of *accepted* (described above).

    Raises
    ------
    TypeError
        If *user* is not of type User or None, if *user* is None/unspecified and *user_id* 
        is not of type int or str, or if *accepted* is not of type bool.
    ValueError
        If *user* is None/unspecified and *user_id* is a str that cannot be parsed to an int.

    Examples
    --------
    >>> db_service.get_user_listings(User(id=1))
    [<Listing ID=1>, <Listing ID=2>]

    >>> db_service.get_user_listings(user_id='2')
    [<Listing ID=3>]

    >>> db_service.get_user_listings()
    TypeError('No user was provided and no user was found by the given user_id (or no user_id was provided)')

    """

    # If user unspecified, search for it
    if user == None:
        user = get_user_by_id(user_id)
        if user == None:
            raise TypeError('No user was provided and no user was found by the given user_id (or no user_id was provided)')
        
    if type(user) != User:
        raise TypeError('A User object must be passed for the value of parameter "user"')
    
    if type(accepted) != bool:
        raise TypeError('accepted parameter must be of type bool')
    
    if user.is_owner:
        if user.is_sitter:
            if accepted:
                return user.accepted_listings
        return user.listings
    return user.accepted_listings

def all_listings(pet_type = None, activities = None, zip_code = None, datetime_range = None):
    """
    Returns a list of all available Listings in the database, filtered by the given parameters.

    Parameters
    ----------
    pet_type : str or None, optional
        Filters Listings for pet type equal to  *pet_type*, or does not filter is unspecified/None.
    activities : list or tuple of str or None, optional
        Filters Listings for those that share any activity with those in the *activities* parameter,
        or does not filter is unspecified/None.
    zip_code : str or None, optional
        Filters Listings for zip code *containing zip_code*, or does not filter if unspecified/None.
    datetime_range : tuple of datetime or None, optional
        Filters Listings by those that match the *datetime_range* parameter. Must be either None/unspecified
        or a tuple of two datetimes, the first one being the start datetime and the second being the end datetime.
        Looks for listings whose datetime ranges fall completely within the range if *full_time* of the Listing is true, or
        datetime ranges that intersect with *datetime_range* if *full_time* is False.

    Returns
    -------
    list of Listing
        A list of Listings that match the specified paremeters (described above).
    
    Raises
    ------
    TypeError
        If any of the parameters are not of the type described in Parameters above, or if any of the values in *activities* or
        *datetime_range* are not of type str or datetime, respectively.
    ValueError
        If datetime_range is a tuple that does not contain exactly 2 datetimes, the second of which is a datetime that is
        after the first.
        If pet_type is not one of the predefined pet types (defined in enums.py)
        If an activity in activities is not one of the predefined activities (defined in enums.py)

    Examples
    --------
    >>> db_service.all_listings(pet_type = 'Dog', activities = ['Walking'], zip_code = '08540')
    [<Listing ID=15>]
    
    """
    
    if pet_type != None:
        if type(pet_type) != str:
            raise TypeError('pet_type should be a parameter of type None or str')
        if pet_type not in enums.pet_types:
            raise ValueError('Pet Type {0} is not in the list of valid pet types {1}'.format(pet_type, enums.pet_types))

    if activities != None:
        if type(activities) != list and type(activities) != tuple:
            raise TypeError('activities should be a parameter of type None, tuple or list')
        for activity in activities:
            if type(activity) != str:
                raise TypeError('activities tuple/list should only contain str')
            if activity not in enums.activities:
                raise ValueError('Activity {0} is not in the list of valid activities {1}'.format(activity, enums.activities))
    
    if type(zip_code) != str and zip_code != None:
        raise TypeError('zip_code should be a parameter of type None or str')
    
    if datetime_range != None:
        if type(datetime_range) != tuple:
            raise(TypeError('datetime_range should be a parameter of type None or tuple'))
        if len(datetime_range) != 2:
            raise ValueError('datetime_range should contain exactly 2 elements, not {0}'.format(len(datetime_range)))
        for time in datetime_range:
            if type(time) != datetime:
                raise TypeError('datetime_range tuple should only contain datetimes')
        startTime = datetime_range[0]
        endTime = datetime_range[1]
        if startTime >= endTime:
            raise ValueError('start time must be before end time (in datetime_range)')
    
    query = Listing.query

    if pet_type != None:
        query = query.filter_by(pet_type = pet_type)

    if activities != None:
        query = query.filter(Listing.activities_intersect(activities))

    if zip_code != None:
        query = query.filter(Listing.zip_code_contains(zip_code))
    
    if datetime_range != None:
        query = query.filter(Listing.datetime_range_matches(*datetime_range))

    return query.all()

def get_listing_by_id(listing_id):
    """
    Returns a Listing object with ID *listing_id*, or None if no such listing exists.

    Parameters
    ----------
    listing_id : int or str
        ID of the Listing

    Returns
    -------
    Listing or None
        The Listing with ID *listing_id* or None if no listing exists with that ID

    Raises
    ------
    TypeError
        If *listing_id* is not an integer or string.
    ValueError
        If *listing_id* is a string that cannot be parsed to an integer.

    Examples
    --------
    >>> db_service.get_listing_by_id(3)
    Listing(id=3)

    >>> db_service.get_listing_by_id('-1')
    None

    >>> db_service.get_listing_by_id([2, 4, 6])
    TypeError('listing_id must be an integer or string')

    """
    id = listing_id

    if type(listing_id) != int:
        if type(listing_id) != str:
            raise TypeError('listing_id must be an integer or string')
        else:
            if _str_is_integer(listing_id):
                id = int(listing_id)
            else:
                raise ValueError('listing_id is a string, but cannot be parsed into an integer')

    return Listing.query.filter_by(id=id).first()

def create_listing(listing):
    """
    Saves a Listing object (*listing*) to the database, or raises an Exception if *listing* is not a valid Listing.

    Parameters
    ----------
    listing : Listing
        The Listing to be created

    Returns
    -------
    str
        Empty string if creation was successful, otherwise a string containing the error that occurred.

    Raises
    ------
    TypeError
        If *listing* is not of type Listing or any of its attributes are invalid types (see the documentation on Listing
        or the documentation for update_listing for types)
    ValueError
        If any attributes of *listing* have invalid values (see documentation of Listing objects or of update_listing)

    Examples
    --------
    >>> db_service.create_listing(listing)
    ''

    """

    # Raises the appropriate exceptions if anything is wrong with listing
    _check_listing_validity(listing)

    try:
        db.session.add(listing)
        db.session.commit()
        return ''
    except Exception as e:
        db.session.rollback()
        return "Error: " + str(e)

def create_user(user):
    """
    Saves a User object (*user*) to the database, or raises an Exception if *user* is not a valid User.

    Parameters
    ----------
    user : User
        The User to be created

    Returns
    -------
    str
        Empty string if creation was successful, otherwise a string containing the error that occurred.

    Raises
    ------
    TypeError
        If *user* is not of type User or any of its attributes are invalid types (see the documentation on User for types)
    ValueError
        If any attributes of *user* have invalid values (see documentation of User objects)

    Examples
    --------
    >>> db_service.create_user(user)
    ''

    """

    # Raises an exception if user is not valid
    _check_user_validity(user)
    
    try:
        db.session.add(user)
        db.session.commit()
        return ''
    except Exception as e:
        db.session.rollback()
        return "Error: " + str(e)

def update_listing(listing_id, pet_name=None, pet_type=None, start_time=None, end_time=None,
                   full_time=None, zip_code=None, extra_info=None, activities=None):
    """
    Updates a Listing with ID *listing_id* in the database, or raises an Exception if no such listing exists
    or any parameter is invalid (see below).

    Parameters
    ----------
    listing_id : int
        The ID of the Listing to be updated
    pet_name : str or None, optional
        The updated pet name, or None if *pet_name* is not to be updated.
    pet_type : str or None, optional
        The updated pet type (from the list of pet types in enums.py), or None if *pet_type* is not to be updated.
    start_time : datetime or None, optional
        The updated start time, or None if *start_time* is not to be updated.
    end_time : datetime or None, optional
        The updated end time, or None if *end_time* is not to be updated.
    full_time : bool
        The updated value of *full_time* (whether the owner wants a sitter for the full duration or just some part of it), 
        or None if *full_time* is not to be updated.
    zip_code : str or None, optional
        The updated zip code, or None if *zip_code* is not to be updated.
    extra_info : str or None, optional
        The updated extra information, or None if *extra_info* is not to be updated.
    activities : list of str or None, optional
        The updated list of activities (from the list of activites in enums.py), or None if *activities* is not to be updated.

    Returns
    -------
    str
        Empty string if the update was successful, otherwise a string containing the error that occurred.

    Raises
    ------
    TypeError
        If any of the parameters above (or their contents, for the lists/tuples) are not of the correct type
    ValueError
        If no user exists with the ID equal to the updated listing's *user_id* attribute, if start_time is after or the same as
        end_time after updating, or if pet_type or any of the activities are not one of the valid values (described in enums.py).

    Examples
    --------
    >>> update_listing(1, pet_name = 'Spot', zip_code = '08540')
    ''

    """

    listing = get_listing_by_id(listing_id)

    if pet_name != None:
        listing.pet_name = pet_name
    if pet_type != None:
        listing.pet_type = pet_type
    if start_time != None:
        listing.start_time = start_time
    if end_time != None:
        listing.end_time = end_time
    if full_time != None:
        listing.full_time = full_time
    if zip_code != None:
        listing.zip_code = zip_code
    if extra_info != None:
        listing.extra_info = extra_info
    if activities != None:
        listing.activities = activities
            
    _check_listing_validity(listing, check_id = False)

    try:
        db.session.commit()
        return ''
    except Exception as e:
        db.session.rollback()
        return "Error: " + str(e)
    
def delete_listing(listing_id):
    try:
        listing_query = Listing.query.filter_by(id=listing_id)
        listing = listing_query.first()
        listing.sitters = []
        listing_query.delete()
        db.session.commit()
        return ''
    except Exception as e:
        db.session.rollback()
        return e

def delete_user(user_id):
    pass

def accept_listing(user_id, listing_id):
    try:
        listing = Listing.query.filter_by(id = listing_id).first()
        user = User.query.filter_by(id = user_id).first()
        user.accepted_listings.append(listing)
        db.session.commit()
        return ''
    except Exception as e:
        db.session.rollback() # Cancel all invalid changes
        errorMsg = e.args[0]
        return errorMsg

# Can a string be parsed to an integer?
def _str_is_integer(s):
    try:
        int(s)
        return True
    except ValueError as e:
        return False

#========================== VALIDATION FUNCTIONS ==============================

# Raises the appropriate exception for invalid listings and does nothing to valid listings
def _check_listing_validity(listing, check_id = True):
    if type(listing) != Listing:
        raise TypeError('listing parameter must be a Listing object')
    
    if listing.id != None and check_id:
        raise ValueError('listing parameter should not have attribute id')
    
    if type(listing.pet_name) != str:
        raise TypeError('listing parameter attribute pet_name must be of type str')
    
    if type(listing.pet_type) != str:
        raise TypeError('listing parameter attribute pet_type must be of type str')
    
    if listing.pet_type not in enums.pet_types:
        raise ValueError('listing parameter pet_type must be one of the following: {0}'.format(enums.pet_types))
    
    if type(listing.start_time) != datetime:
        raise TypeError('listing parameter start_time must be of type datetime')
    
    if type(listing.end_time) != datetime:
        raise TypeError('listing parameter end_time must be of type datetime')
    
    if listing.start_time >= listing.end_time:
        raise ValueError('start_time must be before end_time')
    
    if type(listing.full_time) != bool:
        raise TypeError('listing parameter full_time must be of type bool')
    
    if type(listing.zip_code) != str:
        raise TypeError('listing parameter zip_code must be of type str')
    
    if type(listing.extra_info) != str and listing.extra_info != None:
        raise TypeError('listing parameter extra_info must be of type str or None')
    
    if type(listing.activities) != list and type(listing.activities) != tuple:
        raise TypeError('listing parameter activities must be of type list or tuple')
    
    for activity in listing.activities:
        if type(activity) != str:
            raise TypeError('listing parameter activities must only contain strings')
        if activity not in enums.activities:
            raise ValueError('Activity {0} is not in list of activities {1}'.format(activity, enums.activities))
    
    if type(listing.user_id) != int:
        raise TypeError('listing parameter user_id must be of type int')
    
    if not user_exists(listing.user_id):
        raise ValueError('No user exists with specified user_id {0}'.format(listing.user_id))

# Raises the appropriate exception for invalid user or does nothing if user is valid
# Does NOT check for duplicate email or phone #
def _check_user_validity(user):
    if type(user) != User:
        raise TypeError('user parameter must be a User object')
    
    if user.id != None:
        raise ValueError('user parameter id should be None')
    
    if type(user.is_owner) != bool:
        raise TypeError('user parameter attribute is_owner must be of type bool')
    
    if type(user.is_sitter) != bool:
        raise TypeError('user parameter attribute is_sitter must be of type bool')

    if not (user.is_owner or user.is_sitter):
        raise ValueError('user cannot be neither an owner nor a sitter')
    
    if type(user.full_name) != str:
        raise TypeError('user parameter attribute full_name must be of type str')
    
    if type(user.email) != str:
        raise TypeError('user parameter attribute email must be of type str')
    
    if type(user.phone_number) != str:
        raise TypeError('user parameter phone_number must be of type str')
    
    if type(user.password_hash) != str:
        raise TypeError('user parameter password_hash must be of type str')
    
    if user.listings != None and user.listings != []:
        raise ValueError('user parameter listings should be None or an empty list')
    
    if user.accepted_listings != None and user.accepted_listings != []:
        raise ValueError('user parameter accepted_listings should be None or an empty list')
