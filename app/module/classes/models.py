from flask import jsonify, request, session, redirect, render_template, flash
import uuid
from settings import db
from rabbitmq import publish


# from app import db


class Class:

    '''
        return class list
    '''

    def index(self):
        classes = db.classes.find({})
        classes = [item for item in classes]
        return render_template('classes.html', classes=classes)

    '''
        Create a new class
    '''

    def create(self):
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
            flash('Class name already exists!', 'danger')
            return redirect('/classe/create')

        db.classes.insert_one(item)

        publish({"type": "class", "action": "create", "data": item})
        flash('New class added successfully!', 'success')
        return redirect('/classes')

    def edit_form(self, id):
        class_ = db.classes.find_one({"_id": id})
        teachers = db.users.find({"type": "teacher"})
        subjects = db.subjects.find({})
        return render_template('edit_class.html', class_=class_, teachers=teachers, subjects=subjects)

    def edit(self, id):
        item = {
            "name": request.form.get('name')
        }

        # get teacher
        teacher = db.users.find_one({"_id": request.form.get('teacher')})

        if teacher:
            item['teacher'] = {
                # "teacher_id": "teacher_id",
                "name": teacher['name']
            }

        # get subjects
        subjects = db.subjects.find(
            {"_id": {"$in": request.form.getlist('subjects')}})

        if subjects:
            item['subjects'] = [subject['_id']
                                for subject in subjects]

        # check if user exists in db without the current class

        existing_subject = db.subjects.find_one(
            {"name": item['name'], "_id": {"$ne": id}})

        if existing_subject:
            flash('Class name already exists', 'danger')
            return redirect(f'/class/{id}/edit')

        db.classes.update_one({"_id": id}, {"$set": item})

        # delete from marks table where class id is the current class id and subject id is not in the subjects list
        db.marks.delete_many(
            {"class_id": id, "subject_id": {"$nin": item['subjects']}})

        # if class name updated then update it on students table
        db.students.update_many({"class._id": id}, {
                                "$set": {"class.name": item['name']}})

        item['_id'] = id
        publish({"type": "class", "action": "update", "data": item})
        flash('Class updated successfully!', 'success')
        return redirect('/classes')

    '''
        Create Class Form
    '''

    def create_form(self):
        teachers = db.users.find({"type": "teacher"})
        subjects = db.subjects.find({})
        return render_template('create_class.html', teachers=teachers, subjects=subjects)

    def delete(self, id):
        db.classes.delete_one({"_id": id})

        # delete from marks table where class id is the current class id
        db.marks.delete_many({"class_id": id})

        # update students table where class id is the current class id
        db.students.update_many({"class._id": id}, {"$set": {"class": None}})

        publish({"type": "class", "action": "delete", "data": id})
        flash('Class deleted successfully!', 'success')
        return redirect('/classes')
