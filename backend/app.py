from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('unicourse.db')
    conn.row_factory = sqlite3.Row   #Accedes a las columas por nombre
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
        professors.name AS professor,

        COUNT(DISTINCT likes.id) AS likes_count,
        COUNT(DISTINCT comments.id) AS comments_count
    FROM posts

    JOIN users
        ON posts.user_id = users.id
    JOIN courses
        ON posts.course_id = courses.id
    JOIN professors
        ON courses.professor_id = professors.id
    
    LEFT JOIN likes
        ON posts.id = likes.post_id
    LEFT JOIN comments
        ON posts.id = comments.post_id
    
    GROUP BY
        posts.id,
        posts.content,
        users.username,
        courses.name,
        professors.name
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

@app.route('/api/likes', methods=['POST'])
def create_like():
    conn = get_db_connection()
    data = request.get_json()
    user_id=data['user_id']
    post_id=data['post_id']
    
    try:
        cursor = conn.execute("""
        INSERT INTO likes (user_id, post_id)
        VALUES(?, ?)
        """, (user_id, post_id))
        conn.commit()
        return jsonify({
            'message':'Like creado correctamente'
        }), 201
    except sqlite3.IntegrityError:
        conn.rollback()
        return jsonify({
            'error':'El usuario ya dio like a este post'
        }), 409

@app.route('/api/comments', methods=['POST'])
def create_comment():
    data=request.get_json()
    content=data.get('content')
    user_id=data.get('user_id')
    post_id=data.get('post_id')

    #Validamos datos
    if not content or not user_id or not post_id:
        return jsonify({
            'error': 'Faltan datos'
        }), 400

    conn=get_db_connection()

    try: 
        cursor=conn.execute("""
        INSERT INTO comments (content, user_id, post_id)
        VALUES(?, ?, ?)
        """, (content, user_id, post_id))
        conn.commit()

    except sqlite3.IntegrityError:
        conn.rollback()

        return jsonify({
            'error':'El post o usuario no existe'
        }), 400

    finally:
        conn.close()



if __name__ =='__main__':
    app.run(debug=True)  #Permite que Flas recargue auto si modifico algo y muestra errores detallados