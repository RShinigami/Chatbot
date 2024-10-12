from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from config import db_config
from views.login import login_bp
from views.chat import chat_bp
from views.database_chat import database_chat_bp  # Import the new blueprint

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '2cd4f12eeb57982d1f7b4e5d9a2e23da')
CORS(app)

# Register Blueprints
app.register_blueprint(login_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(database_chat_bp) 

if __name__ == '__main__':
    app.run(debug=True)
