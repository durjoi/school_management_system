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
def create_user():
    if request.method == 'POST':
        return Class().create_class()
    else:
        return Class().create_class_form()
