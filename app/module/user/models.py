from flask import jsonify, request, session, redirect, render_template
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

    def create_teacher(self):
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
            return jsonify({"error": "Email address already in use"}), 401

        db.users.insert_one(user)

        publish({"type": "user", "action": "create", "data": user})

        return redirect('/')

    '''
        Login function for user
    '''

    def login(self):

        if (session.get('logged_in')):
            return jsonify({"error": "Already Logged in"}), 401

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

                return redirect('/')
            else:
                return jsonify({"error": "Invalid username/password"}), 401
        else:
            return jsonify({"error": "Invalid username/password"}), 401

    '''
        function for logout
        this function clears the session and redirects to login page
    '''

    def logout(self):
        session.clear()
        return redirect('/')
