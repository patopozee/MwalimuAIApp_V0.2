import sqlite3

DATABASE_NAME = "mwalimu.db"


def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        grade TEXT,
        age INTEGER,
        favorite_subject TEXT,
        weak_subject TEXT,
        learning_style TEXT,
        language TEXT
    )
    """)

    # Added explicit grade and age columns straight to the progress table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        student_grade TEXT,
        student_age INTEGER,
        activity_type TEXT,
        topic TEXT,
        score INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_student(student):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (
        name, grade, age, favorite_subject, weak_subject, learning_style, language
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        student["name"],
        student["grade"],
        student["age"],
        student["favorite_subject"],
        student["weak_subject"],
        student["learning_style"],
        student["language"]
    ))

    conn.commit()
    conn.close()


def save_activity(student_name, student_grade, student_age, activity_type, topic, score=0):
    """Saves records with full distinct profile context details."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO progress
    (
        student_name,
        student_grade,
        student_age,
        activity_type,
        topic,
        score
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        student_name,
        student_grade,
        int(student_age),
        activity_type,
        topic,
        score
    ))

    conn.commit()
    conn.close()


def get_student_stats(student_name, grade, age):
    """Queries directly from progress using the explicit target metrics."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # 1. Count how many general questions the student has asked
    cursor.execute("""
    SELECT COUNT(id) FROM progress 
    WHERE student_name=? AND student_grade=? AND student_age=?
    AND activity_type='question'
    """, (student_name, grade, age))
    questions = cursor.fetchone()[0] or 0

    # 2. Count how many total quizzes have been generated
    cursor.execute("""
    SELECT COUNT(id) FROM progress 
    WHERE student_name=? AND student_grade=? AND student_age=?
    AND activity_type='quiz'
    """, (student_name, grade, age))
    quizzes = cursor.fetchone()[0] or 0

    # 3. Calculate the average using only final submitted quiz scores
    cursor.execute("""
    SELECT AVG(score) FROM progress 
    WHERE student_name=? AND student_grade=? AND student_age=?
    AND activity_type='quiz_score'
    """, (student_name, grade, age))
    average_score = cursor.fetchone()[0]

    conn.close()

    return {
        "questions": questions,
        "quizzes": quizzes,
        "average_score": round(average_score or 0, 1)
    }

def get_student_quiz_history(name, grade, age):
    """Fetches chronological quiz scores for a student to plot on a graph."""
    conn = sqlite3.connect(DATABASE_NAME) # Using your global DATABASE_NAME variable
    cursor = conn.cursor()
    
    # Updated to match your exact schema table 'progress' and its correct columns
    cursor.execute("""
        SELECT score 
        FROM progress 
        WHERE student_name = ? AND student_grade = ? AND student_age = ? AND activity_type = 'quiz_score'
        ORDER BY created_at ASC
    """, (name, grade, age))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Return a flat list of scores, e.g., [70, 80, 100]
    return [row[0] for row in rows]