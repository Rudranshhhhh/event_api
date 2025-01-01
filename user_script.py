import hashlib
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
SUPERADMIN_USERNAME = os.getenv("SUPERADMIN_USERNAME", "superadmin")
SUPERADMIN_PASSWORD = os.getenv("SUPERADMIN_PASSWORD", "superadmin")
SUPERADMIN_EMAIL = os.getenv("SUPERADMIN_EMAIL", "admin@gmail.com")
SUPERADMIN_FIRSTNAME = os.getenv("SUPERADMIN_FIRSTNAME", "Super")
SUPERADMIN_LASTNAME = os.getenv("SUPERADMIN_LASTNAME", "Admin")
SUPERADMIN_MOBILE = os.getenv("SUPERADMIN_MOBILE", "1234567890")

client = MongoClient(MONGO_URI)
db = client.get_default_database()

def create_superadmin():
    existing_user = db.users.find_one({"username": SUPERADMIN_USERNAME})
    if existing_user:
        print("SuperAdmin user already exists.")
        return

    encrypted_password = hashlib.md5(SUPERADMIN_PASSWORD.encode()).hexdigest()
    superadmin_user = {
        "firstName": SUPERADMIN_FIRSTNAME,
        "lastName": SUPERADMIN_LASTNAME,
        "email": SUPERADMIN_EMAIL,
        "userType": "superAdmin",
        "username": SUPERADMIN_USERNAME,
        "password": encrypted_password,
        "mobile": SUPERADMIN_MOBILE,
        "gender": None
    }

    result = db.users.insert_one(superadmin_user)
    if result.inserted_id:
        print("SuperAdmin user created successfully.")
    else:
        print("Failed to create SuperAdmin user.")

if __name__ == "__main__":
    create_superadmin()