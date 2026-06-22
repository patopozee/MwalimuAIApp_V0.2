# 🎓 Mwalimu AI

> An AI-powered personalized learning assistant built with **Python**, **Streamlit**, and **Google Gemini 2.5 Flash**.

Mwalimu AI is designed to provide students with an engaging, adaptive, and personalized learning experience. The platform acts as an intelligent tutor that adjusts explanations based on a student's age, grade level, learning style, strengths, weaknesses, and preferred language.

---

## 🌟 Features

### 🤖 AI-Powered Teacher

Mwalimu AI leverages **Google Gemini 2.5 Flash** to deliver:

* Personalized explanations tailored to student profiles
* Age and grade-appropriate learning content
* Practical real-world examples
* Encouraging and supportive feedback
* Adaptive teaching strategies

### 👨‍🎓 Dynamic Student Profiles

Students can customize their learning experience through an interactive sidebar.

Profile attributes include:

* Name
* Age
* Grade Level
* Favorite Subject
* Weak Subject
* Learning Style

  * Visual
  * Auditory
  * Reading/Writing
  * Kinesthetic
* Preferred Language

  * English
  * Kiswahili
  * Sheng

All profile information is dynamically injected into the AI system prompt, ensuring every response is personalized.

### 🧠 Quick Challenge Mode

To encourage critical thinking, Mwalimu AI presents students with engaging brain teasers and learning challenges based on their interests and academic profile.

### 🌐 Interactive Web Interface

Built using **Streamlit**, the application includes:

* Modern dark-themed UI
* Dynamic sidebar controls
* Session state persistence
* Real-time AI responses
* Easy profile customization

---

## 🏗️ System Architecture

```text
Student
   │
   ▼
Streamlit Frontend
(web.py)
   │
   ▼
ask_mwalimu()
(app.py)
   │
   ▼
Google Gemini API
(gemini-2.5-flash)
   │
   ▼
Personalized Learning Response
```

---

## 📂 Project Structure

```text
MwalimuAIApp_V0.2/
│
├── app.py               # Gemini integration and AI engine
├── web.py               # Streamlit frontend
├── .env                 # Environment variables
├── requirements.txt     # Dependencies
└── README.md            # Project documentation
```

---

## 🛠️ Technology Stack

| Technology              | Purpose                   |
| ----------------------- | ------------------------- |
| Python 3.10+            | Core Programming Language |
| Streamlit               | Web Application Framework |
| Google Gemini 2.5 Flash | AI Model                  |
| google-genai            | Gemini SDK                |
| python-dotenv           | Environment Management    |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<YOUR_USERNAME>/MwalimuAIApp_V0.2.git
cd MwalimuAIApp_V0.2
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:

```txt
streamlit
google-genai
python-dotenv
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

> ⚠️ Never commit your `.env` file or API keys to GitHub.

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run web.py
```

The application will launch locally at:

```text
http://localhost:8501
```

---

## 📸 Screenshots

Add screenshots of your application here:

```text
assets/
├── homepage.png
├── sidebar-profile.png
└── ai-response.png
```

Example:

![Mwalimu AI Home](assets/homepage.png)

---

## 🚀 Future Roadmap

* [ ] Student authentication system
* [ ] Learning progress tracking
* [ ] AI-generated quizzes
* [ ] Performance analytics dashboard
* [ ] Multi-session memory
* [ ] Teacher dashboard
* [ ] Parent monitoring portal
* [ ] Voice-based tutoring
* [ ] Mobile application

---

## 🎯 Vision

Mwalimu AI aims to become a comprehensive intelligent learning ecosystem that delivers personalized education to every student, regardless of their learning style, language preference, or academic background.

By combining modern AI capabilities with adaptive teaching strategies, Mwalimu AI seeks to make learning more accessible, engaging, and effective for students everywhere.

---

## 👨‍💻 Author

**Mugo Young Millionaire**

* Python Developer
* AI & Machine Learning Enthusiast
* Building educational technology solutions powered by Large Language Models

---

## 📄 License

This project is licensed under the MIT License.

Feel free to fork, contribute, and improve the project.

## 🧠 How It Works Under the Hood
  Profile Synthesis: The student updates their specific parameters (Age, Grade, Preferred Language) in the Streamlit sidebar.

  Context Delivery: The student inputs a question and submits the form.

  System Prompt Construction: app.py bundles the user profile metadata alongside core behavioral constraints, instructing the model to reply using specific tones (e.g., using Sheng or phrasing math concepts using 3rd-grade metaphors).

  LLM Execution: The compiled prompt hits gemini-2.5-flash.

  UI Rendering: The response is seamlessly returned and parsed on screen.