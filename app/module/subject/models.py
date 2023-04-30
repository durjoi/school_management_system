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

    def create_subject(self):
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
