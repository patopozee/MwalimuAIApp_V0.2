# 🎓 Mwalimu AI App

> **Shaping Minds, Shifting Futures.**

Mwalimu AI App is an AI-powered educational platform built specifically for Kenyan primary and secondary school students. It combines personalized tutoring, intelligent lesson generation, adaptive quizzes, flashcards, and study planning into one learning environment.

The application uses Google's Gemini models (via OpenRouter) together with Python, Streamlit, and SQLite to deliver personalized educational experiences based on each student's learning profile, academic performance, and preferred learning style.

---

# 🌟 Features

## 💬 AI Tutor (Ask Mwalimu)

* Personalized AI teacher
* Context-aware conversations
* Remembers previous discussions
* Adapts explanations to:

  * Grade level
  * Age
  * Learning style
  * Preferred language
* Supports:

  * English
  * Kiswahili
  * Sheng

---

## 📝 Interactive Quiz Generator

Generate AI-powered quizzes for any subject.

Features include:

* Multiple-choice questions
* Grade-specific difficulty
* Interactive answering
* Automatic scoring
* Answer review
* Performance tracking

---

## 🃏 AI Flashcards

Generate study flashcards instantly.

Features:

* Active recall learning
* Question & answer cards
* Personalized to the student profile
* Ideal for revision and exam preparation

---

## 📖 AI Lesson Generator

Generate complete textbook-style lessons.

Each lesson includes:

* Lesson title
* Learning objectives
* Introduction
* Detailed explanations
* Kenyan real-life examples
* Worked examples
* Practice exercises
* Summary
* Homework

Lessons are generated according to the student's:

* Grade
* Age
* Learning style
* Preferred language

---

## 📅 AI Personalized Study Planner

Automatically creates personalized daily study schedules using:

* Student profile
* Weak subjects
* Learning preferences
* Previous performance

---

## 📊 Student Progress Dashboard

Track academic growth over time.

Includes:

* Questions asked
* Quizzes completed
* Average quiz score
* Weak topic detection
* Performance analytics
* Study history

---

## 🧠 Adaptive Learning

Mwalimu AI continuously adapts learning by analyzing:

* Previous quiz scores
* Weak topics
* Frequently asked questions
* Student learning preferences

This allows the platform to recommend better lessons, quizzes, and study plans over time.

---

# 🏗️ Technology Stack

| Technology    | Purpose            |
| ------------- | ------------------ |
| Python        | Backend            |
| Streamlit     | User Interface     |
| SQLite        | Local Database     |
| Google Gemini | AI Model           |
| OpenRouter    | AI Gateway         |
| Pillow        | Image Processing   |
| Plotly        | Performance Charts |
| Pandas        | Data Analysis      |

---

# 📂 Project Structure

```text
Mwalimu-AI/
│
├── assets/
│   ├── logo112.png
│   └── logo211.png
│
├── app.py                 # AI engine
├── database.py            # SQLite database functions
├── web.py                 # Streamlit user interface
├── requirements.txt
├── README.md
└── .env
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mwalimu-ai.git

cd mwalimu-ai
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file.

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

## 5. Run the Application

```bash
streamlit run web.py
```

Open your browser:

```
http://localhost:8501
```

---

# 📸 Screenshots

You can showcase screenshots such as:

* Home Dashboard
* Ask Mwalimu
* Quiz Generator
* AI Lessons Generator
* Flashcards
* Personalized Study Planner
* Student Progress Dashboard

---

# 🎯 Current Features

* ✅ AI Tutor
* ✅ Interactive Quiz Generator
* ✅ AI Lesson Generator
* ✅ AI Flashcards
* ✅ Personalized Study Plans
* ✅ Student Progress Tracking
* ✅ Adaptive Learning
* ✅ Weak Topic Detection
* ✅ SQLite Database
* ✅ Performance Charts
* ✅ Responsive Streamlit Interface

---

# 🔒 Configuration Notes

To ensure stability:

* `st.set_page_config()` must be the first Streamlit command.
* Configure your OpenRouter API key in the `.env` file.
* Keep database initialization enabled before launching the application.
* Avoid modifying session-state keys without initialization.

---

# 🚧 Roadmap

Upcoming features include:

* 🔊 Text-to-Speech Lessons
* 🎙️ Voice Conversations
* 📄 PDF Lesson Export
* 📈 Parent & Teacher Dashboards
* 🏆 Gamification (Badges & Rewards)
* 👨‍🏫 Teacher Portal
* 🌐 Web Deployment
* 📱 Android Application
* ☁️ Cloud Database
* 🔐 Student Authentication

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Developer

**JP Cyber Services**

**Mwalimu AI App**

*"Shaping Minds, Shifting Futures."*
