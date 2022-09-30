"""
Manages all score related things
"""

from flask import Blueprint, request, jsonify
from .db import get_db, get_user_from_key, generate_secret
from re import match

bp = Blueprint('score', __name__, url_prefix='')

@bp.route('/leaderboard', methods=['GET'])
def score():
    """
    Returns leaderboard
    """

    db = get_db()
    users = db.execute(
        "SELECT name, score, day FROM user WHERE score>0 ORDER BY score DESC "
    ).fetchall()

    data = list()
    for user in users:
        data.append({"username": user["name"], "score": user["score"], "date": user["day"]})

    return jsonify(data)

@bp.route('/login', methods=['POST'])
def login():
    """
    Checks if a key is valid and returns user informations
    """

    db = get_db()
    key = request.get_json().get('key')

    if not key:
        return {'error': "Key is required"}, 401

    user = get_user_from_key(key)

    if user is None:
        return {'error': "Unknown user"}, 404

    return {
        'username': user['name'],
        'key': user['key'],
        'score': user['score'],
    }

@bp.route('/register', methods=['POST'])
def register_new():
    """
    Creates a new user in the database
    """

    db = get_db()
    username = request.get_json().get("username")

    if not match(r"^[\w\d]{1}[\w\d\s\-\_]{1,24}[\w\d]{1}$", username):
        return {'error': "Username invalid"}, 400

    key = generate_secret()

    try:
        db.execute(
            "INSERT INTO user (name, key, score) VALUES (?, ?, ?)", (username, key, 0)
        )
        db.commit()
    except db.IntegrityError:
        return {'Error': "Username already taken"}, 400

    return {
        'username': username,
        'key': key,
    }
