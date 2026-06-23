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
    Dispatches prompts straight to OpenRouter's high-availability
    free routing pool to bypass all individual model rate limits.
    Takes the current question, student profile,
    and previous conversation history.
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
        # Call the auto-load-balanced free model router
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app", 
                "X-Title": "Mwalimu AI App",
            },
            # TO THIS SPECIFIC RELIABLE MODEL:
            model="meta-llama/llama-3-8b-instruct:free",
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