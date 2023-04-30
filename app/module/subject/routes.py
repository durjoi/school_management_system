from flask import Blueprint, request, render_template, session, redirect
from guard.auth import auth

from module.subject.models import Subject

# Creating a blueprint for user module
subject_bp = Blueprint('subject_bp', __name__)


@subject_bp.route('/subjects', methods=['GET'])
def index():
    return Subject().index()


@subject_bp.route('/subject/create', methods=['GET', 'POST'])
@auth
def create_user():
    if request.method == 'POST':
        return Subject().create_subject()
    else:
        return render_template('create_subject.html')
