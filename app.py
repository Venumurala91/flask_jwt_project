from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Ensure these keys are loaded from the .env file
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config["SECRET_KEY"]="HS256"

# Check if the secret keys are loaded properly
# if not app.config['SECRET_KEY'] or not app.config['JWT_SECRET_KEY']:
#     raise RuntimeError('Both SECRET_KEY and JWT_SECRET_KEY must be set')

# Configure the database URI (SQLite in this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize the database and JWT manager
db = SQLAlchemy()
db.init_app(app)
jwt = JWTManager(app)

# Define the Login_user model for the database
class Login_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __str__(self):
        return f"username: {self.username}"

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    # Extract username and password from the request data
    username = data.get('username')
    password = data.get('password')

    # Find the user in the database
    user = Login_user.query.filter_by(username=username).first()

    # Check if the username exists and the password is correct
    if user is None or user.password != password:
        return jsonify({"message": "Invalid username or password"}), 401

    # Create JWT tokens for the authenticated user
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
