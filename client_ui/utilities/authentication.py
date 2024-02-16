from flask import Flask, request, redirect, abort, session
import datetime
from functools import wraps
from jose import jwt, JWTError, ExpiredSignatureError
from client_ui.config import Config
from client_ui.dependencies.enquiry_api import EnquiryApi


def check_enquiry_accounts(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        params = {}

        if 'id' in kwargs:
            enquiry_id = kwargs.get('id')
            company_id = session['id']
            params = {"id":enquiry_id, "company_id": session['id']}


        elif 'email' in kwargs:
            enquiries_email = kwargs.get('email')
            company_id = session['id']
            params = {"email":enquiries_email, "company_id": session['id']}

        if params != {}:
            enquiry = EnquiryApi().get_enquiry_to_check(params)
        
            if enquiry != []:
                for enquirey in enquiry:
                    if enquirey.get('company_id') != company_id:
                        return redirect("./no-access")

            else:
                return redirect("./no-access")
        else:
            return redirect("./no-access")

        return f(*args, **kwargs)

    return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if 'role' in session:
            if session['role'] != 'client':
                return redirect("./login")
        else:
            return redirect("./login")

        if 'access_token' not in session or 'refresh_token' not in session:
            session.clear()
            return redirect("./login")
        
        access_token = session['access_token']
        refresh_token = session['refresh_token']

        try:
            # Decode the token
            payload = jwt.decode(access_token, Config.JWT_SECRET_KEY, algorithms=[Config.ALGORITHM])
            # You may also want to add additional validation here
        except ExpiredSignatureError:
            # If Token has expired, attempt to refresh
            try:
                new_access_token, new_refresh_token = Authentication.refresh_access_token(refresh_token)
                # Update session with new tokens
                session['access_token'] = new_access_token
                session['refresh_token'] = new_refresh_token
            except JWTError:
                session.clear()
                return redirect("./login")
        except JWTError:
            session.clear()
            return redirect("./login")

        return f(*args, **kwargs)

    return decorated

class Authentication(object):
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(Config.ACCESS_TOKEN_EXPIRE_MINUTES))})
        encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def refresh_access_token(refresh_token: str):
        id = Authentication.validate_refresh_token(refresh_token)
        user_data = {'sub': id}  # Modify as per your user data structure
        new_access_token = Authentication.create_access_token(user_data)
        new_refresh_token = Authentication.create_refresh_token(user_data)
        return new_access_token, new_refresh_token

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: datetime.timedelta = None):
        to_encode = data.copy()
        if expires_delta is None:
            expires_delta = datetime.timedelta(days=int(Config.REFRESH_TOKEN_EXPIRE_DAYS))
        expire = datetime.datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def validate_refresh_token(refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, Config.JWT_SECRET_KEY, algorithms=[Config.ALGORITHM])
            id: str = payload.get("sub")
            if id is None:
                abort(400, description="Invalid refresh token")
            return id
        except JWTError:
            abort(403, description="Could not validate credentials")

