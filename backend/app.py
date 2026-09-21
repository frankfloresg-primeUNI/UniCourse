from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('unicourse.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()  
    cursor = conn.execute("""    -- cursor contiene el resultado de la consulta
    SELECT 
        posts.id,
        posts.content,
        users.username,
        courses.name AS course,
        professors.name AS professor
    FROM posts
    JOIN users
        ON posts.user_id = users.id
    JOIN courses
        ON posts.course_id = courses.id
    JOIN professors
        ON courses.professor_id = professors.id
    """)

    posts = cursor.fetchall()  #Dame todas las filas que produjo select
    posts_list = [dict(row) for row in posts]
    conn.close()
    return jsonify(posts_list)   #La convierte en una respuesta JSON
 

@app.route('/api/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    cursor = conn.execute("""
    SELECT 
    courses.id,
    courses.name,
    courses.code,
    professors.name AS professor
    FROM courses 
    JOIN professors
    ON courses.professor_id = professors.id
    """)
    courses = cursor.fetchall()
    courses_list = [dict(row) for row in courses]
    conn.close()
    return jsonify(courses_list)

@app.route('/api/professors',methods=['GET'])
def get_professors():
    conn = get_db_connection()
    cursor = conn.execute("""
    SELECT
    professors.id,
    professors.name,
    professors.email
    FROM professors
    """)
    professors = cursor.fetchall()
    list_professors = [dict(row) for row in professors]
    conn.close()
    return jsonify(list_professors)

@app.route('/api/posts',methods=['POST'])
def create_post():
    data = request.get_json()
    content = data['content']
    user_id = data['user_id']
    course_id = data['course_id']

    conn = get_db_connection()

    cursor = conn.execute("""
    INSERT INTO posts (content, user_id, course_id)
    VALUES (?, ?, ?)
    """, (content, user_id, course_id))
    conn.commit()
    return jsonify({
        "message" : "Post creado correctamente"
    }), 201

if __name__ =='__main__':
    app.run(debug=True)  #Permite que Flas recargue auto si modifico algo y muestra errores detallados