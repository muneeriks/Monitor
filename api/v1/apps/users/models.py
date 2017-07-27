from datetime import datetime
from werkzeug.security import generate_password_hash, \
     check_password_hash

from apps import db


class User(db.Model):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(255))
    country = db.Column(db.String(120))
    website = db.Column(db.String(120))
    industry = db.Column(db.String(120))
    company_size = db.Column(db.String(120))
    password = db.Column(db.String(255), nullable=False, server_default='')
    parent = db.Column(db.Integer(), db.ForeignKey('auth_user.id'))
    is_admin = db.Column(db.Boolean)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
                backref=db.backref('auth_user', lazy='dynamic'))

    def __init__(self, first_name, last_name, email, password, phone=None, country=None, company=None,
                 website=None, industry=None, company_size=None, parent=None, is_admin=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = email
        self.email = email
        self.phone = phone
        self.company = company
        self.company_size = company_size
        self.industry = industry
        self.website = website
        self.country = country
        self.parent = parent

        if password:
            self.set_password(password)
        if is_admin:
            self.is_admin = is_admin
        else:
            self.is_admin = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
        
    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def email_is_available(self,email):
        if User.query.filter(User.email==email).first():
            return False
        return True


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define UserRoles model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('auth_user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))   
