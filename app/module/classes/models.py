from flask import jsonify, request, session, redirect, render_template
import uuid
from settings import db
from rabbitmq import publish


# from app import db


class Class:

    '''
        return subject list
    '''

    def index(self):
        classes = db.classes.find({})
        classes = [item for item in classes]
        return render_template('classes.html', classes=classes)

    '''
        Create a new user as teacher
    '''

    def create_class(self):
        item = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name')
        }

        # get teacher
        teacher = db.users.find_one({"_id": request.form.get('teacher')})

        if teacher:
            item['teacher'] = {
                "_id": teacher['_id'],
                # "teacher_id": "teacher_id",
                "name": teacher['name']
            }

        # get subjects
        subjects = db.subjects.find(
            {"_id": {"$in": request.form.getlist('subjects')}})

        if subjects:
            item['subjects'] = [subject['_id']
                                for subject in subjects]

        # check if user exists in db

        existing_subject = db.subjects.find_one({"name": item['name']})

        if existing_subject:
            return jsonify({"error": "Class already exists"}), 401

        db.classes.insert_one(item)

        publish({"type": "class", "action": "create", "data": item})

        return redirect('/classes')

    '''
        Create Class Form
    '''

    def create_class_form(self):
        teachers = db.users.find({"type": "teacher"})
        subjects = db.subjects.find({})
        return render_template('create_class.html', teachers=teachers, subjects=subjects)
