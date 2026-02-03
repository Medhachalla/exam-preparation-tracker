import bcrypt
import hashlib
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from .db import get_connection
import traceback


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256 + bcrypt.

    We first hash the UTF-8 encoded password with SHA-256 to remove
    bcrypt's 72-byte input limitation, then bcrypt-hash the fixed-size
    SHA-256 digest. The returned value is a UTF-8 string safe to store.
    """
    pw_bytes = password.encode("utf-8")
    digest = hashlib.sha256(pw_bytes).digest()
    bcrypt_hash = bcrypt.hashpw(digest, bcrypt.gensalt())
    return bcrypt_hash.decode("utf-8")


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify a password against a stored bcrypt hash that was created
    using the SHA-256 + bcrypt scheme above.
    """
    try:
        pw_bytes = password.encode("utf-8")
        digest = hashlib.sha256(pw_bytes).digest()
        return bcrypt.checkpw(digest, stored_hash.encode("utf-8"))
    except Exception:
        # Any error during verification should be treated as a failure
        return False


def signup():
    try:
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        try:
            password_hash = hash_password(password)
        except Exception as e:
            # Log server-side and return generic error to client
            print(f"Error hashing password for signup: {e}")
            traceback.print_exc()
            return jsonify({"error": "Failed to process password"}), 500

        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                (email, password_hash),
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            msg = str(e)
            print(f"Error creating user: {msg}")
            traceback.print_exc()
            # Basic duplicate email detection; keep message generic
            if "duplicate key" in msg or "unique constraint" in msg:
                return jsonify({"error": "Email is already registered"}), 400
            return jsonify({"error": "Failed to create user"}), 500
        finally:
            cur.close()
            conn.close()

        return jsonify({"message": "User created"}), 201

    except Exception as e:
        print(f"Unhandled error in signup: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


def login():
    try:
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT id, password_hash FROM users WHERE email = %s",
                (email,),
            )
            user = cur.fetchone()
        finally:
            cur.close()
            conn.close()

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        user_id, password_hash = user

        if not verify_password(password, password_hash):
            return jsonify({"error": "Invalid credentials"}), 401

        # Convert user_id to string for JWT compatibility
        token = create_access_token(identity=str(user_id))

        return jsonify({"access_token": token}), 200

    except Exception as e:
        print(f"Unhandled error in login: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
