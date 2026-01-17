from passlib.hash import bcrypt
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from .db import get_connection


def signup():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    

    if len(password.encode("utf-8")) > 72:
        return {
            "error": "Password must be 72 characters or fewer"
        }, 400




    password_hash = bcrypt.hash(password)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
        (email, password_hash)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User created"}), 201

def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password_hash FROM users WHERE email = %s",
        (email,)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    user_id, password_hash = user

    if not bcrypt.verify(password, password_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    # Convert user_id to string for JWT compatibility
    token = create_access_token(identity=str(user_id))

    return jsonify({"access_token": token})
