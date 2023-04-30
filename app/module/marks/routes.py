from flask import Blueprint, request, render_template, session, redirect
from guard.auth import auth

from module.marks.models import Marks

# Creating a blueprint for user module
marks_bp = Blueprint('marks_bp', __name__)


@marks_bp.route('/classes', methods=['GET'])
def index():
    return Marks().index()


@marks_bp.route('<student_id>/marks/create', methods=['GET', 'POST'])
@auth
def create_user(student_id):
    if request.method == 'POST':
        return Marks().create(student_id)
    else:
        return Marks().create_marks_form(student_id)


@marks_bp.route('/class_report')
def get_class_report():
    class_id = request.args.get('class_id')
    subject_id = request.args.get('subject_id')
    return Marks().get_class_report(class_id, subject_id)