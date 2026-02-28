from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Student, Admin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey123'

db.init_app(app)

with app.app_context():
    db.create_all()

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
            return redirect(url_for('index'))
        else:
            flash("Invalid Credentials!", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

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

    return render_template('index.html', students=students, search=search)

# ---------------- ADD STUDENT ---------------- #

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_student = Student(
            name=request.form['name'],
            email=request.form['email'],
            course=request.form['course']
        )
        db.session.add(new_student)
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


if __name__ == '__main__':
    app.run(debug=True)