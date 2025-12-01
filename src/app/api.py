from flask import Blueprint, jsonify, request
from .models import Thread, Post, User
from . import db
from flask_jwt_extended import jwt_required, get_jwt_identity

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/threads', methods=['GET'])
def list_threads():
    threads = Thread.query.all()
    return jsonify([{'id':t.id, 'title':t.title, 'craft':t.craft} for t in threads])

@api_bp.route('/threads', methods=['POST'])
@jwt_required()
def create_thread():
    uid = get_jwt_identity()
    data = request.get_json() or {}
    title = data.get('title')
    body = data.get('body')
    craft = data.get('craft')
    if not title or not body:
        return jsonify({'msg':'title and body required'}), 400
    t = Thread(title=title, craft=craft, user_id=uid)
    db.session.add(t)
    db.session.commit()
    p = Post(body=body, thread_id=t.id, user_id=uid)
    db.session.add(p)
    db.session.commit()
    return jsonify({'id': t.id, 'title': t.title}), 201

@api_bp.route('/threads/<int:thread_id>/posts', methods=['POST'])
@jwt_required()
def api_post_reply(thread_id):
    uid = get_jwt_identity()
    data = request.get_json() or {}
    body = data.get('body')
    if not body:
        return jsonify({'msg':'body required'}), 400
    p = Post(body=body, thread_id=thread_id, user_id=uid)
    db.session.add(p)
    db.session.commit()
    return jsonify({'id': p.id}), 201
