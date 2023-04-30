from flask import jsonify, request, session, redirect, render_template
import uuid
from settings import db
from rabbitmq import publish


# from app import db


class Subject:

    '''
        return subject list
    '''

    def index(self):
        subjects = db.subjects.find({})
        subjects = [subject for subject in subjects]
        return render_template('subjects.html', subjects=subjects)

    '''
        Create a new subject
    '''

    def create(self):
        subject = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name')
        }

        # check if subject exists in db

        existing_subject = db.subjects.find_one({"name": subject['name']})

        if existing_subject:
            return jsonify({"error": "Subject already exists"}), 401

        db.subjects.insert_one(subject)

        publish({"type": "subject", "action": "create", "data": subject})

        return redirect('/subjects')

    def edit_form(self, id):
        subject = db.subjects.find_one({"_id": id})
        return render_template('edit_subject.html', subject=subject)

    def edit(self, id):
        subject = {
            "name": request.form.get('name')
        }

        # check if subject exists in db without the current subject
        existing_subject = db.subjects.find_one(
            {"name": subject['name'], "_id": {"$ne": id}})

        if existing_subject:
            return jsonify({"error": "Subject already exists"}), 401

        db.subjects.update_one({"_id": id}, {"$set": subject})

        subject['_id'] = id

        publish({"type": "subject", "action": "update", "data": subject})

        return redirect('/subjects')
