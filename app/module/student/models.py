from flask import jsonify, request, session, redirect, render_template
import uuid
from settings import db
from rabbitmq import publish


# from app import db


class Student:

    '''
        return student list
    '''

    def index(self):
        students = db.students.find({})
        students = [student for student in students]
        return render_template('students.html', students=students)

    '''
        Create a new student
    '''

    def create(self):
        item = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "registration": request.form.get('registration'),
        }

        # get class
        class_ = db.classes.find_one({"_id": request.form.get('class')})

        if class_:
            item['class'] = {
                "_id": class_['_id'],
                "name": class_['name']
            }

        # check if user exists in db

        existing_student = db.students.find_one(
            {"registration": item['registration']})

        if existing_student:
            return jsonify({"error": "Student already exists"}), 401

        db.students.insert_one(item)

        publish({"type": "student", "action": "create", "data": item})

        return redirect('/students')

    '''
        Create Class Form
    '''

    def create_form(self):
        classes = db.classes.find({})
        classes = [item for item in classes]
        return render_template('create_student.html', classes=classes)
