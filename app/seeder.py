import uuid
from settings import db
from passlib.hash import pbkdf2_sha256
from rabbitmq import publish


# from app import db


class UserSeeder:
    def createAdmin(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": "Admin User",
            "email": "admin@admin.com",
            "password": "password",
            "type": "admin"
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # check if user exists in db

        existing_user = db.users.find_one({"email": user['email']})

        if existing_user:
            print("Admin user already exists")
            return

        db.users.insert_one(user)

        publish({"type": "user", "action": "create", "data": user})

        print("Admin user created successfully")


UserSeeder().createAdmin()
