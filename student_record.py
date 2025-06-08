import os
from collections import defaultdict

# This decorator adds color to text output using ANSI escape codes
def colorize(color: str):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "end": "\033[0m"
    }
    def decorator(func):
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            return f"{colors.get(color, '')}{text}{colors['end']}"
        return wrapper
    return decorator

class StudentFile:
    def __init__(self, filename):
        self._filename = filename
        self._students = None  # This will store the student names once loaded

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new_filename):
        if not os.path.exists(new_filename):
            raise FileNotFoundError(f"File '{new_filename}' does not exist!")
        self._filename = new_filename
        self._students = None  # Reset cached students when filename changes

    def _read_students(self):
        # Generator to read each line from the file one by one
        with open(self._filename, "r") as file:
            for line in file:
                yield line.strip()

    @property
    def students(self):
        # Load students from file only once, then reuse the list
        if self._students is None:
            self._students = [student for student in self._read_students()]
        return self._students

    @staticmethod
    def file_exists(filepath):
        return os.path.isfile(filepath)

    @classmethod
    def from_subject(cls, subject):
        # Create a StudentFile object from a subject name like "math" -> "math.txt"
        filename = subject + ".txt"
        return cls(filename)

    @colorize("blue")
    def __str__(self):
        return f"StudentFile: {self._filename}"

    def __add__(self, other):
        # Allow adding two StudentFiles with '+' operator to combine them
        return self.concat_two_files(other)

    def concat_two_files(self, other):
        # Combine students from two files, remove duplicates, save to new file
        combined_students = sorted(set(self.students + other.students))
        new_filename = f"combined_{self.filename}_{other.filename}.txt"
        with open(new_filename, "w") as new_file:
            for student in combined_students:
                new_file.write(student + "\n")
        return StudentFile(new_filename)

    def concat_multiple(self, *others):
        # Combine students from self and any number of other StudentFiles
        combined_students = set(self.students)
        for other in others:
            combined_students.update(other.students)
        new_filename = f"multi_combined_{self.filename}.txt"
        with open(new_filename, "w") as new_file:
            for student in sorted(combined_students):
                new_file.write(student + "\n")
        return StudentFile(new_filename)

    @staticmethod
    def color_students(*student_files):
        # Count how many files each student appears in
        counts = defaultdict(int)
        for sf in student_files:
            unique_students = set(sf.students)
            for student in unique_students:
                counts[student] += 1

        # Print each student with color based on how many files they are in
        for student, count in sorted(counts.items()):
            if count == 1:
                color_code = "\033[92m"  # green
            elif count == 2:
                color_code = "\033[91m"  # red
            else:
                color_code = "\033[95m"  # magenta for 3 or more
            print(f"{color_code}{student}\033[0m")

class ColoredStudentFile(StudentFile):
    @colorize("green")
    def __str__(self):
        return f"ColoredStudentFile: {self.filename}"

    def count_students(self):
        return len(self.students)

    def concat_two_files(self, other):
        print("Using ColoredStudentFile's merge")
        return super().concat_two_files(other)

if __name__ == "__main__":
    # Make sure these text files exist in the same folder
    math = StudentFile("math.txt")
    science = StudentFile("science.txt")
    history = StudentFile("history.txt")

    combined_file = math.concat_multiple(science, history)
    print(combined_file)

    print("\nStudents in combined file:")
    for student in combined_file.students:
        print(student)

    print("\nColored students based on how many subjects they take:")
    StudentFile.color_students(math, science, history)
