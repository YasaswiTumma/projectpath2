from flask import Flask, jsonify
from flask_cors import CORS
from routes.auth import auth_bp
from config.db import get_db

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def home():
    return jsonify({'message': 'Path2Placement API'})

if __name__ == '__main__':
    app.run(debug=True)
