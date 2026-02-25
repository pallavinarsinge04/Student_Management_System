from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    course = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"