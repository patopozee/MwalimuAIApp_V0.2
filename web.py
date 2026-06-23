import streamlit as st
from app import ask_mwalimu

# Page Setup
st.set_page_config(page_title="Mwalimu AI App", page_icon="📚", layout="centered")

st.title("📚 Mwalimu AI App")
st.write(
    "Welcome! I am your friendly Kenyan AI teacher. "
    "Create your profile and ask me any school question."
)

# Sidebar UI
st.sidebar.title("👨‍🎓 Student Profile")
name = st.sidebar.text_input("Student Name")
grade = st.sidebar.selectbox(
    "Grade",
    ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Form 1", "Form 2", "Form 3", "Form 4"]
)
age = st.sidebar.number_input("Age", min_value=5, max_value=25, value=10)
favorite_subject = st.sidebar.text_input("Favorite Subject")
weak_subject = st.sidebar.text_input("Weak Subject")
learning_style = st.sidebar.selectbox("Learning Style", ["Visual", "Practical", "Reading/Writing", "Interactive", "Story-based"])
language = st.sidebar.selectbox("Preferred Language", ["English", "Kiswahili", "Sheng"])

student = {
    "name": name,
    "grade": grade,
    "age": age,
    "favorite_subject": favorite_subject,
    "weak_subject": weak_subject,
    "learning_style": learning_style,
    "language": language,
}

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display Conversation
for message in st.session_state.messages:
    if message["role"] == "student":
        st.write("### 👨‍🎓 You")
        st.write(message["content"])
    elif message["role"] == "assistant":
        st.write("### 👨‍🏫 Mwalimu AI")
        st.write(message["content"])
    st.markdown("---")

# Mobile-Safe Input
question = st.chat_input("✏️ Ask your question")
submit_button = True if question is not None else False

if submit_button:
    if not name.strip():
        st.warning("⚠️ Please enter your name in the Student Profile sidebar.")
    elif not question or not question.strip():
        st.warning("⚠️ Please type a question.")
    else:
        st.session_state.messages.append({"role": "student", "content": question})

        with st.spinner("🧠 Mwalimu AI is thinking..."):
            answer = ask_mwalimu(question, student, st.session_state.messages)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

st.markdown("---")
st.caption("📚 Mwalimu AI Version 0.4 | Gateway Hybrid Engine (Gemini + Llama 3.3)")