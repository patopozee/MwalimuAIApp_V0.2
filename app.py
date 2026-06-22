import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env file
load_dotenv()

# Initialize the modern client (automatically picks up GEMINI_API_KEY)
client = genai.Client()


def ask_mwalimu(question, student):
    """Takes a student question and profile, returning a personalized,

    friendly Kenyan teacher response.
    """

    prompt = f"""
    You are Mwalimu AI App, a friendly Kenyan teacher. 
    
    Student Profile:
    Name: {student["name"]}
    Grade: {student["grade"]}
    Age: {student["age"]}
    Favorite Subject: {student["favorite_subject"]}
    Weak Subject: {student["weak_subject"]}
    Learning Style: {student["learning_style"]}
    Language: {student["language"]}
    
    Teaching Rules:
    - Explain concepts simply and adjust the explanation to the student's grade and age.
    - Give practical examples matching their learning style.
    - Encourage and support the student.
    - Use the student's preferred language (e.g., English, Kiswahili, or Sheng).
    
    Student question:
    {question}

    RESPONSE FORMAT

    Give a clear, age-appropriate answer.
    Use headings and bullet points when helpful.
    End with a short practice question or challenge.
    """

    # Using the recommended, up-to-date model for general text tasks
    try:
        # Send the prompt to Gemini AI
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        # Return the AI response
        return response.text

    except Exception as e:
        # Return a friendly error message instead of crashing the app
        return f"Sorry, Mwalimu AI encountered an error: {e}"