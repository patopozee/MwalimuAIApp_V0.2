from PIL import Image
import streamlit as st
import sqlite3
from app import ask_mwalimu, generate_quiz

# --- INITIALIZE SESSION STATE KEYS ---
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "quiz_raw_score" not in st.session_state:
    st.session_state.quiz_raw_score = 0

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quiz" not in st.session_state:
    st.session_state.quiz = None  


from database import (
    create_tables,
    save_activity,
    get_student_stats
)

# Build structure safely at startup
create_tables()

# Page Setup
st.set_page_config(
    page_title="Mwalimu AI App",
    page_icon="assets/logo112.png",
    layout="centered"
)

# --------------------------------------------------
# LOGO & UI SETTINGS
# --------------------------------------------------
sidebar_logo = Image.open("assets/logo211.png")
resized_logo = sidebar_logo.resize((150, 150)) # 📊 Increased resize bounds for crisper resolution
st.logo(resized_logo)

# Update this exact CSS block to break past default structural limits
# Update this exact CSS block to flatten all possible main page container paddings:
st.html("""
    <style>
        /* ========================================================
           NUCLEAR MAIN PAGE SPACER REMOVAL (COLLAPSE TOP ZONE)
           ======================================================== */
        
        /* 1. Kill the invisible top status/deploy bar element completely */
        [data-testid="stHeader"], header {
            display: none !important;
            height: 0px !important;
        }

        /* 2. Strip padding off the main viewport container layouts */
        [data-testid="stAppViewMainObj"], .stMain, [data-testid="stMain"] {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }

        /* 3. Strip padding off the inner content wrapper layout */
        [data-testid="stMainBlockContainer"], 
        [data-testid="stAppViewBlockContainer"], 
        .block-container {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }
        
        /* ========================================================
           SIDEBAR LOGO TUNING (PRESERVED FOR YOUR SIDEBAR)
           ======================================================== */
        [data-testid="stSidebarHeader"] img {
            max-height: 100px !important;  
            width: auto !important;
            min-height: 90px !important;   
        }
        [data-testid="stSidebarHeader"] [data-testid="stSidebarLogo"] {
            max-height: 100px !important;
            width: auto !important;
            display: flex !important;
            align-items: center !important;
        }
        [data-testid="stSidebarHeader"] {
            padding-top: 2.0rem !important;
            padding-bottom: 1.5rem !important;
            margin-bottom: 0.5rem !important;
        }
    </style>
""")

# --------------------------------------------------
# TITLE & INTRO (Pulled completely to the top)
# --------------------------------------------------
col1, col2 = st.columns([1, 5], vertical_alignment="center")

with col1:
    title_logo = Image.open("assets/logo112.png")
    # Using a clean div wrapper around the image to force zero margins
    st.html("<div style='margin-top: 0 !important; margin-bottom: 0 !important;'>")
    st.image(title_logo, width=100)
    st.html("</div>")

with col2:
    # Adding 'margin-top: 0 !important;' pulls the text completely up
    st.markdown(
        """
        <h1 style='margin-top: 0 !important; margin-bottom: 0 !important; padding: 0;'>
            Mwalimu AI App
        </h1>
        <h4 style='margin-top: 2px !important; margin-bottom: 0 !important; color: gray; font-weight: normal;'>
            Shaping Minds, Shifting Futures.
        </h4>
        """,
        unsafe_allow_html=True
    )

# A small controlled space before the welcome paragraph
st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

st.write(
    """
    Welcome! I am your friendly Kenyan AI teacher.
    Create your profile and ask me any school question.
    You can also generate quizzes tailored to your grade level,
    learning style, and preferred language.
    """
)

# Sidebar UI Elements
st.sidebar.title("Student Profile")

name = st.sidebar.text_input("Student Name")
grade = st.sidebar.selectbox(
    "Grade",
    [
        "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", 
        "Grade 7", "Grade 8", "Form 1", "Form 2", "Form 3", "Form 4"
    ]
)
age = st.sidebar.number_input(
    "Age", 
    min_value=5, 
    max_value=25, 
    value=10
)

favorite_subject = st.sidebar.text_input("Favorite Subject")
weak_subject = st.sidebar.text_input("Weak Subject")

learning_style = st.sidebar.selectbox(
    "Learning Style", 
    ["Visual", "Practical", "Reading/Writing", "Interactive", "Story-based"]
)

language = st.sidebar.selectbox(
    "Preferred Language",
    ["English", "Kiswahili", "Sheng"]
)

student = {
    "name": name,
    "grade": grade,
    "age": age,
    "favorite_subject": favorite_subject,
    "weak_subject": weak_subject,
    "learning_style": learning_style,
    "language": language,
}

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.quiz = None  
    st.session_state.quiz_submitted = False
    st.session_state.quiz_score = 0
    st.session_state.quiz_raw_score = 0
    st.rerun()

# --- PROGRESS DASHBOARD ---
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Progress Dashboard")

if name:
    stats = get_student_stats(name, grade, age)
    st.sidebar.metric("Questions Asked", stats["questions"])
    st.sidebar.metric("Quizzes Generated", stats["quizzes"])
    st.sidebar.metric("Average Score", f"{stats['average_score']}%")

# -----------------------------------
# QUIZ GENERATOR
# -----------------------------------
st.markdown("---")
st.subheader("📝 Quiz Generator")

quiz_topic = st.text_input(
    "Quiz Topic",
    placeholder="e.g. Fractions, Photosynthesis, Electricity"
)

if st.button("Generate Quiz"):
    if not quiz_topic.strip():
        st.warning("Please enter a quiz topic.")
    else:
        with st.spinner("Generating quiz..."):
            st.session_state.quiz = generate_quiz(quiz_topic, student)
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_raw_score = 0
            save_activity(name, grade, age, "quiz", quiz_topic, 0)
            st.rerun() 

# -----------------------------------
# DISPLAY INTERACTIVE QUIZ
# -----------------------------------
if st.session_state.quiz:
    st.markdown("### 📋 Generated Quiz")

    for i, question in enumerate(st.session_state.quiz):
        st.markdown(f"#### Question {i + 1}")
        st.radio(
            question["question"],
            question["options"],
            index=None,
            key=f"q{i}",
            disabled=st.session_state.quiz_submitted
        )

    if not st.session_state.quiz_submitted:
        if st.button("✅ Submit Quiz"):
            current_answers = [st.session_state.get(f"q{i}") for i in range(len(st.session_state.quiz))]
            
            if None in current_answers:
                st.warning("⚠️ Please answer all questions before submitting.")
            else:
                score = 0
                for i, q in enumerate(st.session_state.quiz):
                    if current_answers[i] == q["answer"]:
                        score += 1

                st.session_state.quiz_raw_score = score
                st.session_state.quiz_score = round((score / len(st.session_state.quiz)) * 100)
                st.session_state.quiz_submitted = True
                
                save_activity(name, grade, age, "quiz_score", quiz_topic, st.session_state.quiz_score)
                st.rerun()

    if st.session_state.quiz_submitted:
        raw_score = st.session_state.quiz_raw_score
        total_questions = len(st.session_state.quiz)
        percentage = st.session_state.quiz_score

        st.success(f"🎉 You scored {raw_score}/{total_questions} ({percentage}%)")
        st.markdown("## 📖 Answer Review")

        for i, q in enumerate(st.session_state.quiz):
            student_answer = st.session_state.get(f"q{i}")
            correct_answer = q["answer"]

            st.markdown(f"### Question {i+1}")
            st.write(q["question"])
            st.write(f"**Your Answer:** {student_answer}")

            if student_answer == correct_answer:
                st.success(f"✅ Correct Answer: {correct_answer}")
            else:
                st.error(f"❌ Correct Answer: {correct_answer}")
                
        if st.button("🔄 Clear Quiz Results"):
            st.session_state.quiz = None
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_raw_score = 0
            st.rerun()

# -----------------------------------
# DISPLAY CONVERSATION HISTORY
# -----------------------------------
st.markdown("---")
st.subheader("💬 Chat with Mwalimu")

for message in st.session_state.messages:
    if message["role"] == "student":
        st.write("### 👨‍🎓 You")
        st.write(message["content"])
    elif message["role"] == "assistant":
        st.write("### 👨‍🏫 Mwalimu AI App")
        st.write(message["content"])
    st.markdown("---")

# -----------------------------------
# MOBILE-SAFE INPUT
# -----------------------------------
question = st.chat_input("✏️ Ask your question")

if question:
    if not name.strip():
        st.warning("⚠️ Please enter your name in the Student Profile sidebar.")
    elif not question.strip():
        st.warning("⚠️ Please type a question.")
    else:
        st.session_state.messages.append({"role": "student", "content": question})

        with st.spinner("🧠 Mwalimu AI is thinking..."):
            answer = ask_mwalimu(question, student, st.session_state.messages)
            save_activity(name, grade, age, "question", question, 0)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

st.markdown("---")
st.caption("📚 Mwalimu AI App Version 0.4 | Gateway Hybrid Engine")