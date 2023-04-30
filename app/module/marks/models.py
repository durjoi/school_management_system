from flask import jsonify, request, session, redirect, render_template
import uuid
from settings import db
from rabbitmq import publish


# from app import db


class Marks:

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

    def create(self, student_id):
        item = {
            "_id": uuid.uuid4().hex,
            "subject_id": request.form.get('subject'),
            "marks": request.form.get('marks'),
        }

        # convert marks to int and grade
        marks = int(item['marks'])
        if marks >= 80:
            item['grade'] = "A"
        elif marks >= 60:
            item['grade'] = "B"
        elif marks >= 40:
            item['grade'] = "C"
        elif marks >= 20:
            item['grade'] = "D"
        else:
            item['grade'] = "F"

        # find student
        student = db.students.find_one({"_id": student_id})

        if student:
            item['student_id'] = student['_id']

            # find class
            class_ = db.classes.find_one({"_id": student['class']['_id']})

            if class_:
                item['class_id'] = class_['_id']

                # check marks already exists
                existing_marks = db.marks.find_one(
                    {"student_id": item['student_id'], "subject_id": item['subject_id']})

                if (existing_marks):
                    return jsonify({"error": "Marks already exists"}), 400

                # create marks
                db.marks.insert_one(item)

                publish({"type": "marks", "action": "create", "data": item})

                return redirect('/students')
            return jsonify({"error": "Class not found"}), 400
        return jsonify({"error": "Student not found"}), 400

    '''
        Create Class Form
    '''

    def create_marks_form(self, student_id):
        # find student
        student = db.students.find_one({"_id": student_id})

        if student:
            # find classe
            class_ = db.classes.find_one({"_id": student['class']['_id']})

            if class_:
                # find subjects
                subjects = db.subjects.find(
                    {"_id": {"$in": class_['subjects']}})
                subjects = [subject for subject in subjects]
                print(subjects)
                return render_template('create_marks.html', student=student, classes=class_, subjects=subjects)

            return jsonify({"error": "Class not found"}), 400
        return jsonify({"error": "Student not found"}), 400
