import os
import sys
import jwt
from flask import request, make_response, jsonify
from email_validator import validate_email, EmailNotValidError

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "common",
    )
)
from app_constants import AppConstants
from string_table import AppMessages
from app_response import AppResponse
from werkzeug.security import generate_password_hash, check_password_hash
from app_blueprint import AppBP
from models import SampleUser, Session, TokenStore
from auth_middleware import token_required, tokenid_required

hello_world_test = AppBP("hello_world", __name__)


# Default Page
@hello_world_test.route("/", methods=["GET"])
def hello_world():
    """Home Page
    ---
    tags:
     - name: Default Home Page
    responses:
        200:
            description: Testing Swaager API

    """
    app_response = AppResponse()
    app_response.set_response(
        AppConstants.CODE_OK,
        {"Tester": "Tester"},
        AppMessages.OPERATION_SUCCESS,
        AppConstants.SUCCESSFULL_STATUS_CODE,
    )
    return make_response(jsonify(app_response), app_response["code"])


# Registration Page
@hello_world_test.route("/register", methods=["POST"])
def request_request():
    """New User Creation
    ---
    tags:
     - name: Register POST
    parameters:
      - name: Username
        in: formData
        type: string
        required: true
      - name: Email Address
        in: formData
        type: string
        required: true
      - name: Password
        in: formData
        type: string
        required: true
      - name: Confirm Password
        in: formData
        type: string
        required: true

    responses:
        200:
            description: User is created Successfully
        404:
            description: User is not created successfully
    """
    app_response = AppResponse()
    username = request.form.get("Username")
    email = request.form.get("Email Address")
    password = request.form.get("Password")
    confirm_password = request.form.get("Confirm Password")
    if email is None:
        app_response.set_response(
                    AppConstants.CODE_INVALID_REQUEST,
                    {"Failed": f"Email Should not be empty"},
                    AppMessages.OPERATION_FAILED,
                    AppConstants.CODE_INVALID_REQUEST,
                )
        return make_response(
                            jsonify(app_response), app_response["code"]
                        )
    
    if password is None:
        app_response.set_response(
                    AppConstants.CODE_INVALID_REQUEST,
                    {"Failed": f"Password should not be empty"},
                    AppMessages.OPERATION_FAILED,
                    AppConstants.CODE_INVALID_REQUEST,
                )
        return make_response(
                            jsonify(app_response), app_response["code"]
                        )
    
    if confirm_password is None:
        app_response.set_response(
                    AppConstants.CODE_INVALID_REQUEST,
                    {"Failed": f"Confirm Password should not be empty"},
                    AppMessages.OPERATION_FAILED,
                    AppConstants.CODE_INVALID_REQUEST,
                )
        return make_response(
                            jsonify(app_response), app_response["code"]
                        )
    
    if username is None:
        app_response.set_response(
                    AppConstants.CODE_INVALID_REQUEST,
                    {"Failed": f"Username should not be empty"},
                    AppMessages.OPERATION_FAILED,
                    AppConstants.CODE_INVALID_REQUEST,
                )
        return make_response(
                            jsonify(app_response), app_response["code"]
                        )

    session = Session()
    # Email Validation

    user = session.query(SampleUser).filter_by(email=email).first()
    if user:
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": f"User with this email address {email} already Registered"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])

    try:
        valid_email = validate_email(email)
        email = valid_email["email"]
    except EmailNotValidError as e:
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": f"Email is not correct Error:{str(e)}"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])

    # username Validation
    user = session.query(SampleUser).filter_by(username=username).first()
    if user:
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": f"Username already taken"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])

    if len(username.strip()) < 5:
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": "Username should have length greater than 5"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])

    if len(password.strip()) < 5:
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": "Password should have length greater than 5"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])

    if password.strip() != confirm_password.strip():
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": "Password Not Match"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])
    newuser = SampleUser(
        username=username,
        email=email,
        password=password,
    )
    try:
        session.add(newuser)
        session.commit()
        auth_token = newuser.encode_auth_token(newuser.id).decode()
        generated_token = TokenStore(token=auth_token, user_id=newuser.id)
        session.add(generated_token)
        session.commit()
    finally:
        session.close()
    app_response.set_response(
        AppConstants.CODE_OK,
        {
            "Success": f"User is created with given name as {username} with email {email} Generated Token as {auth_token}"
        },
        AppMessages.OPERATION_SUCCESS,
        AppConstants.SUCCESSFULL_STATUS_CODE,
    )
    return make_response(jsonify(app_response), app_response["code"])


# Login Page
@hello_world_test.route("/login", methods=["POST"])
def login_request():
    """User Login
    ---
    tags:
     - name: Login POST
    parameters:
      - name: Email Address
        in: formData
        type: string
        required: true
      - name: Password
        in: formData
        type: string
        required: true

    responses:
        200:
            description: User is Login Successfully
        404:
            description: User is not LoggedInn
    """
    app_response = AppResponse()
    email = request.form.get("Email Address")
    password = request.form.get("Password")
    session = Session()
    if email is None:
        app_response.set_response(
                    AppConstants.CODE_INVALID_REQUEST,
                    {"Failed": f"Email Should not be empty"},
                    AppMessages.OPERATION_FAILED,
                    AppConstants.CODE_INVALID_REQUEST,
                )
        return make_response(
                            jsonify(app_response), app_response["code"]
                        )
    if password is None:
        app_response.set_response(
                    AppConstants.CODE_INVALID_REQUEST,
                    {"Failed": f"Password should not be empty"},
                    AppMessages.OPERATION_FAILED,
                    AppConstants.CODE_INVALID_REQUEST,
                )
        return make_response(
                            jsonify(app_response), app_response["code"]
                        )
    try:
        user = session.query(SampleUser).filter_by(email=email).first()
        if user:
            if user.verify_password(password):
                user_token = (
                    session.query(TokenStore).filter_by(user_id=user.id).first()
                )
                if user_token:
                    is_valid, check_token = user.decode_auth_token(user_token.token)
                    if is_valid:
                        app_response.set_response(
                            AppConstants.CODE_OK,
                            {
                                "Success": f"User is loggedinn with given email as {email} with email as {email} and token as {user_token.token}"
                            },
                            AppMessages.OPERATION_SUCCESS,
                            AppConstants.SUCCESSFULL_STATUS_CODE,
                        )
                        return make_response(
                            jsonify(app_response), app_response["code"]
                        )

                    else:
                        auth_token = user.encode_auth_token(user.id).decode()
                        user_token.token = auth_token
                        session.commit()
                        app_response.set_response(
                            AppConstants.CODE_OK,
                            {
                                "Success": f"User is loggedinn with email as {email} and token as {auth_token}"
                            },
                            AppMessages.OPERATION_SUCCESS,
                            AppConstants.SUCCESSFULL_STATUS_CODE,
                        )
                        return make_response(
                            jsonify(app_response), app_response["code"]
                        )

                else:
                    auth_token = user.encode_auth_token(user.id).decode()
                    generated_token = TokenStore(token=auth_token, user_id=user.id)
                    session.add(generated_token)
                    session.commit()
                    is_valid, check_token = user.decode_auth_token(auth_token)
                    if is_valid:
                        return {
                            "Success": f"User is loggedinn with email as {email} and token as {auth_token}"
                        }, 200
                    else:
                        app_response.set_response(
                            AppConstants.CODE_INVALID_REQUEST,
                            {"Failed": f"Token is invalid Error: {check_token}"},
                            AppMessages.OPERATION_FAILED,
                            AppConstants.CODE_INVALID_REQUEST,
                        )
                        return make_response(
                            jsonify(app_response), app_response["code"]
                        )

            else:
                app_response.set_response(
                    AppConstants.CODE_INVALID_REQUEST,
                    {"Failed": f"Password is not matched"},
                    AppMessages.OPERATION_FAILED,
                    AppConstants.CODE_INVALID_REQUEST,
                )
                return make_response(jsonify(app_response), app_response["code"])
        else:
            app_response.set_response(
                AppConstants.CODE_INVALID_REQUEST,
                {"Failed": f"User with given email as {email} is not Registered"},
                AppMessages.OPERATION_FAILED,
                AppConstants.CODE_INVALID_REQUEST,
            )
            return make_response(jsonify(app_response), app_response["code"])
    finally:
        session.close()


# User Account Details
@hello_world_test.route("/user_list", methods=["GET"])
@token_required
def hello_user(current_user):
    """User Detail
    ---
    tags:
     - name: Token User
    security:
     - APIKeyHeader: ['x-access-token']
    responses:
        200:
            description: User Detail Accessed perfectly
        400:
            description: User cannot be retrieved

    """
    app_response = AppResponse()
    app_response.set_response(
        AppConstants.CODE_OK,
        {"username": current_user.username, "Email": current_user.email},
        AppMessages.OPERATION_SUCCESS,
        AppConstants.SUCCESSFULL_STATUS_CODE,
    )
    return make_response(jsonify(app_response), app_response["code"])


@hello_world_test.route("/user_delete", methods=["DELETE"])
@tokenid_required
def delete_user(data):
    """User DELETE
    ---
    tags:
     - name: Delete User
    security:
     - APIKeyHeader: ['x-access-token']
    responses:
        200:
            description: User Account deleted successfully
        400:
            description: User Account cannot be deleted

    """
    app_response = AppResponse()
    session = Session()
    user = session.query(SampleUser).filter_by(id=data).first()
    if user:
        try:
            session.delete(user)
            session.commit()
            app_response.set_response(
                AppConstants.CODE_OK,
                {"Success": f"User with given id {data} is deleted successfully"},
                AppMessages.OPERATION_SUCCESS,
                AppConstants.SUCCESSFULL_STATUS_CODE,
            )
            return make_response(jsonify(app_response), app_response["code"])
        except Exception as e:
            app_response.set_response(
                AppConstants.CODE_INVALID_REQUEST,
                {
                    "Failed": f"User with given token id {data} is not deleted successfully as {str(e)}"
                },
                AppMessages.OPERATION_FAILED,
                AppConstants.CODE_INVALID_REQUEST,
            )
            return make_response(jsonify(app_response), app_response["code"])
        finally:
            session.close()
    else:
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": f"User with given id {data} is not available"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])


@hello_world_test.route("/updateuser", methods=["PUT"])
@tokenid_required
def updateuser_request(data):
    """User Update
    ---
    tags:
     - name: Update PUT
    parameters:
      - name: Email Address
        in: formData
        type: string
        required: false
      - name: Username
        in: formData
        type: string
        required: false
      - name: Password
        in: formData
        type: string
        required: false

    security:
     - APIKeyHeader: ['x-access-token']
    responses:
        200:
            description: User Details is Updated Successfully
        404:
            description: User Details is not Updated Successfully
    """
    app_response = AppResponse()
    email = request.form.get("Email Address")
    username = request.form.get("Username")
    password = request.form.get("Password")
    session = Session()

    try:
        user = session.query(SampleUser).filter_by(id=data).first()
        if user:
            if email is not None:
                try:
                    valid_email = validate_email(email)
                    email = valid_email["email"]
                    user.email = email
                except EmailNotValidError as e:
                    app_response.set_response(
                        AppConstants.CODE_INVALID_REQUEST,
                        {"Failed": f"Email is not correct Error:{str(e)}"},
                        AppMessages.OPERATION_FAILED,
                        AppConstants.CODE_INVALID_REQUEST,
                    )
                    return make_response(jsonify(app_response), app_response["code"])
            if username is not None:
                if len(username.strip()) < 5:
                    app_response.set_response(
                        AppConstants.CODE_INVALID_REQUEST,
                        {"Failed": "Username should have length greater than 5"},
                        AppMessages.OPERATION_FAILED,
                        AppConstants.CODE_INVALID_REQUEST,
                    )
                    return make_response(jsonify(app_response), app_response["code"])
                user.username = username
            if password is not None:
                if len(password.strip()) < 5:
                    app_response.set_response(
                        AppConstants.CODE_INVALID_REQUEST,
                        {"Failed": "Password should have length greater than 5"},
                        AppMessages.OPERATION_FAILED,
                        AppConstants.CODE_INVALID_REQUEST,
                    )
                    return make_response(jsonify(app_response), app_response["code"])
                user.password = generate_password_hash(password)
            session.commit()
            app_response.set_response(
                AppConstants.CODE_OK,
                {"Success": f"User with given id as {data} is updated Successfully"},
                AppMessages.OPERATION_SUCCESS,
                AppConstants.SUCCESSFULL_STATUS_CODE,
            )
            return make_response(jsonify(app_response), app_response["code"])

        else:
            app_response.set_response(
                AppConstants.CODE_INVALID_REQUEST,
                {"Failed": f"User with given id as {data} is not Registered"},
                AppMessages.OPERATION_FAILED,
                AppConstants.CODE_INVALID_REQUEST,
            )
            return make_response(jsonify(app_response), app_response["code"])

    finally:
        session.close()
