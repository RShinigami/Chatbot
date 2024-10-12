from flask import Blueprint, render_template, request
from controllers.auth_controller import login_user, logout_user

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        return login_user(username, password)
    return render_template('login.html')

@login_bp.route('/logout', methods=['POST'])
def logout():
    return logout_user()
