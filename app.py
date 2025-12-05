# app.py - Flask REST API (JSON only) with JWT auth, CORS enabled
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_connection
from auth import create_token, jwt_required
from passlib.hash import bcrypt

app = Flask(__name__)
CORS(app)

# Register
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not (name and email and password):
        return jsonify({'error': 'name, email and password required'}), 400

    pw_hash = bcrypt.hash(password)
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)', (name, email, pw_hash))
        conn.commit()
        return jsonify({'message': 'user created'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not (email and password):
        return jsonify({'error': 'email and password required'}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT id, password_hash FROM users WHERE email=%s', (email,))
        user = cur.fetchone()
        if not user or not bcrypt.verify(password, user['password_hash']):
            return jsonify({'error': 'invalid credentials'}), 401
        token = create_token(user['id'])
        return jsonify({'token': token}), 200
    finally:
        cur.close()
        conn.close()

# Protected endpoint example: get current user
@app.route('/me', methods=['GET'])
@jwt_required
def me():
    user_id = request.user_id
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT id, name, email, created_at FROM users WHERE id=%s', (user_id,))
        user = cur.fetchone()
        return jsonify({'user': user})
    finally:
        cur.close()
        conn.close()

# CRUD for items (owned by logged-in user)
@app.route('/items', methods=['GET'])
@jwt_required
def list_items():
    user_id = request.user_id
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT * FROM items WHERE user_id=%s ORDER BY id DESC', (user_id,))
        rows = cur.fetchall()
        return jsonify({'items': rows})
    finally:
        cur.close()
        conn.close()

@app.route('/items', methods=['POST'])
@jwt_required
def create_item():
    user_id = request.user_id
    data = request.get_json() or {}
    title = data.get('title')
    description = data.get('description', '')

    if not title:
        return jsonify({'error': 'title required'}), 400

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO items (user_id, title, description) VALUES (%s, %s, %s)', (user_id, title, description))
        conn.commit()
        return jsonify({'message': 'item created'}), 201
    finally:
        cur.close()
        conn.close()

@app.route('/items/<int:item_id>', methods=['GET'])
@jwt_required
def get_item(item_id):
    user_id = request.user_id
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT * FROM items WHERE id=%s AND user_id=%s', (item_id, user_id))
        item = cur.fetchone()
        if not item:
            return jsonify({'error': 'not found'}), 404
        return jsonify({'item': item})
    finally:
        cur.close()
        conn.close()

@app.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required
def update_item(item_id):
    user_id = request.user_id
    data = request.get_json() or {}
    title = data.get('title')
    description = data.get('description')

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('UPDATE items SET title=%s, description=%s WHERE id=%s AND user_id=%s', (title, description, item_id, user_id))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({'error': 'not found or no permission'}), 404
        return jsonify({'message': 'updated'})
    finally:
        cur.close()
        conn.close()

@app.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required
def delete_item(item_id):
    user_id = request.user_id
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM items WHERE id=%s AND user_id=%s', (item_id, user_id))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({'error': 'not found or no permission'}), 404
        return jsonify({'message': 'deleted'})
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
