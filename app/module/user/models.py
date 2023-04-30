from flask import jsonify, request, session, redirect, render_template, flash
import uuid
from settings import db
from passlib.hash import pbkdf2_sha256
from rabbitmq import publish


# from app import db


class User:

    '''
        this function creates session for user when logged in
    '''

    def start_session(self, user):
        session['logged_in'] = True
        del user['password']
        session['user'] = user

    '''
        return users list
    '''

    def index(self):
        users = db.users.find({"type": "teacher"})
        users = [user for user in users]
        return render_template('teachers.html', teachers=users)

    '''
        Create a new user as teacher
    '''

    def create(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "type": "teacher"
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # check if user exists in db

        existing_user = db.users.find_one({"email": user['email']})

        if existing_user:
            flash('Email address already in use', 'danger')
            return redirect('/teacher/create')

        db.users.insert_one(user)

        publish({"type": "user", "action": "create", "data": user})

        flash('New teacher added successfully!', 'success')
        return redirect('/teachers')

    def edit_form(self, teacher_id):
        teacher = db.users.find_one({"_id": teacher_id})
        return render_template('edit_teacher.html', teacher=teacher)

    def edit(self, teacher_id):
        user = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            # "password": request.form.get('password'),
        }

        if (request.form.get('password')):
            user['password'] = pbkdf2_sha256.encrypt(
                request.form.get('password'))

        # check if user exists in db without the current user

        existing_user = db.users.find_one(
            {"email": user['email'], "_id": {"$ne": teacher_id}})

        if existing_user:
            flash('Email address already in use', 'danger')
            return redirect(f'/teacher/{teacher_id}/edit')

        db.users.update_one({"_id": teacher_id}, {"$set": user})

        user['_id'] = teacher_id
        publish({"type": "user", "action": "update", "data": user})
        flash('Teacher updated successfully!', 'success')
        return redirect('/teachers')

    '''
        Login function for user
    '''

    def login(self):

        if (session.get('logged_in')):
            flash('Already Logged in', 'info')
            return redirect('/')

        user = {
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # check if user exists in db

        user = db.users.find_one({"email": user['email']})

        if user:
            if pbkdf2_sha256.verify(request.form.get('password'), user['password']):
                # save to session
                self.start_session(user)
                flash('Logged in successfully!', 'success')
                return redirect('/')
            else:
                flash('Invalid username/password', 'danger')
                return redirect('/login')
        else:
            flash('Invalid username/password', 'danger')
            return redirect('/login')

    '''
        function for logout
        this function clears the session and redirects to login page
    '''

    def logout(self):
        session.clear()
        flash('Logged out successfully!', 'info')
        return redirect('/')
