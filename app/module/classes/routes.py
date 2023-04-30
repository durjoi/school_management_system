from flask import Blueprint, request, render_template, session, redirect
from guard.auth import auth

from module.classes.models import Class

# Creating a blueprint for user module
class_bp = Blueprint('class_bp', __name__)


@class_bp.route('/classes', methods=['GET'])
def index():
    return Class().index()


@class_bp.route('/class/create', methods=['GET', 'POST'])
@auth
def create():
    if request.method == 'POST':
        return Class().create()
    else:
        return Class().create_form()


@class_bp.route('/class/<class_id>/edit', methods=['GET', 'POST'])
@auth
def edit(class_id):
    if request.method == 'POST':
        return Class().edit(class_id)
    else:
        return Class().edit_form(class_id)


@class_bp.route('/class/<class_id>/delete', methods=['POST'])
@auth
def delete(class_id):
    return Class().delete(class_id)
