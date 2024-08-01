import threading
import time

from flask import Flask, request, render_template, redirect, url_for, session, flash, send_file
from flask_socketio import SocketIO
from flask.views import *
from functools import wraps

from server_pkg.server.models import User
import server_pkg.global_vars as global_vars


from urllib.parse import urlparse, urljoin

from werkzeug.security import generate_password_hash as generate_secure_password_hash, check_password_hash as check_secure_password_hash
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
import hashlib
import random
import string

from io import BytesIO
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request

def genInviteLink():
    str = string.ascii_letters+string.digits
    # remove similar looking characters like 1, l, I, 0, O
    str = str.replace('1', '')
    str = str.replace('l', '')
    str = str.replace('I', '')
    str = str.replace('0', '')
    str = str.replace('O', '')
    return ''.join(random.choice(str) for i in range(10))

def decorator_compressor(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco

def socket_decorator(app, route):
    return decorator_compressor(
        app.route(route),
        cross_origin(origin=app.config['SERVER_NAME'], headers=[
                     'Content- Type', 'Authorization'])
    )

def hash_generator(password):
    return hashlib.sha256(password.encode()).hexdigest()


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # get function name
        func_name = f.__name__
        try:
            verify_jwt_in_request(optional = True)
        except Exception as exc:
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
        current_user_id = get_jwt_identity()
        print(current_user_id)
        if current_user_id is not None:
            user_type = User.query.filter_by(id=current_user_id).first().user_type
        else:  
            user_type = "None"
        print(user_type)
        if user_type == "A":
            return f(*args, **kwargs)
        elif user_type == "None":
            flash("login to access this page", "info")
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
        else:
            flash("login as Admin to access this page", "danger")
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
    return wrap

def sponsor_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # get function name
        func_name = f.__name__
        try:
            verify_jwt_in_request(optional = True)
        except Exception as exc:
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
        current_user_id = get_jwt_identity()
        print(current_user_id)
        if current_user_id is not None:
            user_type = User.query.filter_by(id=current_user_id).first().user_type
        else:  
            user_type = "None"
        if user_type == "S":
            if User.query.filter_by(id=current_user_id).first().sponsor_approval == "True":
                return f(*args, **kwargs)
            else:
                flash("Sponsor Approval Pending", "warning")
                return redirect(url_for('sponsor_dashboard'))
        elif user_type == "None":
            flash("login to access this page", "info")
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
        else:
            flash("login as Sponsor to access this page", "danger")
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
    return wrap

def influencer_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # get function name
        func_name = f.__name__
        try:
            verify_jwt_in_request(optional = True)
        except Exception as exc:
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
        current_user_id = get_jwt_identity()
        if current_user_id is not None:
            user_type = User.query.filter_by(id=current_user_id).first().user_type
        else:  
            user_type = "None"
        if user_type == "I":
            return f(*args, **kwargs)
        elif user_type == "None":
            flash("login to access this page", "info")
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
        else:
            flash("login as Influencer to access this page", "danger")
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
    return wrap

def user_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # get function name
        func_name = f.__name__
        try:
            verify_jwt_in_request(optional = True)
        except Exception as exc:
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
        current_user_id = get_jwt_identity()
        if current_user_id is not None:
            user_type = User.query.filter_by(id=current_user_id).first().user_type
        else:  
            user_type = "None"
        if user_type == "U":
            return f(*args, **kwargs)
        elif user_type == "None":
            flash("login to access this page", "info")
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
        else:
            flash("login as User to access this page", "danger")
            return redirect(url_for('login')+"?next="+url_for(func_name, **kwargs))
    return wrap

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
