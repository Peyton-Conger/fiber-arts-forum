from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify, current_app, send_from_directory
from . import db
from .models import User
from werkzeug.utils import secure_filename
import os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, template_folder='../../templates')

ALLOWED_EXT = {'png','jpg','jpeg','gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form or request.get_json() or {}
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if not username or not password:
            return jsonify({'error': 'username and password required'}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'username exists'}), 400
        u = User(username=username, email=email or None)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        # basic session
        session['user_id'] = u.id
        return redirect(url_for('forum.index'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form or request.get_json() or {}
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('forum.index'))
        flash('Invalid credentials', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('forum.index'))

# --- API endpoints using JWT ---
@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg':'username and password required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'msg':'username exists'}), 400
    u = User(username=username)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    access = create_access_token(identity=u.id)
    return jsonify({'access_token': access}), 201

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access = create_access_token(identity=user.id)
        return jsonify({'access_token': access}), 200
    return jsonify({'msg':'invalid credentials'}), 401

@auth_bp.route('/profile/<int:user_id>', methods=['GET','POST'])
def profile(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        # handle avatar upload
        if 'avatar' in request.files:
            f = request.files['avatar']
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                folder = current_app.config['UPLOAD_FOLDER']
                os.makedirs(folder, exist_ok=True)
                save_path = os.path.join(folder, f"user_{user.id}_" + filename)
                f.save(save_path)
                user.avatar = save_path
                db.session.commit()
                flash('Avatar uploaded', 'success')
                return redirect(url_for('auth.profile', user_id=user.id))
            else:
                flash('Invalid file type', 'danger')
                return redirect(url_for('auth.profile', user_id=user.id))
    return render_template('profile.html', user=user)

@auth_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(folder, filename)
