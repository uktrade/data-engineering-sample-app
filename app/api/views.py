from flask import current_app as flask_app

from data_engineering.common.views import (
    ac,
    json_error,
    response_orientation_decorator
)


def get_data():
    return {'a': 0, 'b': 1}

@json_error
@response_orientation_decorator
@ac.authentication_required
@ac.authorization_required
def get_data_authenticated(orientation):
    response = {'a': 0, 'b': 1, 'authenticated': True}
    response = flask_app.make_response(response)
    print('orientation:', orientation)
    return response

@ac.authentication_required
@ac.authorization_required
def train_model():
    response = {'status': 200}
    response = flask_app.make_response(response)
    return response

