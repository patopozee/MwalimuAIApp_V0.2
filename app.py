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
        error_msg = str(e).lower()
        
        # Catch 503 Overloaded, high demand, or resource exhaustion spikes gracefully
        if "503" in error_msg or "demand" in error_msg or "resource_exhausted" in error_msg:
            return (
                "Pole! 😭 My classroom is currently very crowded with other students. "
                "Please wait just a few seconds and try asking your question again!"
            )
        
        # General fallback if another unique error occurs
        return (
            "Sorry, Mwalimu AI encountered an unexpected error. "
            f"Details: {e}"
        )