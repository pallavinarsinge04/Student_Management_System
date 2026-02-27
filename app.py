from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, Student, Admin
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# -------------------------
# Create Database & Admin
# -------------------------
with app.app_context():
    if not os.path.exists("instance"):
        os.makedirs("instance")

    db.create_all()

    # Create default admin if not exists
    if not Admin.query.filter_by(username="admin").first():
        admin = Admin(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()


# -------------------------
# LOGIN ROUTE
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            session["admin"] = admin.username
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")


# -------------------------
# LOGOUT ROUTE
# -------------------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))


# -------------------------
# HOME - VIEW STUDENTS
# -------------------------
@app.route("/")
def index():
    if "admin" not in session:
        return redirect(url_for("login"))

    students = Student.query.all()
    return render_template("index.html", students=students)


# -------------------------
# ADD STUDENT
# -------------------------
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]

        new_student = Student(name=name, email=email, course=course)
        db.session.add(new_student)
        db.session.commit()

        flash("Student added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add_student.html")


# -------------------------
# UPDATE STUDENT
# -------------------------
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    student = Student.query.get_or_404(id)

    if request.method == "POST":
        student.name = request.form["name"]
        student.email = request.form["email"]
        student.course = request.form["course"]

        db.session.commit()
        flash("Student updated successfully!", "info")
        return redirect(url_for("index"))

    return render_template("add_student.html", student=student)


# -------------------------
# DELETE STUDENT
# -------------------------
@app.route("/delete/<int:id>")
def delete_student(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!", "danger")
    return redirect(url_for("index"))


# -------------------------
# SEARCH STUDENT
# -------------------------
@app.route("/search", methods=["POST"])
def search():
    if "admin" not in session:
        return redirect(url_for("login"))

    name = request.form["name"]
    students = Student.query.filter(Student.name.like(f"%{name}%")).all()
    return render_template("index.html", students=students)


# -------------------------
# RUN APP
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)