# 🎓 Mwalimu AI App

<div align="center">

### An AI-Powered Personalized Learning Assistant for Kenyan Students

Built with **Python**, **Streamlit**, and **Large Language Models (LLMs)**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![AI](https://img.shields.io/badge/AI-Powered-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## 📖 Overview

**Mwalimu AI** is an intelligent tutoring platform designed to provide personalized, adaptive, and engaging educational support for students.

Unlike traditional chatbots, Mwalimu AI adjusts explanations based on:

* 🎓 Grade level
* 👤 Student age
* 🧠 Learning style
* ⭐ Academic strengths
* 📉 Academic weaknesses
* 🌍 Preferred language

The goal is to create an AI tutor that feels like a real teacher—capable of explaining concepts differently for every learner.

---

## ✨ Current Features (Version 0.4)

### 🤖 Personalized AI Teacher

Mwalimu AI provides:

* Age-appropriate explanations
* Grade-specific content adaptation
* Interactive teaching methods
* Step-by-step problem solving
* Encouraging feedback
* Personalized examples

---

### 👨‍🎓 Dynamic Student Profiles

Students can customize their learning experience using a profile system.

#### Profile Attributes

* Name
* Age
* Grade
* Favorite Subject
* Weak Subject
* Learning Style
* Preferred Language

All profile information is injected into the AI context at runtime.

---

### 💬 Conversational Memory

Unlike a traditional Q&A bot, Mwalimu AI remembers previous messages during a session.

Example:

Student:

> What is photosynthesis?

Mwalimu AI:

> Photosynthesis is the process by which plants make food.

Student:

> Explain it in Kiswahili.

Mwalimu AI understands what "it" refers to and continues the conversation naturally.

---

### 🌐 Modern Streamlit Interface

Features include:

* Responsive design
* Sidebar student profile management
* Chat-style interaction
* Session memory
* Loading indicators
* One-click chat clearing

---

## 🏗️ System Architecture

```text
                 Student
                    │
                    ▼
         Streamlit Frontend (web.py)
                    │
                    ▼
       Conversation & Profile Manager
                    │
                    ▼
          Mwalimu AI Engine (app.py)
                    │
                    ▼
          Large Language Model (LLM)
                    │
                    ▼
      Personalized Educational Response
```

---

## 📂 Project Structure

```text
MwalimuAI/
│
├── app.py
│   └── AI engine and prompt management
│
├── web.py
│   └── Streamlit frontend interface
│
├── .env
│   └── Environment variables
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation
│
└── assets/
    └── Screenshots and media
```

---

## 🛠️ Technology Stack

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| Python 3.10+     | Core application development    |
| Streamlit        | Web application framework       |
| Gemini / LLM API | AI-powered tutoring             |
| python-dotenv    | Environment variable management |
| Session State    | Conversational memory           |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/MwalimuAI.git

cd MwalimuAI
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example requirements:

```text
streamlit
google-genai
python-dotenv
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

### 5. Launch the Application

```bash
streamlit run web.py
```

Application URL:

```text
http://localhost:8501
```

---

## 🧠 How Mwalimu AI Works

### Step 1 — Student Creates Profile

The learner provides:

* Name
* Grade
* Age
* Learning style
* Language preference

---

### Step 2 — Student Asks a Question

Example:

> What is a fraction?

---

### Step 3 — AI Builds Context

The engine combines:

* Student profile
* Previous conversation history
* Teaching instructions

---

### Step 4 — AI Generates Response

The LLM produces a personalized explanation tailored to the learner.

---

## 📸 Screenshots

```text
assets/
├── homepage.png
├── profile-sidebar.png
├── chat-interface.png
└── personalized-response.png
```

---

## 🚀 Roadmap

### Version 0.5

* [ ] Student accounts
* [ ] SQLite database integration
* [ ] Learning history storage
* [ ] Progress tracking

### Version 0.6

* [ ] AI-generated quizzes
* [ ] Homework assistant
* [ ] Lesson summary generator
* [ ] Flashcard creator

### Version 0.7

* [ ] CBC curriculum integration
* [ ] KCSE revision materials
* [ ] Retrieval-Augmented Generation (RAG)
* [ ] Vector database knowledge base

### Version 1.0

* [ ] Teacher dashboard
* [ ] Parent dashboard
* [ ] Voice tutoring
* [ ] Multi-agent AI learning ecosystem

---

## 🎯 Vision

Our long-term goal is to build a complete AI-powered educational platform capable of delivering personalized learning experiences to students across Kenya and beyond.

Mwalimu AI aims to become:

* A personal tutor
* A study planner
* A homework assistant
* A revision coach
* A progress tracking system

All in one platform.

---

## 🤝 Contributing

Contributions are welcome.

To contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

---

## 👨‍💻 Author

**Mugo Young Millionaire**

* Python Developer
* AI Enthusiast
* Educational Technology Builder

---

## 📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute the software in accordance with the license terms.
