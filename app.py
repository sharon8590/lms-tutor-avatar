from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
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

if __name__ == "__main__":
    app.run(debug=True)