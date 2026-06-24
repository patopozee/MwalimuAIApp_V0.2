import os
from dotenv import load_dotenv
from openai import OpenAI

# Load keys from the local .env file
load_dotenv()

# Initialize unified OpenRouter gateway client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)


def ask_mwalimu(question, student, messages):
    """
    Dispatches prompts straight to OpenRouter's auto-balancing free routing pool.
    This automatically switches models to keep your classroom online 24/7.
    """

    # Build conversation history context string
    history = ""
    for msg in messages:
        if msg["role"] == "student":
            history += f"Student: {msg['content']}\n"
        else:
            history += f"Mwalimu AI: {msg['content']}\n"

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

    Give a clear educational response.
    """

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app", 
                "X-Title": "Mwalimu AI App",
            },
            # Uses OpenRouter's automatic free pool to instantly bypass model removals
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e).lower()
        if "429" in error_msg or "rate" in error_msg:
            return (
                "Pole! 😭 My classroom has a small queue. "
                "Please wait 5 seconds and click ask again!"
            )
        return f"Mwalimu AI hit a routing issue. Details: {e}"


def generate_quiz(topic, student):
    """
    Generate a quiz using the automatic free routing engine pool.
    """

    prompt = f"""
    You are Mwalimu AI, a Kenyan teacher.

    Student Profile:
    Name: {student["name"]}
    Grade: {student["grade"]}
    Age: {student["age"]}
    Learning Style: {student["learning_style"]}
    Language: {student["language"]}

    Create a 5-question multiple-choice quiz about:
    {topic}

    Rules:
    - Match the student's grade level.
    - Include options A, B, C, and D.
    - Mark the correct answer after each question.
    - Keep questions age-appropriate.
    """

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app",
                "X-Title": "Mwalimu AI App Quiz",
            },
            # Uses OpenRouter's automatic free pool for quiz construction
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as error:
        return "Quiz generation failed due to high server traffic. Please try again in a few moments."