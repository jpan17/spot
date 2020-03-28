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
    provided, attempts to use *user_id* instead. If neither are given, a TypeError
    is raised. *accepted* is only used if a user is both an owner and a sitter,
    in which case *accepted* being True will make the function return the user's
    accepted listings rather than the listings they own.

    Parameters
    ----------

    """

    if type(user_id) != int:
        raise TypeError('user_id must be an integer or string')

    # If user unspecified, search for it
    if user == None:
        user = get_user_by_id(user_id)
        if user == None:
            raise TypeError('No user was provided and no user was found by the given user_id (or no user_id was provided)')

def _str_is_integer(s):
    try:
        int(s)
        return True
    except ValueError as e:
        return False