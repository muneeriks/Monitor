import json

from flask_jwt import JWT
from flask_restful import Resource, request, abort
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp, check_password_hash

from apps import app, db
from forms import RegisterForm, ProfileUpdateForm, CreateSubAccountForm, UpdateSubAccountForm
from models import User
from serializer import AlchemyEncoder


class UserSignUptView(Resource):

    def post(self):
        register_form = RegisterForm(request.form, csrf_enabled=False)
        if register_form.validate():
            register_form.save()
            return {"status": "success, User created"}
        return register_form.errors


class UserDetailsView(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        user =  User.query.filter(User.username==current_identity.username).first()
        data = json.dumps(user, cls=AlchemyEncoder)
        return {"data": data}


def authenticate(username, password):
    user = User.query.filter(User.username==username).first()
    if user and check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.filter(User.id==user_id).first()

jwt = JWT(app, authenticate, identity)


class UpdateProfileView(Resource):
    method_decorators = [jwt_required()]

    def post(self):
        obj = User.query.filter(User.username==current_identity.username).first()
        update_form = ProfileUpdateForm(request.form, csrf_enabled=False)
        if update_form.validate():
            update_form.save(obj)
            return {"status": "success, Profile updated!"}
        return update_form.errors


def abort_if_user_doesnt_exist(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, message="User {} doesn't exist".format(user_id))


def sub_account_validate(sub_account_id):
    obj = User.query.get(sub_account_id)
    if not obj.parent == current_identity.id:
        abort(401, message="Permission denied, User {} is not your child".format(sub_account_id))


class CreateSubAccountView(Resource):
    method_decorators = [jwt_required()]

    def put(self):
        create_form = CreateSubAccountForm(request.form, csrf_enabled=False)
        if create_form.validate():
            create_form.save()
            return {"status": "success, Created sub account."}
        return create_form.errors


class UpdateSubAccountView(Resource):
    method_decorators = [jwt_required()]

    def get(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        user =  User.query.get(user_id)
        data = json.dumps(user, cls=AlchemyEncoder)
        return {"data": data}

    def put(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        sub_account_validate(user_id)
        obj = User.query.get(user_id)
        update_form = UpdateSubAccountForm(request.form, instance=obj, csrf_enabled=False)
        if update_form.validate():
            update_form.save(user_id)
            return {"status": "success, Updated sub account details"}
        return update_form.errors

    def delete(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        sub_account_validate(user_id)
        db.session.query(User).filter(User.id==user_id).delete()
        db.session.commit()
        return '', 204
