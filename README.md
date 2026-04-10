<div align="center">
  <img src="https://img.shields.io/badge/Flask-3.0.0-black?style=for-the-badge&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-green?style=for-the-badge&logo=openai" alt="OpenAI">
  <img src="https://img.shields.io/badge/SQLite-3.0+-lightblue?style=for-the-badge&logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
  
  <br>
  
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=30&duration=3000&pause=500&color=6A0DAD&center=true&vCenter=true&width=600&lines=AI-Powered+Learning+System;Voice-Enabled+Tutor+Avatar;BTech+Major+Project" alt="Typing SVG">
</div>

<h1 align="center">📚 AI Tutor Avatar - Learning Management System</h1>

<p align="center">
  <b>An Intelligent, Voice-Enabled Learning Platform with Emotion-Aware AI Tutoring</b>
  <br>
  <i>🎓 BTech Final Year Project | 🤖 Powered by OpenAI GPT-4o-mini | 🎙️ Voice Interaction Ready</i>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-demo">Demo</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-api-endpoints">API</a> •
  <a href="#-screenshots">Screenshots</a>
</p>

<hr>

## 🚀 Overview

**AI Tutor Avatar** is a comprehensive Learning Management System that revolutionizes online education by combining traditional LMS features with cutting-edge AI capabilities. The platform features a voice-enabled tutor avatar that understands student emotions and provides personalized learning experiences.

### ✨ Key Highlights

| Feature | Description |
|---------|-------------|
| 🎙️ **Voice Tutor** | Interactive voice-based learning sessions |
| 🤖 **AI-Powered Responses** | GPT-4o-mini integration for intelligent explanations |
| 😊 **Emotion Detection** | Real-time student emotion analysis |
| 📚 **Subject Management** | Technical & Non-Technical subject organization |
| 👥 **Role-Based Access** | Separate portals for Admin and Users |
| 📊 **Request Tracking** | Student learning request workflow |
| 🧩 **Interactive Quizzes** | Voice-enabled quizzes and puzzles |
| 📈 **Progress Monitoring** | Track learning progress and emotions |

## 🎯 Features

### 👨‍💼 Admin Features
- ✅ **Dashboard Overview** - Complete system analytics
- 📚 **Subject Management** - Add, edit, delete subjects (Technical/Non-Technical)
- 👥 **User Management** - View and manage all registered users
- 📋 **Request Management** - Approve/Reject learning requests
- 😊 **Emotion Analytics** - Track student emotional states during learning
- 📊 **Reports** - Generate learning analytics reports

### 👩‍🎓 User Features
- 🔐 **Authentication** - Secure registration and login
- 📚 **Browse Subjects** - Explore available learning subjects
- 📝 **Learning Requests** - Request subjects for learning
- 🤖 **AI Tutor** - Ask questions and get AI-generated explanations
- 🎙️ **Voice Tutor** - Voice-enabled learning with emotion tracking
- 🧩 **Interactive Quizzes** - Test knowledge with voice quizzes
- 🎯 **Puzzles** - Solve engaging learning puzzles
- 📈 **Request Status** - Track approval status of requests

### 🤖 AI Capabilities
- **OpenAI GPT-4o-mini Integration** - Intelligent responses to student queries
- **Emotion Detection** - Analyzes student messages to detect emotions:
  - 😊 Happy | 😕 Confused | 😤 Frustrated | 🎉 Excited | 😐 Neutral
- **Context-Aware Tutoring** - Subject-specific teaching approaches
- **Personalized Learning** - Adapts responses based on student needs

## 🛠️ Tech Stack

<details open>
<summary><b>Backend</b></summary>

| Technology | Version | Purpose |
|------------|---------|---------|
| **Flask** | 3.0.0 | Web Framework |
| **SQLAlchemy** | 3.0.5 | ORM for Database |
| **SQLite** | 3.x | Database Engine |
| **bcrypt** | 4.0.1 | Password Hashing |
| **OpenAI** | Latest | GPT-4o-mini API |

</details>

<details>
<summary><b>Frontend</b></summary>

| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure |
| **CSS3** | Styling |
| **JavaScript** | Interactivity |
| **Jinja2** | Templating |

</details>

<details>
<summary><b>Voice & Audio (Planned/Partial)</b></summary>

| Library | Purpose |
|---------|---------|
| **pyttsx3** | Text-to-Speech |
| **speechrecognition** | Voice Input |
| **pyaudio** | Audio Processing |

</details>



---

## 📁 Project Structure

```text
tutor_avatar_lms/
│
├── 📄 app.py               # Main Flask Application (Core Logic)
├── 📄 config.py            # Configuration & API Settings
├── 📄 requirements.txt     # Python Dependencies
├── 📄 .gitignore           # Git Ignore Rules
│
├── 📁 database/            # SQLite Database Storage
│   └── 📄 lms.db           # Main Database File
│
├── 📁 templates/           # HTML Templates (Jinja2)
│   ├── 📄 login.html       # Authentication Pages
│   ├── 📄 register.html
│   ├── 📄 admin_*.html     # Admin Management Suite
│   ├── 📄 user_*.html      # Student Dashboards
│   └── 📄 voice_*.html     # Interactive Voice/AI Components
│
├── 📁 static/              # Static Assets
│   └── 📁 avatar/          # Tutor Avatar Assets
│       ├── 🖼️ idle.png     # Idle State Image
│       └── 🎬 talking.gif  # Speaking Animation
│
└── 📁 modules/             # Custom Logic
    └── 📄 voice.py         # Voice Processing & NLP Module

```

## 🚀 Installation

### 🔧 Prerequisites
- Python 3.10+
- OpenAI API Key

---

### ⚙️ Setup

```bash
# Clone repo
git clone https://github.com/sharon8590/lms-tutor-avatar.git
cd lms-tutor-avatar

# Create virtual env
python -m venv venv

# Activate
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set API key
set OPENAI_API_KEY=your_key_here

# Run app
python app.py

```

## 🔐 Default Admin Login

| Role | Email | Password |
|------|------|---------|
| 👑 Admin | admin@lms.com | admin123 |

---

## 📖 Usage

### 👨‍💼 Admin
- Manage subjects  
- Approve requests  
- Monitor users  
- View emotion analytics  

### 👩‍🎓 User
- Register account  
- Request subjects  
- Learn using AI Tutor  
- Use voice-based learning  
- Attempt quizzes  

---

## 🔌 API Overview

### 🔑 Auth
- `/` → Login  
- `/register` → Register  
- `/logout` → Logout  

### 👨‍💼 Admin
- `/admin`  
- `/admin/subjects`  
- `/admin/users`  
- `/admin/requests`  
- `/admin/emotions`  

### 👩‍🎓 User
- `/user`  
- `/user/subjects`  
- `/user/ai-tutor`  
- `/user/voice-tutor`  
- `/user/voice-quiz`  

---

## 🔐 Security

- ✅ Password hashing (bcrypt)  
- ✅ Session management  
- ✅ Role-based access  
- ✅ SQL injection protection  

---

## 🚧 Future Enhancements

- 🎙️ Full voice integration  
- 📹 Live video classes  
- 📜 Certificate generation  
- 💳 Payment gateway  
- 📱 Mobile app  
- 🎮 Gamification system  

---

## 🤝 Contributing

```bash
git checkout -b feature/new-feature
git commit -m "Added new feature"
git push origin feature/new-feature

```

👨‍💻 Author

Sharon Biju
🔗 GitHub: https://github.com/sharon8590

⭐ Support

If you like this project:

⭐ Star the repository
📢 Share with others
<div align="center">

💙 Built for BTech Final Year Project
🚀 Powered by AI + Innovation

</div> ```
