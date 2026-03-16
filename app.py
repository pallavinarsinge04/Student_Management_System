from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
from models import db, Student, Admin
from werkzeug.security import generate_password_hash, check_password_hash
import csv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey123'

db.init_app(app)

# ---------------- DATABASE SETUP ---------------- #

with app.app_context():
    db.create_all()

    admin = Admin.query.filter_by(username="pallavi").first()

    if not admin:
        new_admin = Admin(
            username="pallavi",
            password=generate_password_hash("pallavi123")
        )
        db.session.add(new_admin)
        db.session.commit()

# ---------------- LOGIN ---------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):

            session['admin'] = username
            flash("Login Successful!", "success")

            return redirect(url_for('dashboard'))

        else:
            flash("Invalid Credentials!", "danger")

    return render_template('login.html')

# ---------------- LOGOUT ---------------- #

@app.route('/logout')
def logout():

    session.pop('admin', None)
    flash("Logged out successfully!", "info")

    return redirect(url_for('login'))

# ---------------- DASHBOARD ---------------- #

@app.route('/dashboard')
def dashboard():

    if 'admin' not in session:
        return redirect(url_for('login'))

    total_students = Student.query.count()

    page = request.args.get('page', 1, type=int)

    students = Student.query.paginate(page=page, per_page=5)

    return render_template(
        'dashboard.html',
        total_students=total_students,
        students=students
    )

# ---------------- HOME ---------------- #

@app.route('/')
def index():

    if 'admin' not in session:
        return redirect(url_for('login'))

    search = request.args.get('search')

    page = request.args.get('page', 1, type=int)

    if search:
        students = Student.query.filter(
            Student.name.contains(search) |
            Student.email.contains(search) |
            Student.course.contains(search)
        ).paginate(page=page, per_page=5)

    else:
        students = Student.query.paginate(page=page, per_page=5)

    return render_template(
        'index.html',
        students=students,
        search=search
    )

# ---------------- ADD STUDENT ---------------- #

@app.route('/add', methods=['GET', 'POST'])
def add_student():

    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        student = Student(
            name=request.form['name'],
            email=request.form['email'],
            course=request.form['course']
        )

        db.session.add(student)
        db.session.commit()

        flash("Student Added Successfully!", "success")

        return redirect(url_for('index'))

    return render_template('add_student.html')

# ---------------- EDIT STUDENT ---------------- #

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):

    if 'admin' not in session:
        return redirect(url_for('login'))

    student = Student.query.get_or_404(id)

    if request.method == 'POST':

        student.name = request.form['name']
        student.email = request.form['email']
        student.course = request.form['course']

        db.session.commit()

        flash("Student Updated Successfully!", "success")

        return redirect(url_for('index'))

    return render_template('edit_student.html', student=student)

# ---------------- DELETE STUDENT ---------------- #

@app.route('/delete/<int:id>')
def delete_student(id):

    if 'admin' not in session:
        return redirect(url_for('login'))

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash("Student Deleted Successfully!", "danger")

    return redirect(url_for('index'))

# ---------------- EXPORT CSV ---------------- #

@app.route('/export')
def export_students():

    if 'admin' not in session:
        return redirect(url_for('login'))

    students = Student.query.all()

    def generate():

        data = "Name,Email,Course\n"

        for s in students:
            data += f"{s.name},{s.email},{s.course}\n"

        return data

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=students.csv"}
    )

# ---------------- RUN APP ---------------- #

if __name__ == '__main__':
    
    app.run(debug=True)