from student_record import AdvancedStudentRecordManager

manager = AdvancedStudentRecordManager("students.txt")

# Add a new student
manager.add_student("Charlie Black", "Math", 48)

# Display all students
print("All students:")
for student in manager.read_students():
    print(student)

# Filtered
print("\nMath students:")
for student in manager.filter_by_subject("Math"):
    print(student)

# Grade status display (uses decorator)
print("\nGrade evaluation:")
print("Charlie Black:", manager.grade_status(48))
print("Alice Brown:", manager.grade_status(78))
