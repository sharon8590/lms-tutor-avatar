from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import render_template, request, session

import bcrypt
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# ---------------- MODELS ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))  # admin / user
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), nullable=False)
    subject_type = db.Column(db.String(50), nullable=False)  # Technical / Non-Technical
class LearningRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    subject_id = db.Column(db.Integer)
    status = db.Column(db.String(50), default="Pending")  # Pending / Approved

# -------- CREATE DATABASE -------- #
if not os.path.exists("database"):
    os.makedirs("database")

with app.app_context():
    db.create_all()

    # Create default admin (only once)
    if not User.query.filter_by(email="admin@lms.com").first():
        hashed_pw = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
        admin = User(
            name="Admin",
            email="admin@lms.com",
            password=hashed_pw,
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Default Admin Created")

# ---------------- ROUTES ---------------- #

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode(), user.password):
            session["user_id"] = user.id
            session["role"] = user.role

            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("user_dashboard"))
        else:
            flash("Invalid Email or Password")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for("register"))

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        user = User(
            name=name,
            email=email,
            password=hashed_pw,
            role="user"
        )
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("admin_dashboard.html")

@app.route("/user")
def user_dashboard():
    if session.get("role") != "user":
        return redirect(url_for("login"))
    return render_template("user_dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/admin/subjects", methods=["GET", "POST"])
def manage_subjects():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["subject_name"]
        s_type = request.form["subject_type"]

        subject = Subject(subject_name=name, subject_type=s_type)
        db.session.add(subject)
        db.session.commit()
        flash("Subject added successfully")

    subjects = Subject.query.all()
    return render_template("admin_subjects.html", subjects=subjects)
@app.route("/admin/subject/edit/<int:id>", methods=["GET", "POST"])
def edit_subject(id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    subject = Subject.query.get_or_404(id)

    if request.method == "POST":
        subject.subject_name = request.form["subject_name"]
        subject.subject_type = request.form["subject_type"]
        db.session.commit()
        flash("Subject updated successfully")
        return redirect(url_for("manage_subjects"))

    return render_template("edit_subject.html", subject=subject)
@app.route("/admin/subject/delete/<int:id>")
def delete_subject(id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash("Subject deleted successfully")
    return redirect(url_for("manage_subjects"))

@app.route("/user/subjects", methods=["GET", "POST"])
def user_subjects():
    if session.get("role") != "user":
        return redirect(url_for("login"))

    subjects = Subject.query.all()

    if request.method == "POST":
        subject_id = request.form["subject_id"]

        # Avoid duplicate requests
        existing = LearningRequest.query.filter_by(
            user_id=session["user_id"],
            subject_id=subject_id
        ).first()

        if existing:
            flash("You already requested this subject")
        else:
            req = LearningRequest(
                user_id=session["user_id"],
                subject_id=subject_id
            )
            db.session.add(req)
            db.session.commit()
            flash("Learning request sent successfully")

    return render_template("user_subjects.html", subjects=subjects)
@app.route("/user/requests")
def user_requests():
    if session.get("role") != "user":
        return redirect(url_for("login"))

    requests = db.session.query(
        LearningRequest, Subject
    ).join(Subject, LearningRequest.subject_id == Subject.id)\
     .filter(LearningRequest.user_id == session["user_id"]).all()

    return render_template("user_requests.html", requests=requests)

@app.route("/user/ai-tutor", methods=["GET", "POST"])
def ai_tutor():
    if "user_id" not in session:
        return redirect("/login")

    response = ""

    if request.method == "POST":
        subject = request.form["subject"]
        question = request.form["question"]

        # Simple AI Logic (can upgrade later)
        response = ai_reply(subject, question)

    return render_template("ai_tutor.html", response=response)


def ai_reply(subject, question):
    subject = subject.lower()

    if subject == "python":
        return f"""
Python Answer:
{question}

Explanation:
Python is a high-level programming language. This concept involves syntax, logic, and examples.

Example:
print("Hello World")
"""

    elif subject == "machine learning":
        return f"""
Machine Learning Answer:
{question}

Explanation:
Machine Learning enables systems to learn from data without explicit programming.

Example:
Supervised learning uses labeled data.
"""

    elif subject == "soft skills":
        return f"""
Soft Skills Answer:
{question}

Explanation:
Soft skills involve communication, confidence, and interpersonal abilities.

Tip:
Practice speaking clearly and confidently.
"""

    else:
        return "This subject is not yet supported."


@app.route("/user/voice-tutor", methods=["GET", "POST"])
def voice_tutor():
    if "user_id" not in session:
        return redirect("/login")

    response = ""

    if request.method == "POST":
        question = request.form["question"]
        response = ai_reply("general", question)

    return render_template("voice_tutor.html", response=response)


@app.route("/user/voice-tutor/<subject>", methods=["GET", "POST"])
def subject_voice_tutor(subject):
    if "user_id" not in session:
        return redirect("/login")

    response = ""

    if request.method == "POST":
        question = request.form["question"]
        response = ai_reply(subject, question)

    return render_template(
        "subject_voice_tutor.html",
        subject=subject,
        response=response
    )

@app.route("/user/voice-subjects")
def voice_subjects():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("voice_subject_select.html")

quiz_questions = [
    {
        "question": "What keyword is used to define a function in Python?",
        "answer": "def"
    },
    {
        "question": "What does HTML stand for?",
        "answer": "hypertext markup language"
    }
]

@app.route("/user/voice-quiz", methods=["GET", "POST"])
def voice_quiz():
    if "user_id" not in session:
        return redirect("/login")

    q = quiz_questions[0]
    result = ""

    if request.method == "POST":
        user_answer = request.form["answer"].lower()
        if q["answer"] in user_answer:
            result = "Correct answer! Well done."
        else:
            result = f"Wrong answer. The correct answer is {q['answer']}"

    return render_template("voice_quiz.html", question=q["question"], result=result)

@app.route("/user/voice-puzzle", methods=["GET", "POST"])
def voice_puzzle():
    if "user_id" not in session:
        return redirect("/login")

    puzzle = "I speak without a mouth and hear without ears. What am I?"
    answer = "echo"
    result = ""

    if request.method == "POST":
        user_answer = request.form["answer"].lower()
        if answer in user_answer:
            result = "Correct! You solved the puzzle."
        else:
            result = "Incorrect. Try again."

    return render_template("voice_puzzle.html", puzzle=puzzle, result=result)

if __name__ == "__main__":
    app.run(debug=True)