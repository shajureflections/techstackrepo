import sys
import jwt
import os
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from database import database_config
from dotenv import load_dotenv

Base, engine, Session = database_config()


load_dotenv(override=True)
SECRET_KEY = os.environ["SECRET_KEY"]


class SampleUser(UserMixin, Base):
    __tablename__ = "SampleUser"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String, unique=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def __repr__(self):
        return f"<User {self.username}>"

    def verify_password(self, check_password):
        return check_password_hash(self.password, check_password)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=0, seconds=500000),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY)
            return True, payload["sub"]
        except jwt.ExpiredSignatureError:
            return False, "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return False, "Invalid token. Please log in again."


class TokenStore(Base):
    """
    Token Model for storing JWT tokens
    """

    __tablename__ = "tokenstorem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, unique=True, nullable=False)
    blacklisted_on = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("SampleUser.id", ondelete='CASCADE'))

    def __init__(self, token, user_id):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()
        self.user_id = user_id

    def __repr__(self):
        return "<id: UserID: {}".format(self.user_id)


class Todomodel(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    completed = Column(Boolean, default=False, nullable=False)
    description = Column(String, nullable=False)
    createdby_id = Column(Integer, ForeignKey("SampleUser.id",ondelete='CASCADE'))

    def __init__(self, completed, description, createdby_id):
        self.completed = completed
        self.description = description
        self.createdby_id = createdby_id

    def __repr__(self):
        return "<Task: {}".format(self.description)
