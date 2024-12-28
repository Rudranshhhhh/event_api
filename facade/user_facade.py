import logging
import hashlib
import jwt
from flask import current_app
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from models.user import User

class UserFacade:
    @staticmethod
    def create_user(firstName, lastName, email, userType, username, password, mobile=None, gender=None):
        try:
            # Encrypt the password using MD5
            encrypted_password = hashlib.md5(password.encode()).hexdigest()
            user = User(
                firstName=firstName,
                lastName=lastName,
                email=email,
                userType=userType,
                username=username,
                password=encrypted_password,
                mobile=mobile,
                gender=gender
            )
            result = current_app.mongo.db.users.insert_one(user.to_dict())
            user._id = str(result.inserted_id)
            return user.to_dict()
        except Exception as e:
            logging.error("Error creating user: %s", e)
            raise

    @staticmethod
    def get_user(user_id):
        try:
            user_data = current_app.mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user_data:
                user = User.from_dict(user_data)
                return user.to_dict()
            return None
        except Exception as e:
            logging.error("Error getting user: %s", e)
            raise

    @staticmethod
    def update_user(user_id, firstName=None, lastName=None, email=None, userType=None, username=None, password=None, mobile=None, gender=None):
        try:
            update_fields = {}
            if firstName:
                update_fields["firstName"] = firstName
            if lastName:
                update_fields["lastName"] = lastName
            if email:
                update_fields["email"] = email
            if userType:
                update_fields["userType"] = userType
            if username:
                update_fields["username"] = username
            if password:
                update_fields["password"] = hashlib.md5(password.encode()).hexdigest()
            if mobile:
                update_fields["mobile"] = mobile
            if gender:
                update_fields["gender"] = gender
            result = current_app.mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": update_fields}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error("Error updating user: %s", e)
            raise

    @staticmethod
    def delete_user(user_id):
        try:
            result = current_app.mongo.db.users.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception as e:
            logging.error("Error deleting user: %s", e)
            raise

    @staticmethod
    def login(username, password):
        encrypted_password = hashlib.md5(password.encode()).hexdigest()
        user_data = current_app.mongo.db.users.find_one({"username": username, "password": encrypted_password})
        if user_data:
            user = User.from_dict(user_data)
            # Generate JWT token
            token = jwt.encode({
                'user_id': user._id,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }, current_app.config['SECRET_KEY'], algorithm='HS256')
            return {'token': token}
        return None

    @staticmethod
    def get_users(page, size):
        try:
            skip = (page - 1) * size
            users_cursor = current_app.mongo.db.users.find().skip(skip).limit(size)
            users = [User.from_dict(user).to_dict() for user in users_cursor]
            total_users = current_app.mongo.db.users.count_documents({})
            return {
                "users": users,
                "pageSize": size,
                "currentPage": page,
                "totalData": total_users
            }
        except Exception as e:
            logging.error("Error getting users: %s", e)
            raise