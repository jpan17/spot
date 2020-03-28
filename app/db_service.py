"""
db_service.py
=============================================================================
A file containing useful methods for querying the database of Users/Listings,
specifically methods that will be used throughout the application.
 """

from app import app, db
from app.models import User, Listing

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
    activities : list of str or None, optional
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
    
    return None

def _str_is_integer(s):
    try:
        int(s)
        return True
    except ValueError as e:
        return False