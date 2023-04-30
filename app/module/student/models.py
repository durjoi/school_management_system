from flask import jsonify, request, session, redirect, render_template, flash
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

        # check if student exists in db

        existing_student = db.students.find_one(
            {"registration": item['registration']})

        if existing_student:
            flash('Registration no already exists', 'danger')
            return redirect('/student/create')

        db.students.insert_one(item)

        publish({"type": "student", "action": "create", "data": item})
        flash('New student added successfully', 'success')
        return redirect('/students')

    def edit_form(self, id):
        student = db.students.find_one({"_id": id})
        classes = db.classes.find({})
        classes = [item for item in classes]
        return render_template('edit_student.html', student=student, classes=classes)

    def edit(self, id):

        # get the student
        student = db.students.find_one({"_id": id})

        item = {
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

        # check if student exists in db without current student

        existing_student = db.students.find_one(
            {"registration": item['registration'], "_id": {"$ne": id}})

        if existing_student:
            flash('Student registration no already exists', 'danger')
            return redirect(f'/student/{id}/edit')

        db.students.update_one({"_id": id}, {"$set": item})

        # if previous class is different from current class then remove all the marks of this user where class id is previous class id

        db.marks.delete_many(
            {"student._id": id, "class._id": student['class']['_id']})

        item['_id'] = id

        publish({"type": "student", "action": "update", "data": item})
        flash('Student updated successfully', 'success')
        return redirect('/students')
    '''
        Create Class Form
    '''

    def create_form(self):
        classes = db.classes.find({})
        classes = [item for item in classes]
        return render_template('create_student.html', classes=classes)

    def delete(self, id):
        db.students.delete_one({"_id": id})
        # delete marks table where student id is the current student id
        db.marks.delete_many({"student_id": id})

        publish({"type": "student", "action": "delete", "data": id})
        flash('Student deleted successfully', 'success')
        return redirect('/students')
