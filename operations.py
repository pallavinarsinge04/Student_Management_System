from database import connect_db

def add_student(student):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?)",
                   (student.student_id, student.name, student.age, student.course))

    conn.commit()
    conn.close()
    print("Student added successfully!")

def view_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
    print("Student deleted successfully!")

def update_student(student_id, new_name, new_age, new_course):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?
        WHERE student_id = ?
    """, (new_name, new_age, new_course, student_id))

    conn.commit()
    conn.close()
    print("Student updated successfully!")