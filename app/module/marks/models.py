from flask import jsonify, request, session, redirect, render_template, flash
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
            item['grade'] = "A+"
        elif marks >= 70:
            item['grade'] = "A"
        elif marks >= 60:
            item['grade'] = "B"
        elif marks >= 30:
            item['grade'] = "C"
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
                flash('Marks added successfully!', 'success')
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

    def get_class_report(self, class_id, subject_id=None):

        # get all classes
        classes = db.classes.find({})
        classes = [item for item in classes]

        if subject_id:
            # Get the total number of students in the class
            total_students = db.students.count_documents(
                {"class._id": class_id})

            # find class with class_id from classes
            class_ = db.classes.find_one({"_id": class_id})
            # get all subjects of this class
            subjects = db.subjects.find({"_id": {"$in": class_['subjects']}})
            subjects = [item for item in subjects]
            # Return the report in the desired format

            if (total_students == 0):
                return "No students in this class"

            # Get the total number of students who passed the subject
            passed_students = db.marks.count_documents(
                {'class_id': class_id, 'subject_id': subject_id, 'grade': {'$ne': 'F'}})

            # Get the grade-wise count of students who passed the subject
            grades = ['A+', 'A', 'B', 'C', 'F']
            grade_counts = {}
            for grade in grades:
                grade_counts[grade] = db.marks.count_documents(
                    {'class_id': class_id, 'subject_id': subject_id, 'grade': grade})

            # Calculate the percentage of students who passed the subject
            pass_percentage = (passed_students / total_students) * 100
            # convert pass percentage to 2 decimal places
            pass_percentage = "{:.2f}".format(pass_percentage)
            # Create the report
            report = []
            for grade in grades:
                # convert grade percentage to 2 decimal places

                grade_percentage = (grade_counts[grade] / total_students) * 100
                grade_percentage = "{:.2f}".format(grade_percentage)
                report.append({
                    'grade': grade,
                    'students': grade_counts[grade],
                    'percentage': grade_percentage
                })

            response = {
                "report_type": "subject",
                'total_students': total_students,
                'pass_percentage': pass_percentage,
                'report': report,
                'subjects': subjects,
                'classes': classes,
                'selected_class_id': class_id,
                'selected_subject_id': subject_id
            }

            return jsonify(response)

        if not class_id:
            # select first class
            class_ = db.classes.find_one({})
            class_id = class_['_id']

        pipeline = [
            {"$match": {"class_id": class_id}},
            {"$group": {"_id": {"class_id": "$class_id", "subject_id": "$subject_id"},
                        "pass_count": {"$sum": {"$cond": [{"$ne": ["$grade", "F"]}, 100, 0]}},
                        "total_count": {"$sum": 1},
                        "fail_count": {"$sum": {"$cond": [{"$eq": ["$grade", "F"]}, 100, 0]}}}},
            {"$lookup": {"from": "subjects", "localField": "_id.subject_id",
                         "foreignField": "_id", "as": "subject"}},
            {"$project": {"_id": 0, "subject_name": {"$arrayElemAt": [
                "$subject.name", 0]}, "pass_count": 1, "fail_count": 1, "total_count": 1}},
            {"$group": {"_id": "$_id.class_id", "subjects": {"$push": {"subject_name": "$subject_name",
                                                                       "pass_count": "$pass_count", "fail_count": "$fail_count", "total_count": "$total_count"}}, "total_students": {"$sum": "$total_count"}}},
            {"$unwind": "$subjects"},
            {"$project": {"_id": 0, "subject_name": "$subjects.subject_name", "pass_count": "$subjects.pass_count", "fail_count": "$subjects.fail_count", "total_count": "$subjects.total_count",
                          "pass_percentage": {"$multiply": [{"$divide": ["$subjects.pass_count", "$subjects.total_count"]}, 100]}}},
            {"$group": {"_id": "$subject_name", "total_count": {"$first": "$total_count"}, "pass_count": {
                "$sum": "$pass_count"}, "fail_count": {"$sum": "$fail_count"}, "pass_percentage": {"$avg": {"$cond": [{"$gte": [{"$divide": ["$pass_count", "$total_count"]}, 0.4]}, {"$divide": ["$pass_count", "$total_count"]}, 0]}}}},
            {"$project": {"_id": 0, "subject_name": "$_id",
                          "total_count": 1, "pass_count": 1, "pass_percentage": 1, "fail_count": 1, "total_students": {"$sum": "$total_count"}}}
        ]
        result = list(db.marks.aggregate(pipeline))

        # find class with class_id from classes
        class_ = db.classes.find_one({"_id": class_id})
        # get all subjects of this class
        subjects = db.subjects.find({"_id": {"$in": class_['subjects']}})
        subjects = [item for item in subjects]

        total_student = db.students.count_documents({"class._id": class_id})

        response = {
            "report_type": "class",
            "total_students": total_student,
            "report": result,
            'subjects': subjects,
            'classes': classes,
            'selected_class_id': class_id,
        }

        return jsonify(response)
