from PIL import Image
import streamlit as st
import sqlite3
import os
import base64  # Added for absolute bulletproof image injection
from app import ask_mwalimu, generate_quiz, generate_study_plan
    

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
# Initialize chat history if it doesn't exist in the current session state yet
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "study_plan" not in st.session_state:
    st.session_state.study_plan = None


from database import (
    create_tables,
    save_activity,
    get_student_stats,
    get_student_quiz_history,
    get_next_difficulty,          # Add this
    get_student_learning_analysis
    
)

# Build structure safely at startup
create_tables()

# Page Setup
st.set_page_config(
    page_title="Mwalimu AI App",
    page_icon="assets/logo112.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- BASE64 SIDEBAR IMAGE INJECTOR ---
try:
    with open("assets/logo211.png", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    sidebar_bg_style = f"background-image: url('data:image/png;base64,{encoded_logo}') !important;"
except Exception:
    sidebar_bg_style = "" # Fallback if path changes

# --------------------------------------------------
# GLOBAL UI & CSS LAYOUT SETTINGS (UNIFIED & CLEANED)
# --------------------------------------------------
st.html(f"""
    <style>
        /* ========================================================
           DESKTOP ONLY: COLLAPSE SPACE (Wider than 768px)
           ======================================================== */
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

        /* ========================================================
           MOBILE ONLY PRESETS (Narrower than 767px)
           ======================================================== */
        @media (max-width: 767px) {{
            [data-testid="stHeader"], header {{
                background-color: transparent !important;
                height: 3.5rem !important; 
            }}
            [data-testid="stAppViewMainObj"], .stMain, [data-testid="stMain"] {{
                margin-top: 0rem !important; 
                padding-top: 0.5rem !important;
            }}
            [data-testid="stMainBlockContainer"], 
            [data-testid="stAppViewBlockContainer"], 
            .block-container {{
                padding-top: 1rem !important; 
            }}
        }}

        /* ========================================================
           UNIVERSAL LAYOUT CONTROLS
           ======================================================== */
        [data-testid="stHeader"] button {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 4px !important;
            z-index: 999999 !important;
        }}

        /* FORCE THE CONTENT ZONE TO TIGHTEN AGAINST THE NEW HEADER LOGO */
        [data-testid="stSidebarUserContent"] {{
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }}

        /* ========================================================
           THE SECRET WEAPON: INJECT LOGO VIA BASE64 DATA DIRECTLY 
           ======================================================== */
        [data-testid="stSidebarHeader"] {{
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
            margin-bottom: 0rem !important;
            min-height: 80px !important;
            
            {sidebar_bg_style}
            background-size: contain !important;
            background-repeat: no-repeat !important;
            background-position: left center !important;
            margin-left: 55px !important; /* Shifts right slightly so it doesn't collide with the toggle button */
        }}
    </style>
""")

# --------------------------------------------------
# TITLE & INTRO (Pulled completely to the top)
# --------------------------------------------------
col1, col2 = st.columns([1, 5], vertical_alignment="center")

with col1:
    title_logo = Image.open("assets/logo112.png")
    st.html("<div style='margin-top: 0 !important; margin-bottom: 0 !important;'>")
    st.image(title_logo, width=100)
    st.html("</div>")

with col2:
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

st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

st.write(
    """
    Welcome! I am your friendly Kenyan AI teacher.
    Create your profile and ask me any school question.
    You can also generate quizzes tailored to your grade level,
    learning style, and preferred language.
    """
)

# --------------------------------------------------
# SIDEBAR UI ELEMENTS
# --------------------------------------------------
# (Note: Standard image tags are completely removed here to prevent duplication!)
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
    
    # 1. Fetch the adaptive learning analysis from your database
    analysis = get_student_learning_analysis(name, grade, age)
    
    # 2. Display current adaptive status tier cleanly
    st.sidebar.markdown(f"**Learning Status:** `{analysis['current_level']}`")
    
    # 3. Conditionally render weak performance topics
    if analysis.get('weak_topics'):
        st.sidebar.markdown("⚠️ **Needs Improvement:**")
        for t in analysis['weak_topics']:
            st.sidebar.caption(f"• {t}")
            
    # 4. Conditionally render mastered topics
    if analysis.get('strong_topics'):
        st.sidebar.markdown("🏆 **Mastered Areas:**")
        for t in analysis['strong_topics']:
            st.sidebar.caption(f"• {t}")
            
    # 5. Render historical trends plot
    history_scores = get_student_quiz_history(name, grade, age)
    if len(history_scores) > 0:
        st.sidebar.markdown("**📈 Performance Trend**")
        st.sidebar.line_chart(history_scores)
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
            # Step 3 & 4: Automatically resolve adaptive difficulty tier 
            target_diff = get_next_difficulty(name, grade, age, quiz_topic)
            
            # Pass resolved tier straight to the generation engine [cite: 79, 82]
            st.session_state.quiz = generate_quiz(quiz_topic, student, target_diff)
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_raw_score = 0
            
            # Log initial event footprint tracking
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

# --- AI STUDY PLAN SECTION ---
st.markdown("---")
st.subheader("📅 AI Personalized Study Plan")

if st.button("Generate Today's Study Plan"):
    if not name:
        st.warning("Please configure your Student Profile in the sidebar first!")
    else:
        with st.spinner("Creating your personalized study plan..."):
            # 1. Fetch metrics safely using name
            stats = get_student_stats(name, age, grade)
            
            # 2. Re-assemble student data matching your exact sidebar variables
            student_data = {
                "name": name,
                "grade": grade,  
                "age": age,      
                "favorite_subject": favorite_subject,
                "weak_subject": weak_subject,
                "learning_style": learning_style,
                "language": language
            }
            
            # 3. Call your core generation logic
            st.session_state.study_plan = generate_study_plan(student_data, stats)
        
        # This line must align EXACTLY with the "with" block above it
        st.rerun()

# Display the generated plan card if it exists
if st.session_state.study_plan:
    st.info("💡 Tip: Follow the allocated time intervals for maximum focus today!")
    st.markdown(st.session_state.study_plan)
    
    # Optional clear button to refresh the container
    if st.button("Clear Study Plan"):
        st.session_state.study_plan = None
        st.rerun()
# -----------------------------------
# DISPLAY CONVERSATION HISTORY
# -----------------------------------
st.markdown("---")
st.write("### 💬 Chat with Mwalimu")

# Loop through history entries and render them sequentially
for msg in st.session_state.chat_history:
    if msg["role"] == "student":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

# -----------------------------------
# MOBILE-SAFE INPUT
# -----------------------------------
# Handle user chat input
# Handle user chat input
if user_question := st.chat_input("Ask your question"):
    if not name:
        st.warning("Please configure your Student Profile in the sidebar first!")
    else:
        # 1. Immediately append the student's question to the session state array
        st.session_state.chat_history.append({"role": "student", "content": user_question})
        
        # 2. Save the question activity using your exact database parameters
        try:
            save_activity(
                student_name=name,
                student_grade=grade,
                student_age=age,
                activity_type="question",
                topic=favorite_subject,  # Pass your sidebar favorite_subject variable
                score=0
            )
        except Exception as db_err:
            print(f"Database logging background error: {db_err}")
            
        # 3. Extract metrics safely using all three required positional parameters
        stats = get_student_stats(name, grade, age)
        analysis = get_student_learning_analysis(name, grade, age)
        
        adaptive_context = f"""
        Current Mastery Level: {analysis.get('current_level', 'Medium')}
        Average Quiz Score: {stats.get('average_score', 0)}%
        Weak Topics: {', '.join(analysis.get('weak_topics', [])) if analysis.get('weak_topics') else 'None'}
        Strong Topics: {', '.join(analysis.get('strong_topics', [])) if analysis.get('strong_topics') else 'None'}
        """
        
        # 4. Call the model and store the answer
        with st.spinner("Mwalimu is thinking..."):
            try:
                response = ask_mwalimu(
                    question=user_question,
                    student=student,
                    messages=st.session_state.chat_history,
                    adaptive_context=adaptive_context
                )
                
                # Check if the response returned completely empty
                if not response:
                    response = "Mambo! I received an empty response. Let's try asking that again."
                    
            except Exception as e:
                response = f"Mwalimu configuration error: {str(e)}"
                
            if response:
                response = response.replace("User Safety: safe", "").strip()
                response = response.replace("User Safety:safe", "").strip()
                
        # 5. Append Mwalimu's answer to the session state array
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # 6. Trigger a single clear rerun to instantly update the UI elements
        st.rerun()

logo_html_tag = ""
logo_path = "assets/logo112.png"  # Or "logo112.png" depending on your active filename

if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        logo_html_tag = f'<img src="data:assets/logo112.png;base64,{b64}" width="20" style="vertical-align: middle; margin-right: 8px;">'
else:
    # Fallback emoji if file is misplaced
    logo_html_tag = "📚 "

# 2. Render the markdown with the encoded logo string
st.markdown(
    f"""
    <p style='color: gray; font-size: 0.85rem; display: flex; align-items: center;'>
        {logo_html_tag}
        Mwalimu AI App Version 0.5 | Gateway Hybrid Engine | © 2026 Copyright
    </p>
    """, 
    unsafe_allow_html=True
)