import streamlit as st
from streamlit_mic_recorder import mic_recorder
from voice import speech_to_text, text_to_speech
from app import ask_mwalimu
from database import save_chat_message

def render_voice_tutor_page(client):
    st.title("🎙️ Mwalimu AI - Voice Tutor")
    st.write("Click the microphone below to talk with your AI Teacher. Speak clearly!")

    # Extract student profile properties from session state
    name = st.session_state.get("student_name", "Student")
    grade = st.session_state.get("grade", "Grade 7")
    age = st.session_state.get("age", 10)
    favorite_subject = st.session_state.get("favorite_subject", "General")
    weak_subject = st.session_state.get("weak_subject", "")
    learning_style = st.session_state.get("learning_style", "Interactive")
    language = st.session_state.get("language", "English")

    student = {
        "name": name, "grade": grade, "age": age, 
        "favorite_subject": favorite_subject, "weak_subject": weak_subject, 
        "learning_style": learning_style, "language": language
    }

    # Persistent Pipeline State
    if "user_spoken_text" not in st.session_state:
        st.session_state.user_spoken_text = ""
    if "mwalimu_response_text" not in st.session_state:
        st.session_state.mwalimu_response_text = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Audio Recorder Widget
    col1, col2 = st.columns([1.5, 4])
    with col1:
        st.write("**Record Question:**")
        audio_record = mic_recorder(
            start_prompt="🎙️ Start Speaking",
            stop_prompt="🛑 Stop & Send",
            key="voice_tutor_mic"
        )

    # STEP 1: Process Audio safely when user clicks "Stop & Send"
    if audio_record:
        audio_bytes = audio_record['bytes']
        
        if not st.session_state.user_spoken_text:
            with st.spinner("✍️ Writing down your words..."):
                transcription = speech_to_text(audio_bytes)
                
                # STRICT SYSTEM SAFETY FILTER: Stop if the response indicates an API failure
                if "failed" in transcription.lower() or "error" in transcription.lower():
                    st.error(f"⚠️ Audio Pipeline Blocked: {transcription}")
                    st.warning("Please check your OpenRouter API key configurations or credit limits.")
                elif transcription.strip() == "":
                    st.warning("Could not hear anything clearly. Please check microphone access.")
                else:
                    # Success path: store actual speech
                    st.session_state.user_spoken_text = transcription
                    st.session_state.chat_history.append({"role": "user", "content": transcription})
                    save_chat_message(name, grade, age, "user", transcription)

    # STEP 2: Render user speech text & trigger LLM context pipelines
    if st.session_state.user_spoken_text:
        st.info(f"🗣️ **What you said:** {st.session_state.user_spoken_text}")
        
        if not st.session_state.mwalimu_response_text:
            with st.spinner("🤔 Mwalimu is thinking..."):
                try:
                    adaptive_context = f"Learning Style: {learning_style}, Favorite Subject: {favorite_subject}"
                    
                    ai_response_text = ask_mwalimu(
                        question=st.session_state.user_spoken_text,
                        student=student,
                        messages=st.session_state.chat_history[:-1], 
                        adaptive_context=adaptive_context
                    )
                    
                    if ai_response_text:
                        ai_response_text = ai_response_text.replace("User Safety: safe", "").strip()
                        st.session_state.mwalimu_response_text = ai_response_text
                        st.session_state.chat_history.append({"role": "assistant", "content": ai_response_text})
                        save_chat_message(name, grade, age, "assistant", ai_response_text)
                    else:
                        st.session_state.mwalimu_response_text = "Mambo! I missed that, let's try again."
                        
                except Exception as e:
                    st.error(f"Mwalimu setup issue: {str(e)}")

    # STEP 3: Display clean response text and play back voice
    if st.session_state.mwalimu_response_text:
        st.success(f"🤖 **Mwalimu AI:** {st.session_state.mwalimu_response_text}")
        
        # Reset workflow button
        if st.button("🔄 Next Question"):
            st.session_state.user_spoken_text = ""
            st.session_state.mwalimu_response_text = ""
            st.rerun()