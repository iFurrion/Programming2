import os
from collections import defaultdict

# 🎨 Color decorator using ANSI escape codes
def color(color: str):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "end": "\033[0m"
    }

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{colors.get(color, '')}{result}{colors['end']}"
        return wrapper
    return decorator

class StudentFile:
    def __init__(self, filename):
        self._filename = filename
        self._students = None  # lazy load: name → points

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new_filename):
        if not os.path.exists(new_filename):
            raise FileNotFoundError("File doesn't exist.")
        self._filename = new_filename
        self._students = None

    @property
    def subject(self):
        return os.path.splitext(os.path.basename(self._filename))[0]

    def _read_students(self):
        with open(self._filename, "r") as file:
            for line in file:
                if line.strip():
                    name, points = line.strip().rsplit(",", 1)
                    yield name.strip(), int(points.strip())

    @property
    def students(self):
        if self._students is None:
            self._students = {name: points for name, points in self._read_students()}
        return self._students

    @staticmethod
    def file_exists(path):
        return os.path.isfile(path)

    @classmethod
    def from_subject(cls, subject_name):
        return cls(f"{subject_name}.txt")

    @color("blue")
    def __str__(self):
        return f"StudentFile({self.subject})"

    def __add__(self, other):
        return self.concat_two_files(other)

    def concat_two_files(self, other):
        combined = {**self.students}
        for name, points in other.students.items():
            combined[name] = max(points, combined.get(name, 0))

        new_filename = f"combined_{self.subject}_{other.subject}.txt"
        with open(new_filename, "w") as f:
            for name, points in sorted(combined.items()):
                f.write(f"{name}, {points}\n")
        return StudentFile(new_filename)

    def concat_multiple(self, *others):
        combined = {**self.students}
        for other in others:
            for name, points in other.students.items():
                combined[name] = max(points, combined.get(name, 0))

        new_filename = f"multi_combined_{self.subject}.txt"
        with open(new_filename, "w") as f:
            for name, points in sorted(combined.items()):
                f.write(f"{name}, {points}\n")
        return StudentFile(new_filename)

    @staticmethod
    def color_students(*student_files):
        appearance_counts = defaultdict(int)
        student_scores = defaultdict(list)

        for file in student_files:
            for name, points in file.students.items():
                appearance_counts[name] += 1
                student_scores[name].append(points)

        for name in sorted(appearance_counts):
            count = appearance_counts[name]
            if count == 1:
                color_code = "\033[92m"  # green
            elif count == 2:
                color_code = "\033[91m"  # red
            else:
                color_code = "\033[95m"  # magenta

            avg_points = sum(student_scores[name]) // len(student_scores[name])
            print(f"{color_code}{name} - Avg Points: {avg_points}\033[0m")

class ColoredStudentFile(StudentFile):
    @color("green")
    def __str__(self):
        return f"ColoredStudentFile({self.subject})"

    def count_students(self):
        return len(self.students)

    def concat_two_files(self, other):
        print("Using ColoredStudentFile to combine files...")
        return super().concat_two_files(other)

# Example usage
if __name__ == "__main__":
    sf1 = StudentFile("math.txt")
    sf2 = StudentFile("science.txt")
    sf3 = StudentFile("history.txt")

    combined = sf1.concat_multiple(sf2, sf3)
    print(combined)

    print("📚 Students in combined file:")
    for name, points in combined.students.items():
        print(f"{name}: {points}")

    print("\n🎨 Colored Student Overlap:")
    StudentFile.color_students(sf1, sf2, sf3)
