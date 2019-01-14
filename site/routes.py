# This file contains the different routes of the site

# Import
from flask import render_template, url_for, flash, redirect, request, jsonify, send_file, make_response
from site import app, db, bcrypt
from site.forms import LoginForm, RegistrationForm
from site.models import User
from flask_login import login_user, current_user, logout_user, login_required 
from io import BytesIO
import json

is_maintenance_mode = False

'''
@app.before_request
def check_for_maintenance():
    # Before request

'''

'''
@app.context_processor
def context_processor():
    return dict(is_maintenance_mode=is_maintenance_mode)
'''
