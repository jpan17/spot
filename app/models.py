# models.py
# Description: Contains models for each of the data objects we will require.
# NOTE: Listing uses the sqlalchemy.types.ARRAY type, which requires that we use Postgres on the backend.

from app import db
import enums

# Generic user data object - can represent either an owner or sitter, 
# or both depending on the values of is_owner and is_sitter
class User(db.Model):
    __tablename__ = 'user' # To be safe, I believe table name is used in the ForeignKey declaration in Listing
    id = db.Column(db.Integer, primary_key=True)
    is_owner = db.Column(db.Boolean(), default=False, nullable=False)
    is_sitter = db.Column(db.Boolean(), default=False, nullable=False)
    full_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    phone_number = db.Column(db.String(32), nullable=False) # String to account for extensions
    password_hash = db.Column(db.String(128), nullable=False)

    # Define the one-to-many relationship of Users (specifically owners) to Listings
    # lazy=True -> when loading user, only load listings if needed
    # lazy='joined' -> when loading a listing, always load the user's information along with it (using a SQL JOIN statement)
    listings = db.relationship('Listing', backref=db.backref('user', lazy='joined'), lazy=True)

    # toString method
    def __repr__(self):
        return __user_repr__(self)

class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(64), nullable=False)
    pet_type = db.Column(db.Enum(enums.PetType), nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)
    # Does the pet owner require the pet to be sat the full duration, or are they looking for just sometime in between?
    full_time = db.Column(db.Boolean(), default=True, nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    extra_info = db.Column(db.String(1000))

    # Array of Activities, using ARRAY type which is supported ONLY by Postgres
    activities = db.Column(db.ARRAY(db.Enum(enums.Activity), dimensions=1), nullable=False)

    # Foreign Key for One-To-Many relationship with Users
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # toString method
    def __repr__(self):
        return __listing_repr__(self)

# =======================================================================================================
# =                            __repr__ functions (for use in debugging)                                =
# =======================================================================================================

def __user_repr__(user):
    try:
        ret = ''
        if user.is_owner:
            if user.is_sitter:
                ret = 'Pet Owner + Sitter:'
            else:
                ret = 'Pet Owner:'
        else:
            if user.is_sitter:
                ret = 'Pet Sitter:'
            else:
                raise Exception('User is neither Owner nor Sitter')

        ret += '\n============================='
        ret += '\nID: {0}'.format(user.id)
        ret += '\nFull Name: {0}'.format(user.full_name)
        ret += '\nEmail: {0}'.format(user.email)
        ret += '\nPhone Number: {0}'.format(user.phone_number)
        ret += '\nPassword Hash: You probably shouldn\'t be viewing that...'

        return ret

    except Exception as e:
        return 'Degenerate User Object: {0}'.format(e.args[0])

# Can be fleshed out more if needed
def __listing_repr__(listing):
    return '<Listing ID={0}>'.format(listing.id)