from config.db import get_db
import bcrypt
import jwt
import datetime
import os

class User:
    def __init__(self, name, email, password, role='student', student_id=None):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.role = role  # 'student', 'tpo', 'admin'
        self.student_id = student_id
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        db = get_db()
        user_data = {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'student_id': self.student_id,
            'created_at': self.created_at
        }
        result = db.users.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        db = get_db()
        return db.users.find_one({'email': email})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    @staticmethod
    def generate_token(user_id, role):
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, os.getenv('SECRET_KEY', 'your-secret-key'), algorithm='HS256')
        return token
