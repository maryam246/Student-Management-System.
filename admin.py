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

class Administrator(User):
    def __init__(self, username, password):
        super().__init__(username, password, "Administrator")
        self.students = {}  # Student database
        self.teachers = {}  # Teacher database
        self.courses = {}  # Course database

        # Initialize JSON filenames
        self.student_data_filename = "students.json"
        self.teacher_data_filename = "teachers.json"
        self.course_data_filename = "courses.json"

        # Load existing data from JSON files (if they exist)
        self.load_student_data()
        self.load_teacher_data()
        self.load_course_data()

    def login(self, password):
        # Implement user authentication logic here
        if self.password == password:
            logging.info(f"Administrator {self.username} logged in.")
        else:
            raise UnauthorizedAccessException("Unauthorized access.")

    def save_student_data(self):
        # Save student data to the JSON file
        with open(self.student_data_filename, "w") as student_data_file:
            student_data = {student.username: {"password": student.password, "role": student.role} for student in self.students.values()}
            json.dump(student_data, student_data_file, indent=4)
            logging.info(f"Saved student data to {self.student_data_filename}")

    def load_student_data(self):
        # Load student data from the JSON file (if it exists)
        if os.path.exists(self.student_data_filename):
            with open(self.student_data_filename, "r") as student_data_file:
                student_data = json.load(student_data_file)
                for username, data in student_data.items():
                    self.students[username] = User(username, data["password"], data["role"])
            logging.info(f"Loaded student data from {self.student_data_filename}")

    def save_teacher_data(self):
        # Save teacher data to the JSON file
        with open(self.teacher_data_filename, "w") as teacher_data_file:
            teacher_data = {teacher.username: {"password": teacher.password, "role": teacher.role} for teacher in self.teachers.values()}
            json.dump(teacher_data, teacher_data_file, indent=4)
            logging.info(f"Saved teacher data to {self.teacher_data_filename}")

    def load_teacher_data(self):
        # Load teacher data from the JSON file (if it exists)
        if os.path.exists(self.teacher_data_filename):
            with open(self.teacher_data_filename, "r") as teacher_data_file:
                teacher_data = json.load(teacher_data_file)
                for username, data in teacher_data.items():
                    self.teachers[username] = User(username, data["password"], data["role"])
            logging.info(f"Loaded teacher data from {self.teacher_data_filename}")

    def save_course_data(self):
        # Save course data to the JSON file
        with open(self.course_data_filename, "w") as course_data_file:
            json.dump(self.courses, course_data_file, indent=4)
            logging.info(f"Saved course data to {self.course_data_filename}")

    def load_course_data(self):
        # Load course data from the JSON file (if it exists)
        if os.path.exists(self.course_data_filename):
            with open(self.course_data_filename, "r") as course_data_file:
                self.courses = json.load(course_data_file)
            logging.info(f"Loaded course data from {self.course_data_filename}")

    def add_student(self, student_username, student_password):
        # Check if the student username is unique
        if student_username not in self.students:
            # Create a new Student object and add it to the user database
            new_student = User(student_username, student_password, "Student")
            self.students[student_username] = new_student
            logging.info(f"Added new student: {student_username}")
            print(f"Added student: {student_username}")
            # Save student data to the JSON file
            self.save_student_data()
        else:
            logging.warning(f"Student username '{student_username}' already exists. Please choose a different username.")
            print(f"User '{student_username}' already exists. Please choose a different username.")

    def remove_student(self, student_username):
        # Check if the student exists and remove them from the user database
        if student_username in self.students:
            del self.students[student_username]
            logging.info(f"Removed student: {student_username}")
            print(f"Removed student: {student_username}")
            # Save student data to the JSON file after removal
            self.save_student_data()
        else:
            logging.warning(f"Attempted to remove a non-existent student: {student_username}")
            print(f"Student '{student_username}' not found.")

    def add_teacher(self, teacher_username, teacher_password):
        # Check if the teacher username is unique
        if teacher_username not in self.teachers:
            # Create a new Teacher object and add it to the teacher database
            new_teacher = User(teacher_username, teacher_password, "Teacher")
            self.teachers[teacher_username] = new_teacher
            logging.info(f"Added new teacher: {teacher_username}")
            print(f"Added teacher: {teacher_username}")
            # Save teacher data to the JSON file
            self.save_teacher_data()
        else:
            logging.warning(f"Teacher username '{teacher_username}' already exists. Please choose a different username.")
            print(f"User '{teacher_username}' already exists. Please choose a different username.")

    def remove_teacher(self, teacher_username):
        # Check if the teacher exists and remove them from the teacher database
        if teacher_username in self.teachers:
            del self.teachers[teacher_username]
            logging.info(f"Removed teacher: {teacher_username}")
            print(f"Removed teacher: {teacher_username}")
            # Save teacher data to the JSON file after removal
            self.save_teacher_data()
        else:
            logging.warning(f"Attempted to remove a non-existent teacher: {teacher_username}")
            print(f"Teacher '{teacher_username}' not found.")

    def add_course(self, course_id, course_name):
        # Check if the course ID is unique
        if course_id not in self.courses:
            # Add a new course to the course database
            self.courses[course_id] = course_name
            logging.info(f"Added new course: {course_id}")
            print(f"Added course: {course_id}")
            # Save course data to the JSON file
            self.save_course_data()
        else:
            logging.warning(f"Course ID '{course_id}' already exists. Please choose a different ID.")
            print(f"Course ID '{course_id}' already exists. Please choose a different ID.")

    def remove_course(self, course_id):
        # Check if the course exists and remove it from the course database
        if course_id in self.courses:
            del self.courses[course_id]
            logging.info(f"Removed course: {course_id}")
            print(f"Removed course: {course_id}")
            # Save course data to the JSON file after removal
            self.save_course_data()
        else:
            logging.warning(f"Attempted to remove a non-existent course: {course_id}")
            print(f"Course '{course_id}' not found.")

    def assign_course_to_teacher(self, teacher_username, course_id):
        # Check if the teacher and course exist
        if teacher_username in self.teachers and course_id in self.courses:
            # Assign the course to the teacher
            teacher = self.teachers[teacher_username]
            teacher_assigned_courses = getattr(teacher, "assigned_courses", [])

            if course_id not in teacher_assigned_courses:
                teacher_assigned_courses.append(course_id)
                setattr(teacher, "assigned_courses", teacher_assigned_courses)
                logging.info(f"Assigned course '{course_id}' to teacher '{teacher_username}'")
                print(f"Assigned course '{course_id}' to teacher '{teacher_username}'")

                # Update the teacher JSON data file with the assigned courses
                teacher_data_filename = f"{teacher_username}_assign_course.json"  # Updated filename
                if os.path.exists(teacher_data_filename):
                    with open(teacher_data_filename, "r") as teacher_data_file:
                        teacher_data = json.load(teacher_data_file)
                    teacher_data[teacher_username] = teacher_assigned_courses
                    with open(teacher_data_filename, "w") as teacher_data_file:
                        json.dump(teacher_data, teacher_data_file, indent=4)
                else:
                    # If the teacher JSON file does not exist, create it with the assigned courses
                    teacher_data = {teacher_username: teacher_assigned_courses}
                    with open(teacher_data_filename, "w") as teacher_data_file:
                        json.dump(teacher_data, teacher_data_file, indent=4)

            else:
                logging.warning(f"Course '{course_id}' is already assigned to teacher '{teacher_username}'.")
                print(f"Course '{course_id}' is already assigned to teacher '{teacher_username}'.")
        else:
            logging.warning(f"Teacher '{teacher_username}' or course '{course_id}' not found.")
            print(f"Teacher '{teacher_username}' or course '{course_id}' not found.")


    def export_student_data(self, filename):
        # Prompt the user for the student username(s) to export
        student_usernames = input("Enter student username(s) to export (comma-separated): ").split(',')
        student_data_to_export = {}

        for username in student_usernames:
            username = username.strip()
            if username in self.students:
                student = self.students[username]
                student_data_to_export[username] = {"password": student.password, "role": student.role}
            else:
                logging.warning(f"Student username '{username}' not found. Skipping export for this user.")

        if student_data_to_export:
            # Export selected student data to a file (JSON format)
            with open(filename, "w") as student_data_file:
                json.dump(student_data_to_export, student_data_file, indent=4)
                logging.info(f"Exported student data to {filename}")
                print(f"Exported student data to {filename}")
        else:
            logging.warning("No valid student usernames provided for export.")

    def export_course_data(self, filename):
        # Prompt the user for the course ID(s) to export
        course_ids = input("Enter course ID(s) to export (comma-separated): ").split(',')
        course_data_to_export = {}

        for course_id in course_ids:
            course_id = course_id.strip()
            if course_id in self.courses:
                course_data_to_export[course_id] = self.courses[course_id]
            else:
                logging.warning(f"Course ID '{course_id}' not found. Skipping export for this course.")

        if course_data_to_export:
            # Export selected course data to a file (JSON format)
            with open(filename, "w") as course_data_file:
                json.dump(course_data_to_export, course_data_file, indent=4)
                logging.info(f"Exported course data to {filename}")
                print(f"Exported course data to {filename}")
        else:
            logging.warning("No valid course IDs provided for export.")
