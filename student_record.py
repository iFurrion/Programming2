import os
from functools import wraps

def color_text(color):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            color_code = {"red": "\033[91m", "green": "\033[92m", "reset": "\033[0m"}
            if "Fail" in text:
                return f"{color_code['red']}{text}{color_code['reset']}"
            return f"{color_code['green']}{text}{color_code['reset']}"
        return wrapper
    return decorator

class StudentRecordManager:
    def __init__(self, filename):
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new_name):
        if os.path.exists(new_name):
            self._filename = new_name

    def read_students(self):
        with open(self._filename) as f:
            for line in f:
                yield line.strip()

    def get_all_students(self):
        return [line for line in self.read_students()]

    def overwrite_students(self, new_lines):
        with open(self._filename, "w") as f:
            f.writelines(line + "\n" for line in new_lines)

    @staticmethod
    def format_student(name, subject, score):
        return f"{name},{subject},{score}"

    @classmethod
    def from_template(cls):
        return cls("students.txt")

    def add_student(self, name, subject, score):
        line = self.format_student(name, subject, score)
        with open(self._filename, "a") as f:
            f.write(line + "\n")

    def __str__(self):
        return f"StudentRecordManager({self._filename})"

    def __add__(self, other):
        if isinstance(other, StudentRecordManager):
            combined = self.get_all_students() + other.get_all_students()
            new_file = "combined_students.txt"
            with open(new_file, "w") as f:
                f.write("\n".join(combined))
            return StudentRecordManager(new_file)
        raise ValueError("Only StudentRecordManager instances can be combined.")

class AdvancedStudentRecordManager(StudentRecordManager):
    def add_student(self, name, subject, score):
        # Overriding for input validation
        if not (0 <= int(score) <= 100):
            raise ValueError("Score must be between 0 and 100.")
        super().add_student(name, subject, score)

    def filter_by_subject(self, subject):
        for line in self.read_students():
            parts = line.split(",")
            if len(parts) == 3 and parts[1].strip().lower() == subject.lower():
                yield line

    @color_text("red")
    def grade_status(self, score):
        return "Pass" if int(score) >= 50 else "Fail"
