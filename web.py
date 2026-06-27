from PIL import Image
import streamlit as st
import sqlite3
import os
import base64  # Added for absolute bulletproof image injection
from app import ask_mwalimu, generate_quiz, generate_study_plan
from database import (
    create_tables,
    save_activity,
    get_student_stats,
    get_student_quiz_history,
    get_next_difficulty,
    get_student_learning_analysis,
    get_chat_history,
    save_chat_message,
    clear_student_chat_history  # Added for database purge support
)

# 1. RUN BASE DIRECTORY INITIALIZATIONS
create_tables()

# 2. DEFINE YOUR SIDEBAR FORM ARGUMENTS BEFORE ACCESSED
st.sidebar.header("Student Profile")

# 🔥 Automatically trims spaces and capitalizes the first letter of each word
raw_name = st.sidebar.text_input("Student Name", value=st.session_state.get("student_name") or "")
name = raw_name.strip().title() if raw_name else ""

grade = st.sidebar.selectbox("Grade", [
    "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6",
    "Grade 7", "Grade 8", "Form 1", "Form 2", "Form 3", "Form 4"
])
age = st.sidebar.number_input("Age", min_value=5, max_value=25, value=10)
favorite_subject = st.sidebar.text_input("Favorite Subject")
weak_subject = st.sidebar.text_input("Weak Subject")
learning_style = st.sidebar.selectbox("Learning Style", ["Visual", "Practical", "Reading/Writing", "Interactive", "Story-based"])
language = st.sidebar.selectbox("Preferred Language", ["English", "Kiswahili", "Sheng"])

# --- INITIALIZE SESSION STATE KEYS
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
if "study_plan" not in st.session_state:
    st.session_state.study_plan = None

# --- INITIALIZE STATE FROM DATABASE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if name and name.strip() != "":
    try:
        historical_chats = get_chat_history(name)
        if historical_chats:
            st.session_state.chat_history = historical_chats
    except Exception as db_err:
        print(f"Database restoration skipped on initialization: {db_err}")

# Page Setup
st.set_page_config(
    page_title="Mwalimu AI App",
    page_icon="assets/logo112.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- BASE64 SIDEBAR IMAGE INJECTOR
try:
    with open("assets/logo211.png", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    sidebar_bg_style = f"background-image: url('data:image/png;base64, {encoded_logo}') !important;"
except Exception:
    sidebar_bg_style = "" # Fallback if path changes

# GLOBAL UI & CSS LAYOUT SETTINGS
st.html(f"""
<style>
@media (min-width: 768px) {{
    [data-testid="stHeader"], header {{
        background-color: transparent !important;
        height: 3.5rem !important;
    }}
    [data-testid="stAppViewMainObj"], .stMain, [data-testid="stMain"] {{
        margin-top: -2.5rem !important;
        padding-top: 0rem !important;
    }}
    [data-testid="stMainBlockContainer"],
    [data-testid="stAppViewBlockContainer"],
    .block-container {{
        padding-top: 1.5rem !important;
        margin-top: 0rem !important;
    }}
}}
@media (max-width: 767px) {{
    [data-testid="stHeader"], header {{
        background-color: transparent !important;
        height: 3.5rem !important;
    }}
    [data-testid="stAppViewMainObj"], .stMain, [data-testid="stMain"] {{
        margin-top: 0rem !important;
        padding-top: 0.5rem !important;
    }}
}}
[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {{
    padding-top: 1rem !important;
}}
[data-testid="stHeader"] button {{
    background-color: rgba(255, 255, 255, 0.1) !important;
    border-radius: 4px !important;
    z-index: 999999 !important;
}}
[data-testid="stSidebarUserContent"] {{
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}}
[data-testid="stSidebarHeader"] {{
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    margin-bottom: 0rem !important;
    min-height: 80px !important;
    {sidebar_bg_style}
    background-size: contain !important;
    background-repeat: no-repeat !important;
    background-position: left center !important;
    margin-left: 55px !important;
}}
</style>
""")

# TITLE & INTRO
col1, col2 = st.columns([1, 5], vertical_alignment="center")
with col1:
    try:
        title_logo = Image.open("assets/logo112.png")
        st.html("<div style='margin-top: 0 !important; margin-bottom: 0 !important;'>")
        st.image(title_logo, width=100)
        st.html("</div>")
    except Exception:
        pass
with col2:
    st.markdown(
        """
        <h1 style='margin-top: 0 !important; margin-bottom: 0 !important; padding: 0;'>Mwalimu AI App</h1>
        <h4 style='margin-top: 2px !important; margin-bottom: 0 !important; color: gray; font-weight: normal;'>Shaping Minds, Shifting Futures.</h4>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
st.write("Welcome! I am your friendly Kenyan AI teacher. Create your profile and ask me any school question. You can also generate quizzes tailored to your grade level, learning style, and preferred language.")

# --- SIDEBAR PROFILE CONFIGURATION FOR DOWNSTREAM MODULES
st.sidebar.markdown("---")
st.sidebar.title("Active Profile")
if name:
    st.sidebar.info(f"👤 **Student:** {name} \n\n📋 **{grade}** | **Age:** {age}")
else:
    st.sidebar.warning("Please type your Student Name at the top of the sidebar.")

# Re-assemble student dictionary object safely for dependencies
student = {
    "name": name,
    "grade": grade,
    "age": age,
    "favorite_subject": favorite_subject,
    "weak_subject": weak_subject,
    "learning_style": learning_style,
    "language": language,
}

# 🔥 CLEAR CHAT BUTTON (Wipes both database entries and UI states simultaneously)
if st.sidebar.button("🗑️ Clear Chat"):
    if name and name.strip() != "":
        try:
            clear_student_chat_history(name)
        except Exception as e:
            print(f"Error clearing database chat logs: {e}")
            
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.quiz = None
    st.session_state.quiz_submitted = False
    st.session_state.quiz_score = 0
    st.session_state.quiz_raw_score = 0
    st.rerun()

# --- PROGRESS DASHBOARD
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Progress Dashboard")
if name:
    stats = get_student_stats(name, grade, age)
    st.sidebar.metric("Questions Asked", stats.get("questions", 0))
    st.sidebar.metric("Quizzes Generated", stats.get("quizzes", 0))
    st.sidebar.metric("Average Score", f"{stats.get('average_score', 0)}%")

    analysis = get_student_learning_analysis(name, grade, age)
    st.sidebar.markdown(f"**Learning Status:** `{analysis.get('current_level', 'Medium')}`")

    if analysis.get('weak_topics'):
        st.sidebar.markdown("**Needs Improvement:**")
        for t in analysis['weak_topics']:
            st.sidebar.caption(f"• {t}")

    if analysis.get('strong_topics'):
        st.sidebar.markdown("**Mastered Areas:**")
        for t in analysis['strong_topics']:
            st.sidebar.caption(f"• {t}")

    history_scores = get_student_quiz_history(name, grade, age)
    if len(history_scores) > 0:
        st.sidebar.markdown("**Performance Trend**")
        st.sidebar.line_chart(history_scores)

# -----------------------------------
# QUIZ GENERATOR
# -----------------------------------
st.markdown("---")
st.subheader("📝 Quiz Generator")

quiz_topic = st.text_input("Quiz Topic", placeholder="e.g. Fractions, Photosynthesis, Electricity")
if st.button("Generate Quiz"):
    if not quiz_topic.strip():
        st.warning("Please enter a quiz topic.")
    elif not name:
        st.warning("Please configure your Student Profile in the sidebar first!")
    else:
        with st.spinner("Generating quiz..."):
            target_diff = get_next_difficulty(name, grade, age, quiz_topic)
            st.session_state.quiz = generate_quiz(quiz_topic, student, target_diff)
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_raw_score = 0
            
            save_activity(
                student_name=name,
                student_grade=grade,
                student_age=age,
                activity_type="quiz",
                topic=quiz_topic,
                score=0
            )
            st.rerun()

if st.session_state.quiz:
    st.markdown("### Generated Quiz")
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
                
                save_activity(
                    student_name=name,
                    student_grade=grade,
                    student_age=age,
                    activity_type="quiz_score",
                    topic=quiz_topic,
                    score=st.session_state.quiz_score
                )
                st.rerun()

    if st.session_state.quiz_submitted:
        raw_score = st.session_state.quiz_raw_score
        total_questions = len(st.session_state.quiz)
        percentage = st.session_state.quiz_score
        st.success(f"🎉 You scored {raw_score}/{total_questions} ({percentage}%)")
        
        st.markdown("## Answer Review")
        for i, q in enumerate(st.session_state.quiz):
            student_answer = st.session_state.get(f"q{i}")
            correct_answer = q["answer"]
            st.markdown(f"### Question {i+1}")
            st.write(q["question"])
            st.write(f"**Your Answer:** {student_answer}")
            if student_answer == correct_answer:
                st.success(f"Correct Answer: {correct_answer}")
            else:
                st.error(f"Correct Answer: {correct_answer}")

        if st.button("🔄 Clear Quiz Results"):
            st.session_state.quiz = None
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_raw_score = 0
            st.rerun()

# --- AI STUDY PLAN SECTION ---
st.markdown("---")
st.subheader("📅 AI Personalized Study Plan")

if st.button("Generate Today's Study Plan"):
    if not name:
        st.warning("Please configure your Student Profile in the sidebar first!")
    else:
        with st.spinner("Creating your personalized study plan..."):
            stats = get_student_stats(name, grade, age)
            st.session_state.study_plan = generate_study_plan(student, stats)
            st.rerun()

if st.session_state.study_plan:
    st.info("💡 Tip: Follow the allocated time intervals for maximum focus today!")
    st.markdown(st.session_state.study_plan)
    if st.button("Clear Study Plan"):
        st.session_state.study_plan = None
        st.rerun()

# -----------------------------------
# DISPLAY CONVERSATION HISTORY
# -----------------------------------
st.markdown("---")
st.write("### 💬 Chat with Mwalimu")

for msg in st.session_state.chat_history:
    if msg["role"] in ["student", "user"]:
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

# -----------------------------------
# MOBILE-SAFE CHAT INPUT PIPELINE
# -----------------------------------
if user_question := st.chat_input("Ask your question"):
    if not name:
        st.warning("Please configure your Student Profile in the sidebar first!")
    else:
        st.session_state.chat_history.append({"role": "student", "content": user_question})
        save_chat_message(name, grade, age, "student", user_question)
        
        try:
            save_activity(
                student_name=name,
                student_grade=grade,
                student_age=age,
                activity_type="question",
                topic=favorite_subject if favorite_subject else "General",
                score=0
            )
        except Exception as db_err:
            print(f"Database logging background error: {db_err}")
            
        stats = get_student_stats(name, grade, age)
        analysis = get_student_learning_analysis(name, grade, age)
        
        adaptive_context = f"""
        Current Mastery Level: {analysis.get('current_level', 'Medium')}
        Average Quiz Score: {stats.get('average_score', 0)}%
        Weak Topics: {', '.join(analysis.get('weak_topics', [])) if analysis.get('weak_topics') else 'None'}
        Strong Topics: {', '.join(analysis.get('strong_topics', [])) if analysis.get('strong_topics') else 'None'}
        """
        
        with st.spinner("Mwalimu is thinking..."):
            try:
                response = ask_mwalimu(
                    question=user_question,
                    student=student,
                    messages=st.session_state.chat_history,
                    adaptive_context=adaptive_context
                )
                if not response:
                    response = "Mambo! I received an empty response. Let's try asking that again."
            except Exception as e:
                response = f"Mwalimu configuration error: {str(e)}"
                
            if response:
                response = response.replace("User Safety: safe", "").strip()
                response = response.replace("User Safety:safe", "").strip()
                
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        save_chat_message(name, grade, age, "assistant", response)
        st.rerun()

# --- FOOTER LOGO RENDERING TRICK
logo_html_tag = ""
logo_path = "assets/logo112.png"

if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        logo_html_tag = f'<img src="data:image/png;base64,{b64}" width="20" style="vertical-align: middle; margin-right: 8px;">'
else:
    logo_html_tag = "📚 "

st.markdown(
    f"""
    <p style='color: gray; font-size: 0.85rem; display: flex; align-items: center;'>
        {logo_html_tag}
        Mwalimu AI App Version 0.5 | Gateway Hybrid Engine | © 2026 Copyright
    </p>
    """, 
    unsafe_allow_html=True
)