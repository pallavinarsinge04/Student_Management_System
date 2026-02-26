from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Student
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Create DB if not exists
with app.app_context():
    if not os.path.exists("instance"):
        os.makedirs("instance")
    db.create_all()


# HOME - VIEW STUDENTS
@app.route("/")
def index():
    students = Student.query.all()
    return render_template("index.html", students=students)


# ADD STUDENT
@app.route("/add", methods=["GET", "POST"])
def add_student():
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


# UPDATE STUDENT
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        student.name = request.form["name"]
        student.email = request.form["email"]
        student.course = request.form["course"]

        db.session.commit()
        flash("Student updated successfully!", "info")
        return redirect(url_for("index"))

    return render_template("add_student.html", student=student)


# DELETE STUDENT
@app.route("/delete/<int:id>")
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!", "danger")
    return redirect(url_for("index"))


# SEARCH STUDENT
@app.route("/search", methods=["POST"])
def search():
    
    name = request.form["name"]
    students = Student.query.filter(Student.name.like(f"%{name}%")).all()
    return render_template("index.html", students=students)


if __name__ == "__main__":

    app.run(debug=True)