print("APP FILE LOADED")

from flask import Flask, jsonify
from flask_cors import CORS
from .db import get_connection
from flask import request
from .auth import signup, login
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity



from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables from backend/.env
BASE_DIR = Path(__file__).resolve().parents[2]  # points to backend/
load_dotenv(BASE_DIR / ".env")


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
# Explicitly set JWT token location to Authorization header
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
print("JWT_SECRET_KEY loaded:", bool(app.config["JWT_SECRET_KEY"]))

jwt = JWTManager(app)

# JWT Error handlers for better debugging
@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    print(f"Invalid JWT token: {error_string}")
    # Treat invalid tokens as unauthorized (401) so the frontend can redirect
    return jsonify({"error": f"Invalid token: {error_string}"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error_string):
    print(f"Missing JWT token: {error_string}")
    return jsonify({"error": f"Authorization required: {error_string}"}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print(f"Expired JWT token: {jwt_payload}")
    return jsonify({"error": "Token has expired"}), 401

CORS(
    app,
    origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
)



app.add_url_rule("/auth/signup", view_func=signup, methods=["POST"])
app.add_url_rule("/auth/login", view_func=login, methods=["POST"])

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/subjects/<int:subject_id>/topics")
def get_topics(subject_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, name, status
        FROM topics
        WHERE subject_id = %s
        ORDER BY id;
        """,
        (subject_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    topics = []
    for r in rows:
        topics.append({
            "id": r[0],
            "name": r[1],
            "status": r[2]
        })

    return jsonify(topics)


@app.route("/topics/<int:topic_id>/status", methods=["PUT"])
def update_topic_status(topic_id):
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["Not Started", "In Progress", "Completed"]:
        return jsonify({"error": "Invalid status"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE topics
        SET status = %s
        WHERE id = %s;
        """,
        (new_status, topic_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Status updated"})

@app.route("/subjects", methods=["GET"])
@jwt_required()
def get_subjects():
    user_id_str = get_jwt_identity()
    # Convert string identity back to int for database query
    user_id = int(user_id_str) if user_id_str else None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name FROM subjects WHERE user_id = %s ORDER BY id;",
        (user_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    subjects = []
    for r in rows:
        subjects.append({
            "id": r[0],
            "name": r[1]
        })

    return jsonify(subjects)


@app.route("/subjects", methods=["POST"])
@jwt_required()
def add_subject():
    data = request.get_json()
    name = data.get("name")
    user_id_str = get_jwt_identity()
    # Convert string identity back to int for database query
    user_id = int(user_id_str) if user_id_str else None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO subjects (user_id, name) VALUES (%s, %s) RETURNING id;",
         (user_id, name)
    )

    subject_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({ "id": subject_id, "name": name })

@app.route("/subjects/<int:subject_id>/units", methods=["POST"])
def add_unit(subject_id):
    data = request.get_json()
    name = data.get("name")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO units (subject_id, name) VALUES (%s, %s) RETURNING id;",
        (subject_id, name)
    )
    unit_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({ "id": unit_id, "name": name })

@app.route("/units/<int:unit_id>/topics", methods=["POST"])
def add_topic(unit_id):
    data = request.get_json()
    name = data.get("name")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO topics (unit_id, name, status) VALUES (%s, %s, 'Not Started') RETURNING id;",
        (unit_id, name)
    )
    topic_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({ "id": topic_id, "name": name, "status": "Not Started" })

@app.route("/subjects/<int:subject_id>/units", methods=["GET"])
def get_units(subject_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM units WHERE subject_id = %s;", (subject_id,))
    units = cur.fetchall()

    result = []

    for u in units:
        cur.execute("SELECT id, name, status FROM topics WHERE unit_id = %s;", (u[0],))
        topics = cur.fetchall()

        result.append({
            "id": u[0],
            "name": u[1],
            "topics": [
                { "id": t[0], "name": t[1], "status": t[2] } for t in topics
            ]
        })

    cur.close()
    conn.close()
    return jsonify(result)

@app.route("/units/<int:unit_id>/topics", methods=["GET"])
def get_topics_for_unit(unit_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, status FROM topics WHERE unit_id = %s ORDER BY id",
        (unit_id,)
    )

    topics = [
        {"id": r[0], "name": r[1], "status": r[2]}
        for r in cur.fetchall()
    ]

    cur.close()
    conn.close()

    return jsonify(topics)

@app.route("/topics/<int:topic_id>", methods=["DELETE"])
def delete_topic(topic_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM topics WHERE id = %s", (topic_id,))
    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Topic deleted"}, 200

@app.route("/units/<int:unit_id>", methods=["DELETE"])
def delete_unit(unit_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM topics WHERE unit_id = %s", (unit_id,))
    cur.execute("DELETE FROM units WHERE id = %s", (unit_id,))
    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Unit deleted"}, 200

@app.route("/subjects/<int:subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM topics
        WHERE unit_id IN (
            SELECT id FROM units WHERE subject_id = %s
        )
    """, (subject_id,))

    cur.execute("DELETE FROM units WHERE subject_id = %s", (subject_id,))
    cur.execute("DELETE FROM subjects WHERE id = %s", (subject_id,))
    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Subject deleted"}, 200

@app.route("/units/<int:unit_id>/notes", methods=["GET"])
def get_unit_notes(unit_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, content FROM notes WHERE unit_id = %s ORDER BY created_at DESC",
        (unit_id,)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [{"id": r[0], "content": r[1]} for r in rows]

@app.route("/units/<int:unit_id>/notes", methods=["POST"])
def add_unit_note(unit_id):
    data = request.json

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO notes (unit_id, content) VALUES (%s, %s) RETURNING id",
        (unit_id, data["content"])
    )

    note_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return {"id": note_id, "content": data["content"]}, 201

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_unit_note(note_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    conn.commit()

    cur.close()
    conn.close()
    return {"message": "Note deleted"}

@app.route("/units/<int:unit_id>/progress", methods=["GET"])
def get_unit_progress(unit_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE status = 'Completed') AS completed,
            COUNT(*) AS total
        FROM topics
        WHERE unit_id = %s
    """, (unit_id,))

    completed, total = cur.fetchone()
    cur.close()
    conn.close()

    if total == 0:
        return {"progress": 0}

    progress = round((completed / total) * 100)
    return {"progress": progress}

@app.route("/subjects/<int:subject_id>/progress", methods=["GET"])
def get_subject_progress(subject_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE t.status = 'Completed') AS completed,
            COUNT(*) AS total
        FROM topics t
        JOIN units u ON t.unit_id = u.id
        WHERE u.subject_id = %s
    """, (subject_id,))

    completed, total = cur.fetchone()
    cur.close()
    conn.close()

    if total == 0:
        return {"progress": 0}

    progress = round((completed / total) * 100)
    return {"progress": progress}


print("ROUTES REGISTERED")

if __name__ == "__main__":
    print("STARTING FLASK SERVER")
    app.run(host="127.0.0.1", port=5000, debug=True)
