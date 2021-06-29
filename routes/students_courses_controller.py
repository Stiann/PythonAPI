from flask import Blueprint, request
from shared import db
from .models.Student import Student
from .models.Course import Course
from .models.students_courses import association_table

associationroute_blueprint = Blueprint('associationroute_blueprint', __name__)

@associationroute_blueprint.route('/students11/of/<course_id>')
def students_of(course_id):
    course = Course.query.get(course_id)
    
    if course is None:
        return {"message": "student id is not valid"}
    output = []
    for student in course.student_info:
        thestudent = Student.query.get(student.id)
        thestudent_info = {
            "id": thestudent.id,
            "username": thestudent.username,
            "name": thestudent.name,
            "surname": thestudent.surname
        }
        output.append(thestudent_info)
    return {"students": output}

@associationroute_blueprint.route('/courses11/of/<student_id>')
def courses_of(student_id):
    student = Student.query.get(student_id)
    
    if student is None:
        return {"message": "student id is not valid"}
    courses = []
    for course in student.course_info:
        thecourse = Course.query.get(course.id)
        thestudent_info = {
            "id": thecourse.id,
            "name": thecourse.name
        }
        courses.append(thestudent_info)
    return {"courses": courses}
            