from apps import api
from users.views import UserSignUptView, UpdateProfileView, CreateSubAccountView, \
    UpdateSubAccountView, UserDetailsView


def add_resource():
	api.add_resource(UserSignUptView, '/user/signup/')
	api.add_resource(UserDetailsView, '/user/details/')
	api.add_resource(UpdateProfileView, '/user/update-profile/')
	api.add_resource(CreateSubAccountView, '/user/create-sub-account/')
	api.add_resource(UpdateSubAccountView, '/user/update-sub-account/<user_id>/')
