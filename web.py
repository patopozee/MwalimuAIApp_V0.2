import streamlit as st
from app import ask_mwalimu


# -----------------------------
# App Title
# -----------------------------
st.title("📚 Mwalimu AI App")
st.write(
    "Welcome! I am your friendly Kenyan AI teacher. "
    "Create your profile and ask me any school question."
)


# -----------------------------
# Student Profile Sidebar
# -----------------------------
st.sidebar.title("👨‍🎓 Student Profile")

name = st.sidebar.text_input(
    "Student Name"
)

grade = st.sidebar.selectbox(
    "Grade",
    [
        "Grade 1",
        "Grade 2",
        "Grade 3",
        "Grade 4",
        "Grade 5",
        "Grade 6",
        "Grade 7",
        "Grade 8",
        "Form 1",
        "Form 2",
        "Form 3",
        "Form 4"
    ]
)

age = st.sidebar.number_input(
    "Age",
    min_value=5,
    max_value=25,
    value=10
)

favorite_subject = st.sidebar.text_input(
    "Favorite Subject"
)

weak_subject = st.sidebar.text_input(
    "Weak Subject"
)

learning_style = st.sidebar.selectbox(
    "Learning Style",
    [
        "Visual",
        "Practical",
        "Reading/Writing",
        "Interactive",
        "Story-based"
    ]
)

language = st.sidebar.selectbox(
    "Preferred Language",
    [
        "English",
        "Kiswahili",
        "Sheng"
    ]
)


# -----------------------------
# Create Student Profile Object
# -----------------------------
student = {
    "name": name,
    "grade": grade,
    "age": age,
    "favorite_subject": favorite_subject,
    "weak_subject": weak_subject,
    "learning_style": learning_style,
    "language": language,
}


# -----------------------------
# Chat Memory Initialization
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Clear Chat Button
# -----------------------------
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# -----------------------------
# Display Conversation History
# -----------------------------
for message in st.session_state.messages:

    if message["role"] == "student":
        st.write("### 👨‍🎓 You")
        st.write(message["content"])

    elif message["role"] == "assistant":
        st.write("### 👨‍🏫 Mwalimu AI")
        st.write(message["content"])

    st.markdown("---")


# -----------------------------
# Mobile-Friendly Chat Input Element
# -----------------------------
question = st.chat_input("✏️ Ask your question")

# Set submit_button to True if the student enters a question
submit_button = True if question else False


# -----------------------------
# Process Student Question
# -----------------------------
if submit_button:

    # Validate student profile
    if not name.strip():
        st.warning(
            "⚠️ Please enter your name in the Student Profile."
        )

    elif not question or not question.strip():
        st.warning(
            "⚠️ Please type a question."
        )

    else:

        # Save student's message
        st.session_state.messages.append(
            {
                "role": "student",
                "content": question
            }
        )
        

        # Ask Gemini
        with st.spinner(
            "🧠 Mwalimu AI is thinking..."
        ):

            answer = ask_mwalimu(
                question,
                student,
                st.session_state.messages
            )


        # Save AI answer
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Refresh the page
        st.rerun()


# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.caption(
    "📚 Mwalimu AI Version 0.3 | Personalized AI Tutor powered by Gemini 2.5 Flash"
)