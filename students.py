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


class Student(User):
    def __init__(self, username, password):
        super().__init__(username, password, "Student")
        self.load_grades()  # Load student's grades

    def login(self, password):
        # Implement user authentication logic here
        if self.password == password:
            logging.info(f"Student {self.username} logged in.")
        else:
            raise UnauthorizedAccessException("Unauthorized access.")

    def load_grades(self):
        # Load the student's grades from a JSON file
        grades_data_filename = f"{self.username}_grades.json"
        self.grades = {}
        if os.path.exists(grades_data_filename):
            with open(grades_data_filename, "r") as grades_data_file:
                self.grades = json.load(grades_data_file)

    def view_grades(self):
        # Display the grades assigned by teachers for the student's courses
        if self.grades:
            print(f"Your Grades:{self.username}")
            for course, grade in self.grades.items():
                print(f"Course: {course}, Grade: {grade}")
        else:
            print("You have no grades yet.")

    def export_grades(self, filename):
        # Export the student's grades to a JSON file
        with open(filename, "w") as file:
            json.dump(self.grades, file)
        print(f"Grades exported to {filename}")
