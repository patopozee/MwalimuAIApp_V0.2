from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

# Initialize Gemini client
client = genai.Client()


def ask_mwalimu(question, student, messages):
    """
    Takes the current question, student profile,
    and previous conversation history.
    """

    # Build conversation history
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
    - Use the student's preferred language.
    - Adapt to the student's learning style.
    - Be encouraging and patient.
    - Give examples and practice questions.
    - Remember previous parts of the conversation.

    Give a clear educational response.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return (
            "Sorry, Mwalimu AI encountered an error. "
            f"Details: {e}"
        )