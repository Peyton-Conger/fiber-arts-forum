from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app, flash
from . import db
from .models import Thread, Post, User
from werkzeug.utils import secure_filename
import os

forum_bp = Blueprint('forum', __name__, template_folder='../../templates')

ALLOWED_EXT = {'png','jpg','jpeg','gif','pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

def current_user():
    uid = session.get('user_id')
    if not uid:
        return None
    return User.query.get(uid)

@forum_bp.route('/')
def index():
    q = request.args.get('q')
    craft = request.args.get('craft')
    threads = Thread.query
    if q:
        threads = threads.filter(Thread.title.ilike(f"%{q}%"))
    if craft:
        threads = threads.filter_by(craft=craft)
    threads = threads.order_by(Thread.created_at.desc()).all()
    return render_template('index.html', threads=threads, current_user=current_user())

@forum_bp.route('/thread/new', methods=['GET','POST'])
def new_thread():
    user = current_user()
    if request.method == 'POST':
        data = request.form or request.get_json() or {}
        title = data.get('title')
        craft = data.get('craft')
        body = data.get('body')
        if not user:
            return jsonify({'error': 'authentication required'}), 401
        if not title or not body:
            return jsonify({'error': 'title and body required'}), 400
        t = Thread(title=title, craft=craft, user_id=user.id)
        db.session.add(t)
        db.session.commit()
        p = Post(body=body, thread_id=t.id, user_id=user.id)
        # handle optional attachment
        if 'attachment' in request.files:
            f = request.files['attachment']
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                folder = current_app.config['UPLOAD_FOLDER']
                os.makedirs(folder, exist_ok=True)
                save_path = os.path.join(folder, f"thread_{t.id}_" + filename)
                f.save(save_path)
                p.attachment = save_path
        db.session.add(p)
        db.session.commit()
        flash('Thread created', 'success')
        return redirect(url_for('forum.view_thread', thread_id=t.id))
    return render_template('new_thread.html', current_user=user)

@forum_bp.route('/thread/<int:thread_id>', methods=['GET','POST'])
def view_thread(thread_id):
    user = current_user()
    t = Thread.query.get_or_404(thread_id)
    if request.method == 'POST':
        data = request.form or request.get_json() or {}
        body = data.get('body')
        if not user:
            return jsonify({'error': 'authentication required'}), 401
        if not body:
            return jsonify({'error': 'body required'}), 400
        p = Post(body=body, thread_id=t.id, user_id=user.id)
        if 'attachment' in request.files:
            f = request.files['attachment']
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                folder = current_app.config['UPLOAD_FOLDER']
                os.makedirs(folder, exist_ok=True)
                save_path = os.path.join(folder, f"post_{t.id}_" + filename)
                f.save(save_path)
                p.attachment = save_path
        db.session.add(p)
        db.session.commit()
        flash('Reply posted', 'success')
        return redirect(url_for('forum.view_thread', thread_id=thread_id))
    return render_template('thread.html', thread=t, current_user=user)

@forum_bp.route('/thread/<int:thread_id>/edit', methods=['GET','POST'])
def edit_thread(thread_id):
    user = current_user()
    t = Thread.query.get_or_404(thread_id)
    if not user or user.id != t.user_id:
        flash('Not authorized', 'danger')
        return redirect(url_for('forum.view_thread', thread_id=thread_id))
    if request.method == 'POST':
        data = request.form or {}
        t.title = data.get('title') or t.title
        t.craft = data.get('craft') or t.craft
        db.session.commit()
        flash('Thread updated', 'success')
        return redirect(url_for('forum.view_thread', thread_id=thread_id))
    return render_template('edit_thread.html', thread=t, current_user=user)

@forum_bp.route('/thread/<int:thread_id>/delete', methods=['POST'])
def delete_thread(thread_id):
    user = current_user()
    t = Thread.query.get_or_404(thread_id)
    if not user or user.id != t.user_id:
        flash('Not authorized', 'danger')
        return redirect(url_for('forum.view_thread', thread_id=thread_id))
    db.session.delete(t)
    db.session.commit()
    flash('Thread deleted', 'success')
    return redirect(url_for('forum.index'))

@forum_bp.route('/post/<int:post_id>/edit', methods=['GET','POST'])
def edit_post(post_id):
    user = current_user()
    p = Post.query.get_or_404(post_id)
    if not user or user.id != p.user_id:
        flash('Not authorized', 'danger')
        return redirect(url_for('forum.view_thread', thread_id=p.thread_id))
    if request.method == 'POST':
        p.body = request.form.get('body') or p.body
        db.session.commit()
        flash('Post updated', 'success')
        return redirect(url_for('forum.view_thread', thread_id=p.thread_id))
    return render_template('edit_post.html', post=p, current_user=user)

@forum_bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    user = current_user()
    p = Post.query.get_or_404(post_id)
    if not user or user.id != p.user_id:
        flash('Not authorized', 'danger')
        return redirect(url_for('forum.view_thread', thread_id=p.thread_id))
    thread_id = p.thread_id
    db.session.delete(p)
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('forum.view_thread', thread_id=thread_id))
