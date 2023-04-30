from flask import Flask, Blueprint, request, render_template, session, jsonify, redirect
from guard.auth import auth

from module.user.models import User

# Creating a blueprint for user module
user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/teachers', methods=['GET'])
def index():
    return User().index()


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return User().login()
    else:
        if (session.get('logged_in')):
            return redirect('/')
        return render_template('login.html')


@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    return User().logout()


@user_bp.route('/teacher/create', methods=['GET', 'POST'])
@auth
def create_user():
    if request.method == 'POST':
        return User().create_teacher()
    else:
        return render_template('create_teacher.html')