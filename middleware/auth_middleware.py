# flask imports
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import jwt
import os, sys
from functools import wraps
from dotenv import load_dotenv
from app_constants import AppConstants
from string_table import AppMessages
from app_response import AppResponse

load_dotenv(override=True)
SECRET_KEY = os.environ["SECRET_KEY"]
from models import SampleUser, Session

session = Session()


def authenticate_token(auth_token, SECRET_KEY):
    app_response = AppResponse()
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        return True, payload["sub"]
    except jwt.ExpiredSignatureError:
        app_response.set_response(
            AppConstants.CODE_FORBIDDEN,
            {"Failed": "Signature expired."},
            AppMessages.INVALID_JWT,
            AppConstants.CODE_FORBIDDEN,
        )
        return make_response(jsonify(app_response), app_response["code"])
    except jwt.InvalidTokenError:
        app_response.set_response(
            AppConstants.CODE_FORBIDDEN,
            {"Failed": "Invalid token."},
            AppMessages.INVALID_JWT,
            AppConstants.CODE_FORBIDDEN,
        )
        return make_response(jsonify(app_response), app_response["code"])


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        app_response = AppResponse()
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            app_response.set_response(
                AppConstants.CODE_FORBIDDEN,
                {"Failed": "Token is missing !!"},
                AppMessages.INVALID_JWT,
                AppConstants.CODE_FORBIDDEN,
            )
            return make_response(jsonify(app_response), app_response["code"])

        try:
            # decoding the payload to fetch the stored details
            is_valid, data = authenticate_token(token, SECRET_KEY)
            if is_valid:
                current_user = session.query(SampleUser).filter_by(id=data).first()
                return f(current_user, *args, **kwargs)
            else:
                app_response.set_response(
                    AppConstants.CODE_FORBIDDEN,
                    {"Failed": f"Token is invalid as {data}!!"},
                    AppMessages.INVALID_JWT,
                    AppConstants.CODE_FORBIDDEN,
                )
                return make_response(jsonify(app_response), app_response["code"])
        except Exception as e:
            app_response.set_response(
                AppConstants.CODE_FORBIDDEN,
                {"Failed": f"Token is invalid as {e}!!"},
                AppMessages.INVALID_JWT,
                AppConstants.CODE_FORBIDDEN,
            )
            return make_response(jsonify(app_response), app_response["code"])

    return decorated


def tokenid_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        app_response = AppResponse()
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            app_response.set_response(
                AppConstants.CODE_FORBIDDEN,
                {"Failed": f"Token is missing !!"},
                AppMessages.INVALID_JWT,
                AppConstants.CODE_FORBIDDEN,
            )
            return make_response(jsonify(app_response), app_response["code"])

        try:
            # decoding the payload to fetch the stored details
            is_valid, data = authenticate_token(token, SECRET_KEY)
            if is_valid:
                return f(data, *args, **kwargs)
            else:
                app_response.set_response(
                    AppConstants.CODE_FORBIDDEN,
                    {"Failed": f"Token is invalid as {data}!!"},
                    AppMessages.INVALID_JWT,
                    AppConstants.CODE_FORBIDDEN,
                )
                return make_response(jsonify(app_response), app_response["code"])
        except Exception as e:
            app_response.set_response(
                AppConstants.CODE_FORBIDDEN,
                {"Failed": f"Token is invalid as {e}!!"},
                AppMessages.INVALID_JWT,
                AppConstants.CODE_FORBIDDEN,
            )
            return make_response(jsonify(app_response), app_response["code"])

    return decorated
