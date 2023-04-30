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


@marks_bp.route('/student/<student_id>/marks', methods=['GET'])
@auth
def get_student_marks(student_id):
    return Marks().get_student_marks(student_id)


@marks_bp.route('/marks/<marks_id>/delete', methods=['POST'])
@auth
def delete_user(marks_id):
    return Marks().delete(marks_id)


@marks_bp.route('/marks/<marks_id>/edit', methods=['POST'])
@auth
def edit_user(marks_id):
    return Marks().edit(marks_id)
