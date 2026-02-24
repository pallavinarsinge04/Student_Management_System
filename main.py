from student import Student
from database import create_table
from operations import add_student, view_students, delete_student, update_student

def menu():
    print("\n--- Student Management System ---")
    print("1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

def main():
    create_table()

    while True:
        menu()
        choice = input("Enter choice: ")

        if choice == "1":
            student_id = input("Enter ID: ")
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            course = input("Enter Course: ")

            student = Student(student_id, name, age, course)
            add_student(student)

        elif choice == "2":
            view_students()

        elif choice == "3":
            student_id = input("Enter ID to update: ")
            name = input("Enter New Name: ")
            age = int(input("Enter New Age: "))
            course = input("Enter New Course: ")
            update_student(student_id, name, age, course)

        elif choice == "4":
            student_id = input("Enter ID to delete: ")
            delete_student(student_id)

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()