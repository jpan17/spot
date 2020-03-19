from app import db

# Generic user data object - can represent either an owner or sitter, 
# or both depending on the values of is_owner and is_sitter
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_owner = db.Column(db.Boolean(), default=False, nullable=False)
    is_sitter = db.Column(db.Boolean(), default=False, nullable=False)
    full_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    phone_number = db.Column(db.String(32), nullable=False) # String to account for extensions
    password_hash = db.Column(db.String(128), nullable=False)

    # toString method
    def __repr__(self):
        try:
            ret = ''
            if self.is_owner:
                if self.is_sitter:
                    ret = 'Pet Owner + Sitter:'
                else:
                    ret = 'Pet Owner:'
            else:
                if self.is_sitter:
                    ret = 'Pet Sitter:'
                else:
                    raise Exception('User is neither Owner nor Sitter')
                
            ret += '\n============================='
            ret += '\nID: {0}'.format(self.id)
            ret += '\nFull Name: {0}'.format(self.full_name)
            ret += '\nEmail: {0}'.format(self.email)
            ret += '\nPhone Number: {0}'.format(self.phone_number)
            ret += '\nPassword Hash: You probably shouldn\'t be viewing that...'

            return ret

        except Exception as e:
            return 'Degenerate User Object: {0}'.format(e.args[0])