from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from controllers.chat_controller import process_chat

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/chat')
def main_chat_page():
    if 'user' in session:
        username = session['user'][1]
        return render_template('chatpage.html', username=username)
    return redirect(url_for('login_bp.login'))

@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    response = process_chat(user_input)
    return jsonify({'response': response})
