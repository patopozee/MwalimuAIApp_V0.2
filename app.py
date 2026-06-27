import os
import json
import random
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load keys from local .env file if it exists
load_dotenv()

# 2. Unified fallback: check system environment variables first, then fallback to Streamlit secrets
api_key = os.environ.get("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")

# 3. Initialize unified OpenRouter gateway client safely
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def ask_mwalimu(question, student, messages, adaptive_context=""):
    """
    Dispatches prompts to a specific high-quality free model on OpenRouter.
    """
    # Build conversation history context string safely
    history = ""
    for msg in messages:
        # Check if msg is a dictionary and has the required keys safely
        if isinstance(msg, dict) and "role" in msg and "content" in msg:
            role = str(msg["role"]).lower()
            content = msg["content"]
            
            # Universal check matching 'student', 'user', 'assistant' or 'mwalimu'
            if role in ["student", "user"]:
                history += f"Student: {content}\n"
            elif role in ["assistant", "mwalimu"]:
                history += f"Mwalimu AI: {content}\n"

    # ==========================
    # PROMPT TEMPLATE STRINGS CONTINUE BELOW...

    prompt = f"""
    You are Mwalimu AI App, a friendly Kenyan teacher.

    ==========================
    STUDENT PROFILE
    ==========================
    Name: {student["name"]}
    Grade: {student["grade"]}
    Age: {student["age"]}
    Favorite Subject: {student["favorite_subject"]}
    Weak Subject: {student["weak_subject"]}
    Learning Style: {student["learning_style"]}
    Language: {student["language"]}

    ==========================
    ADAPTIVE LEARNING ANALYSIS
    ==========================
    {adaptive_context}

    ==========================
    PREVIOUS CONVERSATION
    ==========================
    {history}

    ==========================
    CURRENT QUESTION
    ==========================
    Student:
    {question}

    ==========================
    TEACHING RULES
    ==========================
    - Explain according to the student's age and grade.
    - Use the student's preferred language (English, Kiswahili, or Sheng).
    - Adapt directly to the student's learning style.
    - Be encouraging and patient.
    - Give examples and short practice questions.
    - Remember previous parts of the conversation.
    - ADAPTIVE RULE: If the question is about a topic listed in their 'Weak Topics', break it down into much simpler foundational steps.
    - ADAPTIVE RULE: If their 'Current Level' is 'Hard', challenge them with an analytical thinking follow-up question.

    Give a clear educational response.
    """
    
    # ... your existing OpenRouter client request execution lines continue here ...

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app",
                "X-Title": "Mwalimu AI App",
            },
            # Explicitly points to the zero-cost tier string endpoint
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]  # Changed 'student' to 'user' for OpenAI specification compliance
        )
        return response.choices[0].message.content

    except Exception as e:
            error_msg = str(e).lower()
            # Print the exact error to your terminal console so you can debug it locally
            print(f"OpenRouter API Error: {e}")
            
            if "429" in error_msg or "rate" in error_msg:
                return "Pole! 🇰🇪 My classroom has a small queue. Please wait 5 seconds and click ask again!"
            
            # Fallback return so the app never hangs silently
            return f"Mwalimu encountered an error while thinking: {e}. Please try again!"


def generate_quiz(topic, student, difficulty="Easy"):
    """Generates structured JSON quiz variations based on adaptive parameters."""

    # Define adaptive difficulty constraints directly for the model context
    difficulty_rules = {
        "Easy": "Use very simple language. Focus on one core concept per question. No trick questions.",
        "Medium": "Slightly more challenging. Require two-step thinking. Use localized practical examples.",
        "Hard": "Incorporate complex application questions, critical thinking scenarios, and higher-order reasoning."
    }
    
    prompt = f"""
    You are Mwalimu AI, a friendly Kenyan teacher personalization model.
    # Change this line inside your prompt string in app.py:
    Generate a 5-question multiple-choice quiz about '{topic}' for a student in {student['grade']} ({student['age']} years old).
    
    Target Difficulty Level: {difficulty}
    Difficulty Context Rules: {difficulty_rules.get(difficulty, "")}
    Preferred Learning Style: {student['learning_style']}
    Preferred Delivery Language: {student['language']}
    
    Return your response strictly as a valid JSON array of objects structured exactly like this:
    [
      {{
        "question": "Question text here",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "The exact correct option string matching one of the options"
      }}
    ]
    """

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app",
                "X-Title": "Mwalimu AI App Quiz",
            },
            # Match the same exact free production tier model
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        quiz_text = response.choices[0].message.content

        if quiz_text is None:
            print("No content returned from model")
            return []

        # --- RECOVERY MECHANISM FOR UNWANTED MARKDOWN ---
        quiz_text = quiz_text.replace("```json", "").replace("```", "").strip()

        try:
            quiz_data = json.loads(quiz_text)
            for question in quiz_data:
                if "options" in question and isinstance(question["options"], list):
                    random.shuffle(question["options"])  
            return quiz_data                          
        except json.JSONDecodeError:
            print("Invalid JSON returned by Model:")
            print(quiz_text)
            return []

    except Exception as e:
        print(f"Error calling OpenRouter API: {e}")
        return []

def generate_study_plan(student, stats):
    """
    Generates a daily personalized study plan based on student profile and quiz history metrics.
    """
    prompt = f"""
    You are Mwalimu AI, an intelligent Kenyan teacher.
    Create a personalized DAILY STUDY PLAN.

    Student Profile
    Name: {student.get("name", "Student")}
    Grade: {student.get("grade", "N/A")}
    Age: {student.get("age", "N/A")}
    Favorite Subject: {student.get("favorite_subject", "N/A")}
    Weak Subject: {student.get("weak_subject", "N/A")}
    Learning Style: {student.get("learning_style", "General")}
    Preferred Language: {student.get("language", "English")}

    Student Statistics
    Questions Asked: {stats.get("questions", 0)}
    Quizzes Taken: {stats.get("quizzes", 0)}
    Average Score: {stats.get("average_score", 0)}%

    Requirements:
    Create a highly structured study plan for today. Include:
    1. Study Goal (focused on improving their weak subject while keeping them engaged with their favorite subject)
    2. Subjects to study
    3. Specific Topics
    4. Time allocation (e.g., 08:00-08:20)
    5. Practical practice activities aligned with their preferred learning style ({student.get("learning_style", "General")})
    6. Revision items
    7. A dynamic custom Quiz recommendation
    8. A warm, motivational message using encouraging Kenyan teacher phrasing (e.g., "Kazi safi", "Keep pushing").

    Format the plan beautifully with clean markdown spacing, bold subtitles, and bullet points.
    """

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app",
                "X-Title": "Mwalimu AI Study Plan",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenRouter Study Plan Error: {e}")
        return f"Mwalimu encountered an issue preparing your roadmap: {e}. Please click generate again!"