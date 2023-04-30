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
def create():
    if request.method == 'POST':
        return Subject().create()
    else:
        return render_template('create_subject.html')


@subject_bp.route('/subject/<subject_id>/edit', methods=['GET', 'POST'])
@auth
def edit(subject_id):
    if request.method == 'POST':
        return Subject().edit(subject_id)
    else:
        return Subject().edit_form(subject_id)
