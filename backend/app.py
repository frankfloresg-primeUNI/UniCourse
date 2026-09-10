from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "courses.db"


def init_db():
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            professor TEXT NOT NULL,
            rating REAL NOT NULL,
            description TEXT NOT NULL,
            advice TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM courses")

    if cursor.fetchone()[0] == 0:

        courses = [
            (
                "Programación I",
                "Juan Pérez",
                4.5,
                "Curso donde aprendes fundamentos de programación.",
                "Practica programación todas las semanas."
            ),
            (
                "Cálculo II",
                "María López",
                4.2,
                "Curso enfocado en integrales y aplicaciones.",
                "Haz ejercicios constantemente."
            ),
            (
                "Circuitos Eléctricos",
                "Carlos Torres",
                3.8,
                "Análisis de circuitos eléctricos y sus componentes.",
                "Practica problemas y entiende los conceptos."
            )
        ]

        cursor.executemany("""
            INSERT INTO courses
            (name, professor, rating, description, advice)
            VALUES (?, ?, ?, ?, ?)
        """, courses)

    conn.commit()
    conn.close()


@app.route("/api/courses")
def get_courses():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses")

    courses = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify(courses)


@app.route("/api/courses/<int:course_id>")
def get_course(course_id):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM courses WHERE id = ?",
        (course_id,)
    )

    course = cursor.fetchone()

    conn.close()

    if course is None:
        return jsonify({"error": "Curso no encontrado"}), 404

    return jsonify(dict(course))


from flask import request
@app.route("/api/courses", methods=["POST"])
def create_course():

    data = request.json

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO courses
        (name, professor, rating, description, advice)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["professor"],
        data["rating"],
        data["description"],
        data["advice"]
    ))

    conn.commit()

    new_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "message": "Curso creado",
        "id": new_id
    }), 201


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)

@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):

    data = request.json

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE courses
        SET name = ?,
            professor = ?,
            rating = ?,
            description = ?,
            advice = ?
        WHERE id = ?
    """, (
        data["name"],
        data["professor"],
        data["rating"],
        data["description"],
        data["advice"],
        course_id
    ))

    conn.commit()

    conn.close()

    return jsonify({
        "message": "Curso actualizado"
    })

@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM courses WHERE id = ?",
        (course_id,)
    )

    conn.commit()

    conn.close()

    return jsonify({
        "message": "Curso eliminado"
    })