print("APP FILE LOADED")

from flask import Flask, jsonify
from flask_cors import CORS
from db import get_connection
from flask import request



app = Flask(__name__)
CORS(app, supports_credentials=True)


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
        SET status = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
        """,
        (new_status, topic_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Status updated"})

@app.route("/subjects", methods=["GET"])
def get_subjects():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM subjects ORDER BY id;")
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
def add_subject():
    data = request.get_json()
    name = data.get("name")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO subjects (name) VALUES (%s) RETURNING id;", (name,))
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
        "SELECT id, content FROM unit_notes WHERE unit_id = %s ORDER BY created_at DESC",
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
        "INSERT INTO unit_notes (unit_id, content) VALUES (%s, %s) RETURNING id",
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

    cur.execute("DELETE FROM unit_notes WHERE id = %s", (note_id,))
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
