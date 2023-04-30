from flask import Blueprint, request, render_template, session, redirect
from guard.auth import auth

from module.student.models import Student

# Creating a blueprint for user module
student_bp = Blueprint('student_bp', __name__)


@student_bp.route('/students', methods=['GET'])
def index():
    return Student().index()


@student_bp.route('/student/create', methods=['GET', 'POST'])
@auth
def create_user():
    if request.method == 'POST':
        return Student().create()
    else:
        return Student().create_form()
