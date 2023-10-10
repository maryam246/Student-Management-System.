from admin import Administrator, UnauthorizedAccessException
from teachers import Teacher
from students import Student
import logging

# Configure the logging settings
logging.basicConfig(filename="events.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    user_type = input("Select User Type (1 for Administrator, 2 for Teacher, 3 for student): ")
    print("Login")

    if user_type == "1":
        admin_username = input("Enter administrator username: ")
        admin_password = input("Enter administrator password: ")

        # Create an Administrator instance
        admin = Administrator(admin_username, admin_password)

        # Authenticate the administrator
        try:
            admin.login(admin_password)
        except UnauthorizedAccessException as e:
            print(str(e))
            return

        while True:
            print("\nAdministrator Menu:")
            print("1. Add Student")
            print("2. Remove Student")
            print("3. Add Teacher")
            print("4. Remove Teacher")
            print("5. Add Course")
            print("6. Remove Course")
            print("7. Assign Teacher to Course")
            print("8. Export Student Data")
            print("9. Export Course Data")
            print("10. Logout.")

            choice = input("Enter your choice: ")

            if choice == "1":
                student_username = input("Enter student username: ")
                student_password = input("Enter student password: ")
                admin.add_student(student_username, student_password)

            elif choice == "2":
                student_username = input("Enter student username to remove: ")
                admin.remove_student(student_username)

            elif choice == "3":
                teacher_username = input("Enter teacher username: ")
                teacher_password = input("Enter teacher password: ")
                admin.add_teacher(teacher_username, teacher_password)

            elif choice == "4":
                teacher_username = input("Enter teacher username to remove: ")
                admin.remove_teacher(teacher_username)

            elif choice == "5":
                course_id = input("Enter course ID: ")
                course_name = input("Enter course name: ")
                admin.add_course(course_id, course_name)

            elif choice == "6":
                course_id = input("Enter course ID to remove: ")
                admin.remove_course(course_id)

            elif choice == "7":
                teacher_username = input("Enter teacher username: ")
                course_id = input("Enter course ID: ")
                admin.assign_course_to_teacher(teacher_username, course_id)

            elif choice == "8":
                filename = input("Enter filename to export student data (e.g., student_data.json): ")
                admin.export_student_data(filename)

            elif choice == "9":
                filename = input("Enter filename to export course data (e.g., course_data.json): ")
                admin.export_course_data(filename)

            elif choice == "10":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please select a valid option.")

    elif user_type == "2":
        teacher_username = input("Enter teacher username: ")
        teacher_password = input("Enter teacher password: ")

        # Create a Teacher instance
        teacher = Teacher(teacher_username, teacher_password)

        # Authenticate the teacher
        try:
            teacher.login(teacher_password)
        except UnauthorizedAccessException as e:
            print(str(e))
            return

        while True:
            print("\nTeacher Menu:")
            print("1. View Assigned Courses")
            print("2. Enter Grade")
            print("3. Update Grade")
            print("4. Export Grades")
            print("5. Logout.")

            choice = input("Enter your choice: ")

            if choice == "1":
                teacher.view_assigned_courses()


            elif choice == "2":
                # Teacher enter grade...
                student_username = input("Enter student username: ")
                course_id = input("Enter course ID: ")
                grade = input("Enter grade: ")
                if teacher.enter_grade(student_username, course_id, grade):
                    print(f"Grade entered for student '{student_username}' in course '{course_id}'.")

            elif choice == "3":
                # Teacher update grade...
                student_username = input("Enter student username: ")
                course_id = input("Enter course ID: ")
                new_grade = input("Enter new grade: ")
                if teacher.update_grade(student_username, course_id, new_grade):
                    print(f"Grade updated for student '{student_username}' in course '{course_id}'.")

            elif choice == "4":
                # Teacher export grades...
                course_id = input("Enter course ID to export grades: ")
                filename = input("Enter filename (e.g., grades.json): ")
                if teacher.export_grades(course_id, filename):
                    print(f"Grades exported to '{filename}' for course '{course_id}'.")

            elif choice == "5":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please select a valid option.")

    elif user_type == "3":
        student_username = input("Enter student username: ")
        student_password = input("Enter student password: ")
        # Create a Student instance
        student = Student(student_username, student_password)

        # Authenticate the student
        try:
            student.login(student_password)
        except UnauthorizedAccessException as e:
            print(str(e))
            return

        while True:
            print("\nStudent Menu:")
            print("1. View Grades")
            print("2. Export Grades")
            print("3. Logout.")

            choice = input("Enter your choice: ")

            if choice == "1":
                student.view_grades()

            elif choice == "2":
                filename = input("Enter filename to export your grades (e.g., your_grades.json): ")
                student.export_grades(filename)

            elif choice == "3":
                print("Logging out...")
                break

            else:
                print("Invalid choice. Please select a valid option.")

    else:
        print("Invalid user type. Please select a valid user type (1 for Administrator, 2 for Teacher,3 for student).")


if __name__ == "__main__":
    main()
