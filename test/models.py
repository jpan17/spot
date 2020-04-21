# models.py
# Description: Contains models for each of the data objects we will require.
# NOTE: Listing uses the sqlalchemy.types.ARRAY type, which requires that we use Postgres on the backend.

from app import db
import enums
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.sql.expression import or_, and_, not_
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, TEXT
from sqlalchemy import cast
from flask import Flask
from flask_login import UserMixin


# Many-To-Many relationship between users (specifically sitters) and listings
# Note: Online, the documentation has primary_key=True for both columns, but it is omitted here
# (not sure why it would be necessary)
accepted_listings = db.Table('accepted_listings',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('listing_id', db.Integer, db.ForeignKey('listing.id')),
   extend_existing= True
)
# Generic user data object - can represent either an owner or sitter, 
# or both depending on the values of is_owner and is_sitter
class User(UserMixin, db.Model):
    __tablename__ = 'user' # To be safe, I believe table name is used in the ForeignKey declaration in Listing
    id = db.Column(db.Integer, primary_key=True)
    is_owner = db.Column(db.Boolean(), default=False, nullable=False)
    is_sitter = db.Column(db.Boolean(), default=False, nullable=False)
    full_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    phone_number = db.Column(db.String(32), unique=True, nullable=False) # String to account for extensions
    password_hash = db.Column(db.String(1000), nullable=False)

    # Define the one-to-many relationship of Users (specifically owners) to Listings - note that the field name is owner, not user
    # lazy=True -> when loading user, only load listings if needed
    # lazy='joined' -> when loading a listing, always load the user's information along with it (using a SQL JOIN statement)
    listings = db.relationship('Listing', 
        backref=db.backref('owner', lazy='joined'), 
        lazy=True,
        cascade="all, delete, delete-orphan", # All changes should reflect in listings, and listings who no longer have a user associated should be deleted
        passive_deletes=True # if possible, let DB handle the cascade deletion
    )

    # A list of accepted listings (specifically for pet sitters) - note that the field name is sitters, not users
    accepted_listings = db.relationship('Listing', secondary=accepted_listings, lazy=True,
                            backref=db.backref('sitters', lazy=True))

    def __repr__(self):
        return __user_repr__(self)

# Listings are posts made by pet owners for their pets to be taken care of.
class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(64), nullable=False)
    pet_type = db.Column(ENUM(*enums.pet_types, name="pet_type"), nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)
    # Does the pet owner require the pet to be sat the full duration, or are they looking for just sometime in between?
    full_time = db.Column(db.Boolean(), default=True, nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    extra_info = db.Column(db.String(1000))

    # Array of Activities, using ARRAY type which is supported ONLY by Postgres
    activities = db.Column(ARRAY(db.String(64), dimensions=1), nullable=False)

    # Foreign Key for One-To-Many relationship with Users
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)

    # Is the pet type one of the queried pet types?
    @hybrid_method
    def pet_type_is_in(self, pet_types):
        return self.pet_type in pet_types

    @pet_type_is_in.expression
    def pet_type_is_in(cls, pet_types):
        return or_(
            *[cls.pet_type == pet_type for pet_type in pet_types]
        )

    # Can a sitter with availability from start_time to end_time fulfill this listing?
    @hybrid_method
    def datetime_range_matches(self, start_time, end_time):
        if full_time:
            return start_time <= self.start_time and end_time >= self.end_time
        return start_time < self.end_time and end_time > self.start_time

    @datetime_range_matches.expression
    def datetime_range_matches(cls, start_time, end_time):
        return or_(
                and_(cls.full_time, start_time <= cls.start_time, end_time >= cls.end_time),
                and_(not_(cls.full_time), start_time < cls.end_time, end_time > cls.start_time)
            )

    # Does the list of activities contain this listing's list?
    @hybrid_method
    def activities_satisfied(self, activities):
        return set(self.activities).issubset(set(activities))

    @activities_satisfied.expression
    def activities_satisfied(cls, activities):
        temp = set(activities)
        temp.add('3frvdg4gtbn434') # So temp will be a strict superset iff activities was a superset
        return cast(cls.activities, ARRAY(TEXT)).contained_by(temp)

    # Does this listing's zip code contain zip_code in it?
    @hybrid_method
    def zip_code_contains(self, zip_code):
        return zip_code in self.zip_code

    @zip_code_contains.expression
    def zip_code_contains(cls, zip_code):
        # Thank goodness I think this is protected from SQL injection, source:
        # https://stackoverflow.com/questions/31949733/is-a-sqlalchemy-query-vulnerable-to-injection-attacks
        return cls.zip_code.ilike('%{0}%'.format(zip_code))

    def __repr__(self):
        return __listing_repr__(self)

    def start_time_repr(self):
        return '{dt.month}/{dt.day} {hour}:{minute_am_pm}'.format(dt=self.start_time, hour=((self.start_time.hour + 11) % 12 + 1), minute_am_pm=self.start_time.strftime('%M %p'))

    def end_time_repr(self):
        return '{dt.month}/{dt.day} {hour}:{minute_am_pm}'.format(dt=self.end_time, hour=((self.end_time.hour + 11) % 12 + 1), minute_am_pm=self.end_time.strftime('%M %p'))

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
        ret += '\nPassword Hash: {0}'.format(user.password_hash)

        return ret

    except Exception as e:
        return 'Degenerate User Object: {0}'.format(e.args[0])

# Can be fleshed out more if needed
def __listing_repr__(listing):
    return '<Listing ID={0}, pet_name={1}, activities={2}>'.format(listing.id, listing.pet_name, listing.activities)