"""
db_service.py
=============================================================================
A file containing useful methods for querying the database of Users/Listings,
specifically methods that will be used throughout the application.
 """

from app import app, db
from app.models import User, Listing
import datetime
import enums

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

def get_listings(user = None, user_id = -1, accepted = False):
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
    >>> db_service.get_listings(User(id=1))
    [<Listing ID=1>, <Listing ID=2>]

    >>> db_service.get_listings(user_id='2')
    [<Listing ID=3>]

    >>> db_service.get_listings()
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
        Filters Listings for pet type *pet_type*, or does not filter is unspecified/None.
    activities : list or tuple of str or None, optional
        Filters Listings for those that share any activity with those in the *activities* parameter,
        or does not filter is unspecified/None.
    zip_code : str or None, optional
        Filters Listings for zip code *zip_code*, or does not filter if unspecified/None.
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

    Examples
    --------
    >>> db_service.all_listings(pet_type = 'Dog', activities = ['Walking'], zip_code = '08540')
    [<Listing ID=15>]
    
    """
    
    listings = []
    
    if type(pet_type) != str and type(pet_type) != NoneType:
        raise TypeError('pet_type should be a parameter of type None or str')
    
    if type(activities) != list or type(activities) != tuple and type(activities) != NoneType:
        raise TypeError('activities should be a parameter of type None, tuple or list')
    
    for activity in activities:
        if type(activity) != str:
            raise TypeError('activities tuple/list should only contain str')
    
    if type(zip_code) != str and type(zip_code) != NoneType:
        raise TypeError('zip_code should be a parameter of type None or str')
    
    if type(datetime_range) != tuple and type(datetime_range) != NoneType:
        raise(TypeError('datetime_range should be a parameter of type None or tuple'))
    
    for time in datetime_range:
        if type(time) != datetime:
            raise TypeError('datetime_range tuple should only contain datetimes')
        
    startTime = datetime_range[0]
    endTime = datetime_range[1]
    
    if startTime >= endTime:
        raise ValueError('starttime must be before endtime')
    
    return Listing.query.all()

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
    
    if type(listing) != Listing:
        raise TypeError('listing parameter must be a Listing object')
    
    if hasattr(listing, 'id'):
        raise ValueError('listing parameter should not have attribute id')
    
    if type(listing.pet_name) != str:
        raise TypeError('listing parameter attribute pet_name must be of type str')
    
    if type(listing.pet_type) != str or pet_type not in enums.pet_types:
        raise TypeError('listing parameter pet_type must be of type str and be one of our prespecified pet types')
    
    if type(listing.start_time) != datetime:
        raise TypeError('listing parameter start_time must be of type datetime')
    
    if type(listing.end_time) != datetime:
        raise TypeError('listing parameter end_time must be of type datetime')
    
    if listing.start_time >= listing.end_time:
        raise ValueError('starttime must be before endtime')
    
    if type(listing.full_time) != bool:
        raise TypeError('listing parameter full_time must be of type bool')
    
    if type(listing.zip_code) != str:
        raise TypeError('listing parameter zip_code must be of type str')
    
    if hasattr(listing, 'extra_info') and type(listing.extra_info) != str and type(listing.extra_info) != NoneType:
        raise TypeError('listing parameter extra_info must be of type str or None')
    
    if type(listing.activities) != list and type(activities) != tuple:
        raise TypeError('listing parameter activities must be of type list or tuple')
    
    for activity in listing.activities:
        if type(activity) != str:
            raise TypeError('listing paremeter activities must only contain strings')
        if activity not in enums.activities:
            raise ValueError('listing paremeter activities must only contain strings that are one of our prespecified activities')
    
    if type(listing.user_id) != int:
        raise TypeError('listing parameter user_id must be of type int')
    
    try:
        db.session.add(listing)
        db.session.commit()
        return ''
    except Exception as e:
        db.session.rollback()
        return "Error: " + str(e)

def create_user(user):
    
    if type(user) != User:
        raise TypeError('user parameter must be a User object')
    
    if hasattr(user, 'id'):
        raise ValueError('user parameter should not have attribute id')
    
    if type(user.is_owner) != bool:
        raise TypeError('user parameter attribute is_owner must be of type bool')
    
    if type(user.is_sitter) != bool:
        raise TypeError('user parameter attribute is_sitter must be of type bool')
    
    if type(user.full_name) != str:
        raise TypeError('user parameter attribute full_name must be of type str')
    
    if type(user.email) != str:
        raise TypeError('user parameter attribute email must be of type str')
    
    if type(user.phone_number) != str:
        raise TypeError('user parameter phone_number must be of type str')
    
    if type(user.password_hash) != str:
        raise TypeError('user parameter password_hash must be of type str')
    
    if hasattr(user, 'listings'):
        raise ValueError('user parameter should not have attribute listings')
    
    if hasattr(user, 'accepted_listings'):
        raise ValueError('user parameter should not have attribute accepted_listings')
    
    try:
        db.session.add(user)
        db.session.commit()
        return ''
    except Exception as e:
        db.session.rollback()
        return "Error: " + str(e)

def update_listing(listing_id, pet_name=None, pet_type=None, start_time=None, end_time=None,
                   full_time=None, zip_code=None, extra_info=None, activiies=None):
    
    id = listing_id

    if type(listing_id) != int:
        if type(listing_id) != str:
            raise TypeError('listing_id must be an integer or string')
        else:
            if _str_is_integer(listing_id):
                id = int(listing_id)
            else:
                raise ValueError('listing_id is a string, but cannot be parsed into an integer')
            
    listing = Listing.query.filter_by(id=id).first()
    
    if type(pet_name) != str and type(pet_name) != NoneType:
        raise TypeError('attribute pet_name must be of type str or None')
    
    if type(pet_type) != NoneType and type(pet_type) != str:
        raise TypeError('attribute pet_type must be of type str or None')
    
    if pet_type not in enums.pet_types:
        raise ValueError('attribute pet_type must be one of our prespecified pet types')
    
    if type(start_time) != datetime:
        raise TypeError('attribute start_time must be of type datetime')
    
    if type(end_time) != datetime:
        raise TypeError('attribute end_time must be of type datetime')
    
    if listing.start_time >= listing.end_time:
        raise ValueError('starttime must be before endtime')
    
    if type(full_time) != bool:
        raise TypeError('attribute full_time must be of type bool')
    
    if type(zip_code) != str:
        raise TypeError('attribute zip_code must be of type str')
    
    if type(extra_info) != str and type(extra_info) != NoneType:
        raise TypeError('listing parameter extra_info must be of type str or None')
    
    if type(activities) != list and type(activities) != tuple or type(activities) != NoneType:
        raise TypeError('listing parameter activities must be of type list or tuple or None')
    
    for activity in activities:
        if type(activity) != str:
            raise TypeError('listing paremeter activities must only contain strings')
        if activity not in enums.activities:
            raise ValueError('listing paremeter activities must only contain strings that are one of our prespecified activities')
        
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
            
    try:
        db.session.commit()
        return ''
    except Exception as e:
        db.session.rollback()
        return "Error: " + str(e)
    
def delete_listing(listing_id):
    
    id = listing_id

    if type(listing_id) != int:
        if type(listing_id) != str:
            raise TypeError('listing_id must be an integer or string')
        else:
            if _str_is_integer(listing_id):
                id = int(listing_id)
            else:
                raise ValueError('listing_id is a string, but cannot be parsed into an integer')

    # check if listing exists in the first place
    listing = Listing.query.filter_by(id=id).first()
    
    if listing == None:
        raise ValueError('listing does not exist in database')
    
    # delete listing from owner's listings (and sitter's accepted listings? but idk how to)
    # implement that HELP RELATIONSHIPS :(
    userid = listing.userid
    user = get_user(userid)
    
    # did I do this part right?
    listing.delete()
    
    try:
        db.session.commit()
        return ''
    except Exception as e:
        db.session.rollback()
        return "Error: " + str(e)
    

def delete_user(user_id):
    pass

def accept_listing(user_id, listing_id):
    pass

def _str_is_integer(s):
    try:
        int(s)
        return True
    except ValueError as e:
        return False