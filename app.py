from flask import Flask
from routes.user_routes import user_bp
from routes.event_routes import event_bp
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
ver = os.getenv("VERSION", "v1")
app.config["VERSION"] = ver

mongo = PyMongo(app)
app.mongo = mongo
print("version:", ver)
app.register_blueprint(user_bp, url_prefix=f'/{ver}/api')
app.register_blueprint(event_bp, url_prefix=f'/{ver}/api')

if __name__ == '__main__':
    app.run(debug=True)
