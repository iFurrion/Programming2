import os
import pytest
from student_record import StudentFile, ColoredStudentFile

# Helper to create a sample text file
def create_sample_file(filename, lines):
    with open(filename, "w") as f:
        for line in lines:
            f.write(line + "\n")

@pytest.fixture
def sample_files(tmp_path):
    math = tmp_path / "math.txt"
    science = tmp_path / "science.txt"
    history = tmp_path / "history.txt"

    create_sample_file(math, [
        "Alice, 90",
        "Bob, 85"
    ])
    create_sample_file(science, [
        "Alice, 88",
        "Charlie, 77"
    ])
    create_sample_file(history, [
        "Bob, 70",
        "Charlie, 80",
        "David, 95"
    ])

    return str(math), str(science), str(history)

def test_file_exists(sample_files):
    math, science, _ = sample_files
    assert StudentFile.file_exists(math)
    assert StudentFile.file_exists(science)

def test_student_loading(sample_files):
    math, _, _ = sample_files
    sf = StudentFile(math)
    students = sf.students
    assert "Alice" in students
    assert students["Bob"] == 85

def test_concat_two_files(sample_files, tmp_path):
    math, science, _ = sample_files
    sf1 = StudentFile(math)
    sf2 = StudentFile(science)
    combined = sf1 + sf2
    assert "Charlie" in combined.students
    assert combined.students["Alice"] == 90  # Highest between 90 and 88
    assert os.path.exists(combined.filename)

def test_concat_multiple(sample_files):
    math, science, history = sample_files
    sf1 = StudentFile(math)
    sf2 = StudentFile(science)
    sf3 = StudentFile(history)
    combined = sf1.concat_multiple(sf2, sf3)

    assert "David" in combined.students
    assert combined.students["Alice"] == 90  # Best score retained
    assert len(combined.students) == 4

def test_colored_student_file_str(sample_files):
    math, _, _ = sample_files
    colored_file = ColoredStudentFile(math)
    assert "ColoredStudentFile" in str(colored_file)

def test_classmethod_from_subject(tmp_path):
    test_file = tmp_path / "english.txt"
    create_sample_file(test_file, ["Eve, 99"])
    sf = StudentFile.from_subject("english")
    sf.filename = str(test_file)  # rebind path if needed
    assert "Eve" in sf.students

