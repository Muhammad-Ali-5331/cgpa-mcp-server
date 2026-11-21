from pathlib import Path

COURSES = {
    1: [
        ("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation I", 0.5),
        ("GE-190", "Functional English", 3.0),
    ],
    2: [
        ("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation II", 0.5),
    ],
    3: [
        ("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation III", 0.5),
    ],
    4: [
        ("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation IV", 0.5),
    ],
    5: [
        ("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation V", 0.5),
    ],
    6: [
        ("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation VI", 0.5),
    ],
    7: [
        ("CC-411", "Final Year Project I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation VII", 0.5),
    ],
    8: [
        ("CC-412", "Final Year Project II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation VIII", 0.5),
    ],
}

def marks_to_grade_points(marks: int) -> float | str:
    """ Call this function/tool when student gives raw marks (0-100) and you need the grade-point equivalent before computing a GPA. """

    if marks < 0 or marks > 100: return "Error: marks must be between 0 and 100"
    if marks>=85: return 4.0
    elif marks>=80: return 3.7
    elif marks>=75: return 3.3
    elif marks>=70: return 3.0
    elif marks>=65: return 2.7
    elif marks>=61: return 2.3
    elif marks>=58: return 2.0
    elif marks>=55: return 1.7
    elif marks>=50: return 1.0
    else: return 0.0


def calculate_semester_gpa(grade_points: list[float], credit_hours: list[float]) -> float | str:
    """ Call this function/tool when you have a list of grade-points and credit-hours for a semester and you need to calculate one semester’s credit-weighted GPA. """

    if len(grade_points) != len(credit_hours):
        return "Error: grade_points and credit_hours must have the same length"

    if any(gp < 0.0 or gp > 4.0 for gp in grade_points):
        return "Error: grade_points must be between 0.0 and 4.0"
    if any(ch < 0 for ch in credit_hours):
        return "Error: credit_hours must be non-negative"

    semester_gpa = 0.0
    for i in range(len(grade_points)):
        semester_gpa += grade_points[i] * credit_hours[i]
    try:
        semester_gpa /= sum(credit_hours)
    except ZeroDivisionError:
        return "Error: total credit hours cannot be zero"
    return semester_gpa


def get_semester_courses(semester: int) -> str:
    """ Call this function/tool when you need to get or the student asks for the list of courses for a given semester.
    OR You can use this function/tool to get the list of courses for a given semester and their credit hours. """


    if semester not in COURSES: return "Error: semester must be between 1 and 8"
    res = ""
    for course in COURSES[semester]:
        res += f"{course[0]} - {course[1]} ({course[2]} credit hours)\n"
    return res


def get_remaining_credit_hours(current_semester: int) -> float | str:
    """ Call this function/tool when you need to get the total remaining credit hours for a student given their current semester. """

    if current_semester not in COURSES:
        return "Error: Current Semester must be between 1 and 8"

    remaining_credit_hours = 0.0
    for nxt_semester in range(current_semester+1, 9):
        for course in COURSES[nxt_semester]:
            remaining_credit_hours += course[2]
    return remaining_credit_hours


def get_credit_hours(semesters: list[int]) -> float | str:
    """ Call this function/tool when you need the TOTAL credit hours of one or more semesters, e.g. semesters=[5, 6]. """

    total = 0.0
    for sem in semesters:
        if sem not in COURSES:
            return "Error: every semester must be between 1 and 8"
        total += sum(course[2] for course in COURSES[sem])
    return total


def calculate_new_cgpa(current_cgpa: float, completed_credit_hours: float, semester_gpa: float, semester_credit_hours: float) -> float | str:
    """ Call this function/tool when you need to calculate the new CGPA after a semester given the current CGPA, completed credit hours, semester GPA, and semester credit hours. """

    
    if current_cgpa<0.0 or current_cgpa>4.0:
        return "Error: CGPA must be between 0.0 and 4.0"
    elif semester_gpa<0.0 or semester_gpa>4.0:
        return "Error: Semester GPA must be between 0.0 and 4.0"
    elif completed_credit_hours<0:
        return "Error: Completed credit hours must be non-negative"
    elif semester_credit_hours<0:
        return "Error: Semester credit hours must be non-negative"
    else:
        try:
            new_cgpa = (current_cgpa * completed_credit_hours + semester_gpa * semester_credit_hours) / (completed_credit_hours + semester_credit_hours)
        except ZeroDivisionError:
            return "Error: total credit hours cannot be zero"
        return new_cgpa


def required_gpa_for_target(target_cgpa: float, current_cgpa: float, completed_credit_hours: float, remaining_credit_hours: float) -> float | str:
    """ Call this function/tool when you need to calculate the required GPA for a student to achieve a target CGPA given their current CGPA, completed credit hours, and remaining credit hours. """

    if target_cgpa<0.0 or target_cgpa>4.0:
        return "Error: Target CGPA must be between 0.0 and 4.0"
    elif current_cgpa<0.0 or current_cgpa>4.0:
        return "Error: Current CGPA must be between 0.0 and 4.0"
    elif completed_credit_hours<0:
        return "Error: Completed credit hours must be non-negative"
    elif remaining_credit_hours<0:
        return "Error: Remaining credit hours must be non-negative"
    else:
        try:
            required_gpa = (target_cgpa * (completed_credit_hours + remaining_credit_hours) - current_cgpa * completed_credit_hours) / remaining_credit_hours
        except ZeroDivisionError:
            return "Error: remaining credit hours cannot be zero"
        return required_gpa


def save_report(filename: str, content: str) -> str:
    """ Call this function/tool when you need to save a report to a file. """

    folder_path = Path("reports")
    folder_path.mkdir(parents=True, exist_ok=True)

    valid_filename = filename.replace(" ", "_").replace("/", "_").replace("\\", "_")

    for ext in [".output", ".txt", ".doc", ".pdf"]:
        if valid_filename.endswith(ext):
            valid_filename = valid_filename.removesuffix(ext)

    file_path = folder_path / f"{valid_filename}.txt"
    try:
        with open(file_path, "w") as f:
            f.write(content)
    except PermissionError:
        return "Error: Permission denied. Please check the file permissions and try again."
    except OSError:
        return "Error: Could not save the report. Please check the filename and try again."
    return f"Report saved to {file_path.name}"
