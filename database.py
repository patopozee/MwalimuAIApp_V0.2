import sqlite3

DATABASE_NAME = "mwalimu.db"

def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # 1. Students Profile Schema
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
    # 2. Main Analytics & Activity Progress Schema
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
    INSERT INTO students (
        name, grade, age, favorite_subject, weak_subject, learning_style, language
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
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
    """Saves records with full distinct profile context details into the progress table."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO progress (
        student_name, student_grade, student_age, activity_type, topic, score
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (student_name, student_grade, student_age, activity_type, topic, score))
    conn.commit()
    conn.close()

# ==================== UPDATED QUANTITATIVE QUERIES ====================

def get_student_stats(student_name, student_grade, student_age):
    """Calculates live aggregated metric counters using name, grade, and age filters together."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Questions counter - FIXED: added full profile filter matches
    cursor.execute("""
        SELECT COUNT(*) FROM progress 
        WHERE student_name = ? AND student_grade = ? AND student_age = ? AND activity_type = 'question'
    """, (student_name, student_grade, student_age))
    questions = cursor.fetchone()[0]
    
    # Quizzes counter - FIXED: added full profile filter matches
    cursor.execute("""
        SELECT COUNT(*) FROM progress 
        WHERE student_name = ? AND student_grade = ? AND student_age = ? AND activity_type = 'quiz'
    """, (student_name, student_grade, student_age))
    quizzes = cursor.fetchone()[0]
    
    # Average score - FIXED: added full profile filter matches
    cursor.execute("""
        SELECT AVG(score) FROM progress 
        WHERE student_name = ? AND student_grade = ? AND student_age = ? AND activity_type = 'quiz_score'
    """, (student_name, student_grade, student_age))
    avg_score = cursor.fetchone()[0]
    avg_score = round(avg_score) if avg_score else 0
    
    conn.close()
    return {
        "questions": questions,
        "quizzes": quizzes,
        "average_score": avg_score
    }

def get_student_quiz_history(student_name, student_grade, student_age):
    """Fetches historical quiz scores scoped explicitly to a single unique student profile layout."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # FIXED: query now checks for full distinct identity criteria
    cursor.execute("""
        SELECT score FROM progress
        WHERE student_name = ? AND student_grade = ? AND student_age = ? AND activity_type = 'quiz_score'
        ORDER BY created_at ASC
    """, (student_name, student_grade, student_age))
    scores = [row[0] for row in cursor.fetchall()]
    conn.close()
    return scores

def get_next_difficulty(student_name, student_grade, student_age, topic):
    """Dynamically scales assignment difficulty parameters based on performance details of this explicit student."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # FIXED: tracking performance limits across matching grade/age profiles
    cursor.execute("""
        SELECT score FROM progress
        WHERE student_name = ? AND student_grade = ? AND student_age = ? AND topic = ? AND activity_type = 'quiz_score'
        ORDER BY created_at DESC LIMIT 3
    """, (student_name, student_grade, student_age, topic))
    scores = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not scores:
        return "Medium"
    avg = sum(scores) / len(scores)
    if avg >= 80:
        return "Hard"
    elif avg < 50:
        return "Easy"
    return "Medium"

def get_student_learning_analysis(student_name, student_grade, student_age):
    """Provides focus topic analytics isolated by name, grade, and age checks."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # FIXED: Aggregates only rows belonging to this precise child version template
    cursor.execute("""
        SELECT topic, AVG(score) FROM progress
        WHERE student_name = ? AND student_grade = ? AND student_age = ? AND activity_type = 'quiz_score'
        GROUP BY topic
    """, (student_name, student_grade, student_age))
    topic_averages = cursor.fetchall()
    conn.close()
    
    weak_topics = [topic for topic, avg in topic_averages if avg < 70]
    strong_topics = [topic for topic, avg in topic_averages if avg >= 80]
    
    all_scores = [avg for topic, avg in topic_averages]
    overall_avg = sum(all_scores) / len(all_scores) if all_scores else 0
    if overall_avg < 50:
        current_level = "Easy"
    elif overall_avg < 80:
        current_level = "Medium"
    else:
        current_level = "Hard"
        
    return {
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "current_level": current_level
    }

# ==================== UPDATED CHAT ROUTINES ====================

def get_chat_history(student_name: str, grade: str, age: int):
    """Retrieves previous chat logs sorted chronologically matching the user's explicit profile combo."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # FIXED: Added student_grade and student_age parameter rules to prevent cross-chat leak
    cursor.execute("""
        SELECT activity_type, topic FROM progress
        WHERE student_name = ? AND student_grade = ? AND student_age = ? 
        AND (activity_type = 'student' OR activity_type = 'assistant')
        ORDER BY id ASC
    """, (student_name, grade, age))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": "user" if r[0] == "student" else "assistant", "content": r[1]} for r in rows]

def save_chat_message(student_name: str, grade: str, age: int, role: str, message: str):
    """Explicitly records messages with multi-dimensional profile context details."""
    activity = "student" if role in ["user", "student"] else "assistant"
    save_activity(
        student_name=student_name,
        student_grade=grade,
        student_age=age,
        activity_type=activity,
        topic=message,
        score=0
    )

def clear_student_chat_history(student_name: str, grade: str, age: int):
    """Deletes chat data ONLY for this matching profile segment configuration."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # FIXED: Added strict segment matching so clearing one user doesn't drop conversations of name clones
    cursor.execute("""
        DELETE FROM progress
        WHERE student_name = ? AND student_grade = ? AND student_age = ?
        AND (activity_type = 'student' OR activity_type = 'assistant')
    """, (student_name, grade, age))
    conn.commit()
    conn.close()