from flask import session, jsonify, url_for
from models.user import User

def login_user(username, password):
    user = User.authenticate(username, password)
    if user:
        session['user'] = user
        return jsonify({'redirect': url_for('chat_bp.main_chat_page')})
    else:
        return jsonify({'error': 'Invalid username or password'})

def logout_user():
    session.clear()
    return jsonify({'redirect': url_for('login_bp.login')})
