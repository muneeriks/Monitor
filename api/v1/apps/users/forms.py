#from __future__ import absolute_import
from datetime import datetime
# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, TextField, PasswordField,BooleanField

# Import Form validators
from wtforms.validators import *
from wtforms import ValidationError

from flask_jwt import current_identity

from apps import db
from models import User


# Define the login form (WTForms)
class LoginForm(Form):
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])


def unique_email_validator(form, field):
    """ Username must be unique"""
    if not User.email_is_available(field.data):
        raise ValidationError('This Email is already in use. Please try another one.')


def update_email_validator(form, field):
    """ Username must be unique"""
    obj = User.query.filter(User.username==current_identity.username).first()
    if not User.email_is_available(field.data) and not field.data == obj.email:
        raise ValidationError('This Email is already in use. Please try another one.')


def update_sub_account_email_validator(form, field):
    """ Username must be unique"""
    if not User.email_is_available(field.data) and not field.data == form.instance.email:
        raise ValidationError('This Email is already in use. Please try another one.')


class RegisterForm(Form):

    first_name = StringField('First Name', validators=[
        DataRequired('First Name is required')])
    last_name = StringField('Last Name', validators=[
        DataRequired('Last Name is required')])
    country = StringField('Country', validators=[
        DataRequired('Country is required')])
    email = StringField('Email', validators=[
        DataRequired('Email is required'),
        Email('Invalid Email'),
        unique_email_validator])
    company = StringField('Company', validators=[
        DataRequired('Company is required')])  
    phone = StringField('Phone', validators=[
        DataRequired('Phone Number is required')])    
    password = PasswordField('Password', validators=[
        DataRequired('Password is required')])

    def save(self,instance=None):
        data = self.data
        db.session.add(User(**data))
        db.session.commit()


class ProfileUpdateForm(Form):

    first_name = StringField('First Name', validators=[
        DataRequired('First Name is required')])
    last_name = StringField('Last Name', validators=[
        DataRequired('Last Name is required')])
    country = StringField('Country', validators=[
        DataRequired('Country is required')])
    email = StringField('Email', validators=[
        DataRequired('Email is required'),
        Email('Invalid Email'), update_email_validator])
    company = StringField('Company', validators=[
        DataRequired('Company is required')])
    phone = StringField('Phone', validators=[
        DataRequired('Phone Number is required')])
    company_size = StringField('Company size')
    industry = StringField('Industry')
    website = StringField('Website')

    def save(self, instance=None):
        data = self.data
        db.session.query(User).filter_by(username=instance.username).update(data)
        db.session.commit()


class CreateSubAccountForm(Form):

    first_name = StringField('First Name', validators=[
        DataRequired('First Name is required')])
    last_name = StringField('Last Name', validators=[
        DataRequired('Last Name is required')])
    email = StringField('Email', validators=[
        DataRequired('Email is required'),
        Email('Invalid Email'), unique_email_validator])
    password = PasswordField('Password', validators=[
        DataRequired('Password is required')])
    retype_password = PasswordField('Retype Password', validators=[
        EqualTo('password', message='Password and Retype Password did not match')])

    def save(self, instance=None):
        data = self.data
        data['parent'] = current_identity.id
        del data['retype_password']
        db.session.add(User(**data))
        db.session.commit()


class UpdateSubAccountForm(Form):

    first_name = StringField('First Name', validators=[
        DataRequired('First Name is required')])
    last_name = StringField('Last Name', validators=[
        DataRequired('Last Name is required')])
    email = StringField('Email', validators=[
        DataRequired('Email is required'),
        Email('Invalid Email'), update_sub_account_email_validator])
    password = PasswordField('Password', )
    retype_password = PasswordField('Retype Password', validators=[
        EqualTo('password', message='Password and Retype Password did not match')])

    def __init__(self, *args, **kwargs):
        self.instance = kwargs['instance']
        super(UpdateSubAccountForm, self).__init__(*args, **kwargs)

    def save(self, sub_account_id):
        data = self.data
        data['username'] = data['email']
        del data['retype_password']
        db.session.query(User).filter_by(id=sub_account_id).update(data)
        db.session.commit()
