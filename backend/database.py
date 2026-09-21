import sqlite3  ## SQLite3 database connection


##Inicializa la conexión a la base de datos SQLite3
def init_db():
    conn = sqlite3.connect('unicourse.db') ## Crea una conexión a la base de datos SQLite3 llamada 'unicourse.db'
    cursor = conn.cursor() ## Crea un cursor para ejecutar consultas SQL
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    professor_id INTEGER,

    FOREIGN KEY (professor_id) REFERENCES professors(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    user_id INTEGER,
    course_id INTEGER,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES posts(id),

    UNIQUE (user_id, post_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES posts(id)
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO users (username, email)
    VALUES 
    ('Frank', 'frank.flores.g@uni.pe'),
    ('Harold','harold.eustaquio.h@uni.pe')

    """)

    cursor.execute("""
    INSERT OR IGNORE INTO professors (name, email)
    VALUES
    ('Benitez', 'carlos.benitez.c@uni.pe'),
    ('Llamocca','luis.llamocca.c@uni.pe')
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO courses (name, code, professor_id)
    VALUES
    ('Algoritmos 1','ICM01',1),
    ('Física 1','BFI01',2)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO posts (content, user_id, course_id)
    VALUES
    ('El profe es tranca', 1,1),
    ('El profe es pésimo',2,2)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO likes (user_id, post_id)
    VALUES 
    (1, 1),
    (2, 1),
    (1, 2)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO comments (content, user_id, post_id)
    VALUES
    ('Gracias por advertir',1,1),
    ('Que malo...',2,2)
    """)

    cursor.execute("""
    SELECT
    users.username,
    posts.content,
    courses.name,
    professors.name

    FROM posts
    JOIN users
    ON posts.user_id = users.id
    JOIN courses 
    ON  posts.course_id = courses.id
    JOIN professors
    ON courses.professor_id = professors.id
    """)

    results = cursor.fetchall()

    for row in results:
        print(row)

    conn.commit()
    conn.close()


init_db()