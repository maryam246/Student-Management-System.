import json
import os
import logging

# Configure the logging settings
logging.basicConfig(filename="events.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def __str__(self):
        return f"Username: {self.username}, Role: {self.role}"

class UnauthorizedAccessException(Exception):
    pass

class Teacher(User):
    def __init__(self, username, password):
        super().__init__(username, password, "Teacher")
        self.load_assigned_courses()
        self.load_grades()  # Load existing grade data

    def login(self, password):
        # Implement user authentication logic here
        if self.password == password:
            logging.info(f"Teacher {self.username} logged in.")
        else:
            raise UnauthorizedAccessException("Unauthorized access.")

    def load_assigned_courses(self):
        # Load assigned courses for the teacher from a JSON file
        teacher_data_filename = f"{self.username}_assign_course.json"
        self.assigned_courses = []
        if os.path.exists(teacher_data_filename):
            with open(teacher_data_filename, "r") as teacher_data_file:
                teacher_data = json.load(teacher_data_file)
                self.assigned_courses = teacher_data.get(self.username, [])

    def load_grades(self):
        # Load grades for the teacher's courses from a JSON file
        grades_data_filename = f"{self.username}_grades.json"
        self.grades = {}
        if os.path.exists(grades_data_filename):
            with open(grades_data_filename, "r") as grades_data_file:
                self.grades = json.load(grades_data_file)

    def view_assigned_courses(self):
        # Display the courses assigned to the teacher
        if self.assigned_courses:
            print(f"Assigned Courses for Teacher {self.username}:")
            for course_name in self.assigned_courses:
                print(course_name)
        else:
            print("No courses assigned to this teacher.")

    def enter_grade(self, student_username, course_id, grade):
        # Check if the teacher is assigned to the course
        if course_id not in self.assigned_courses:
            print(f"Teacher {self.username} is not assigned to course {course_id}.")
            return False

        # Check if the student exists
        if student_username not in self.grades:
            self.grades[student_username] = {}

        # Enter the grade for the student
        self.grades[student_username][course_id] = grade

        # Save the updated grade data to a JSON file
        self.save_grades(student_username)

        print(f"Grade entered for student '{student_username}' in course '{course_id}'.")
        return True

    def update_grade(self, student_username, course_id, new_grade):
        # Check if the teacher is assigned to the course
        if course_id not in self.assigned_courses:
            print(f"Teacher {self.username} is not assigned to course {course_id}.")
            return False

        # Check if the student exists
        if student_username not in self.grades:
            print(f"Student '{student_username}' not found.")
            return False

        # Check if the course exists in the student's grades
        if course_id not in self.grades[student_username]:
            print(f"Course '{course_id}' not found in student '{student_username}' grades.")
            return False

        # Update the grade for the student
        self.grades[student_username][course_id] = new_grade

        # Save the updated grade data to the JSON file
        self.save_grades(student_username)

        print(f"Grade updated for student '{student_username}' in course '{course_id}'.")
        return True

    def save_grades(self, student_username):
        # Save grade data to the JSON file named "student_username_grades.json" for the specific student
        student_grades_data_filename = f"{student_username}_grades.json"
        with open(student_grades_data_filename, "w") as grades_data_file:
            json.dump(self.grades[student_username], grades_data_file, indent=4)
            logging.info(f"Saved grade data for student '{student_username}' to {student_grades_data_filename}")

    def export_grades(self, course_id, filename):
        # Check if the teacher is assigned to the course
        if course_id not in self.assigned_courses:
            print(f"Teacher {self.username} is not assigned to course {course_id}.")
            return False

        # Extract the grades for the specified course
        course_grades = {}
        for student_username, grades in self.grades.items():
            if course_id in grades:
                course_grades[student_username] = grades[course_id]

        # Export agrades for the course to a file (JSON format)
        with open(filename, "w") as course_grades_file:
            json.dump(course_grades, course_grades_file, indent=4)
            logging.info(f"Exported grades for course '{course_id}' to {filename}")
            print(f"Exported grades for course '{course_id}' to {filename}")
