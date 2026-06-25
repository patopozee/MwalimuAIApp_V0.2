import os
import json
import random
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
    Dispatches prompts to a specific high-quality free model on OpenRouter.
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
            # Explicitly points to the zero-cost tier string endpoint
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
    Generate a quiz using a specific free model variant.
    Handles accidental markdown codeblock wrappers safely.
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

    IMPORTANT:
    Return ONLY a raw valid JSON array.
    Do not include explanations outside the JSON.
    Do not include markdown packaging.
    Do not include formatting code blocks.

    Use this exact structure format:
    [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Option A"
        }}
    ]

    Rules:
    - Generate exactly 5 questions.
    - Match the student's grade level.
    - Keep questions age-appropriate.
    - Use the student's preferred language.
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