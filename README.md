# 🎓 Mwalimu AI App

<div align="center">

### Your Personalized AI Teacher for Kenyan Students

An intelligent educational platform built with **Python**, **Streamlit**, and **OpenRouter AI**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red?logo=streamlit)
![OpenRouter](https://img.shields.io/badge/OpenRouter-AI%20Gateway-purple)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 📖 Overview

**Mwalimu AI App** is an AI-powered educational assistant designed to provide personalized learning experiences for students.

Inspired by the role of a real Kenyan teacher (*Mwalimu*), the platform adapts explanations, examples, and quizzes based on each learner's:

* 🎓 Grade level
* 👤 Age
* ⭐ Favorite subjects
* 📉 Weak subjects
* 🧠 Learning style
* 🌍 Preferred language (English, Kiswahili, or Sheng)

The goal is to make learning more engaging, accessible, and personalized for every student.

---

# ✨ Features

## 👨‍🎓 Personalized Student Profiles

Students can customize their learning experience through an interactive profile system.

### Profile Attributes

* Student Name
* Grade Level (Grade 1 – Form 4)
* Age
* Favorite Subject
* Weak Subject
* Learning Style
* Preferred Language

Mwalimu AI uses this information to tailor every response.

---

## 🤖 AI-Powered Classroom Assistant

Ask questions on any school topic and receive:

* Grade-appropriate explanations
* Personalized examples
* Step-by-step guidance
* Encouraging feedback
* Practice questions

The AI adapts its teaching style to suit each learner.

---

## 💬 Context-Aware Conversations

Unlike traditional chatbots, Mwalimu AI remembers the ongoing conversation during a session.

This allows students to ask follow-up questions naturally, such as:

> What is photosynthesis?

Then:

> Explain it in Kiswahili.

The AI understands the context automatically.

---

## 📝 Instant Quiz Generator

Generate customized quizzes on any topic.

Features include:

* 5 multiple-choice questions
* Grade-level adaptation
* Personalized difficulty
* Topic-specific assessment
* Instant generation

Example topics:

* Fractions
* Photosynthesis
* Electricity
* English Grammar
* History

---

## ⚡ High-Availability AI Routing

Powered by **OpenRouter**, Mwalimu AI benefits from:

* Unified AI gateway architecture
* Intelligent model routing
* Reduced downtime
* Improved reliability
* Simplified API management

---

# 🏗️ System Architecture

```text
                 Student
                    │
                    ▼
          Streamlit Frontend
                 (web.py)
                    │
                    ▼
         Session State Manager
                    │
                    ▼
            Mwalimu Engine
                 (app.py)
                    │
                    ▼
            OpenRouter API
                    │
                    ▼
            Large Language Model
                    │
                    ▼
      Personalized Learning Response
```

---

# 🛠️ Technology Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python 3.10+  | Core application development    |
| Streamlit     | Interactive web interface       |
| OpenRouter    | AI model gateway                |
| OpenAI SDK    | API client                      |
| python-dotenv | Environment variable management |
| Session State | Conversation memory             |

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/MwalimuAI.git

cd MwalimuAI
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example requirements:

```text
streamlit
openai
python-dotenv
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

⚠️ Never commit your `.env` file to GitHub.

---

## 5. Run the Application

```bash
streamlit run web.py
```

The application will launch locally at:

```text
http://localhost:8501
```

---

# 📂 Project Structure

```text
MwalimuAI/
│
├── app.py
│   └── AI engine, prompt management, quiz generation
│
├── web.py
│   └── Streamlit UI, student profiles, chat interface
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
    └── Screenshots and images
```

---

# 📸 Screenshots

```text
assets/
├── homepage.png
├── student-profile.png
├── quiz-generator.png
└── classroom-chat.png
```

---

# ☁️ Deployment

Mwalimu AI is optimized for deployment on **Streamlit Community Cloud**.

### Push Your Code

```bash
git add .

git commit -m "feat: deploy production-ready Mwalimu AI"

git push origin main
```

### Deploy

1. Connect your GitHub repository to Streamlit Community Cloud.
2. Select your repository.
3. Set:

```text
Main file path:
web.py
```

4. Add your secret key:

```toml
OPENROUTER_API_KEY="your_actual_api_key"
```

5. Deploy 🚀

---

# 🗺️ Roadmap

## Version 0.5

* [ ] Interactive quizzes
* [ ] Automatic quiz grading
* [ ] Quiz score tracking

## Version 0.6

* [ ] Student progress dashboard
* [ ] SQLite database integration
* [ ] Learning history

## Version 0.7

* [ ] Homework assistant
* [ ] Flashcard generator
* [ ] Study planner

## Version 0.8

* [ ] CBC curriculum knowledge base
* [ ] KCSE revision materials
* [ ] Retrieval-Augmented Generation (RAG)

## Version 1.0

* [ ] Voice tutoring
* [ ] Parent dashboard
* [ ] Teacher dashboard
* [ ] Full AI learning ecosystem

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

---

# 👨‍💻 Author

**Mugo Young Millionaire**

Python Developer • AI Enthusiast • Educational Technology Builder

Building AI-powered learning tools for the next generation of students.

---

# 📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute the software in accordance with the license terms.

