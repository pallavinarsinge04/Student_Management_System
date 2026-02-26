from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Student

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


# Home Page
@app.route('/')
def home():
    students = Student.query.all()
    return render_template("view_students.html", students=students)

# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        marks = request.form['marks']

        new_student = Student(name=name, email=email, course=course, marks=marks)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add_student.html")

# Update Student
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.course = request.form['course']
        student.marks = request.form['marks']

        db.session.commit()
        return redirect(url_for('home'))

    return render_template("update_student.html", student=student)

# Delete Student
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)