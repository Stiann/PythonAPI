from flask import Blueprint, request
from shared import db
from .models.Grade import Grade
from .models.Student import Student
from .models.Teacher import Teacher
from .models.Course import Course

gradesroute_blueprint = Blueprint('gradesroute_blueprint', __name__)


@gradesroute_blueprint.route('/grades', methods=['GET'])
def get_grades():
    grades = Grade.query.all()
    output = []
	# serializing
    for grade in grades:
        student = Student.query.get(grade.student)
        student_data = {"id": student.id,
                "name": student.name,
                "surname": student.surname}
    
        teacher = Teacher.query.get(grade.teacher)
        teacher_data = {"id": teacher.id, 
                    "name": teacher.name, 
                    "surname": teacher.surname}
        
        course = Course.query.get(grade.course)
        
        course_data = {"id": course.id,
                       "name": course.name}
        
        grade_data = {"id": grade.id,
                      "id_student": student_data,
                      "id_teacher": teacher_data,
                      "course": course_data,
                      "grade": grade.grade}
        output.append(grade_data)
        
    return {"grades": output}


@gradesroute_blueprint.route('/grades/<id>', methods=['GET'])
def get_grade(id):
    if len(id) != 36:
        return {"message": "ID not valid"}
    grade = Grade.query.get(id)
    if grade is None:
	    return {"message": "Not Found"}, 404
    
    student = Student.query.get(grade.student)
    student_data = {"id": student.id,
                    "username": student.username,
                    "name": student.name,
                    "surname": student.surname}
    
    course = Course.query.get(grade.course)
        
    course_data = {"id": course.id,
                   "name": course.name}
    
    teacher = Teacher.query.get(grade.teacher)
    teacher_data = {"id": teacher.id, 
                    "username": teacher.username,
                    "name": teacher.name, 
                    "surname": teacher.surname}
    
    return {"id": grade.id,
            "id_student": student_data,
            "id_teacher": teacher_data,
            "course": course_data,
            "grade": grade.grade}


@gradesroute_blueprint.route('/grades', methods=['POST'])
def post_grade():
    try:
        if len(request.json['student']) != 36:
            return {"message": "ID not valid"}, 400
        student = Student.query.get(request.json['student'])
        if student is None:
            return {"message": "Student with that ID does not exist"}, 400
        if student.disabled is True:
            return {"message": "Student is disabled"}, 400
    except:
        return {"message": "JSON requires student"}
    
    try:
        if len(request.json['teacher']) != 36:
            return {"message": "ID not valid"}, 400
        teacher = Teacher.query.get(request.json['teacher'])
        if teacher is None:
            return {"message": "Teacher with that ID does not exist"}, 400
    except:
        return {"message": "JSON requires teacher"}
    
    try:
        if len(request.json['course']) != 36:
            return {"message": "ID not valid"}, 400
        course = Course.query.get(request.json['course'])
        if course is None:
            return {"message": "Course with that ID doe no exist"}, 400
    except:
        return {"message": "JSON requires course"}
    try:
        if request.json['grade'] > 10 or request.json['grade'] <= 0:
            return {"message": "Grades cannot be bigger than 10 and less or equal than 0"}, 400
    except:
        return {"message": "JSON requires grade"}
    
    grade = Grade(student=request.json['student'], 
                  teacher=request.json['teacher'],
                  course=request.json['course'],
                  grade=request.json['grade'])
    db.session.add(grade)
    db.session.commit()
    course_data = {"id": course.id,
                   "name": course.name
                   }
    student_data = {"id": student.id,
                    "name": student.name,
                    "surname": student.surname}
    
    teacher_data = {"id": teacher.id, 
                    "name": teacher.name, 
                    "surname": teacher.surname}
    
    return {"id": grade.id, 
            "student": student_data, 
            "teacher": teacher_data,
            "course": course_data,
            "grade": grade.grade}, 201


@gradesroute_blueprint.route('/grades/<id>', methods=['PUT'])
def put_grade(id):
    if len(id) != 36:
    	return {"message": "ID is not valid"}
    
    grade = Grade.query.get(id)
    
    if grade is None:
        return {"message": "Grade not Found"}, 404
    
    try:
        course = Course.query.get(request.json['course'])
        if course is None:
            return {"message": "course with that ID does not exist"}, 400
        grade.course = request.json['course']
    except:
        return {"message": "JSON must contain course"}, 400
    
    try:
        student = Student.query.get(request.json['id_student'])
        if student is None:
            return {"message": "Student with that ID does not exist"}, 400
        if student.disabled is True:
            return {"message": "Student is disabled"}, 400
        grade.id_student = request.json['id_student']
    except:
        return {"message": "JSON must containt id_student"}, 400
    
    try:
        teacher = Teacher.query.get(request.json['id_teacher'])
        if teacher is None:
            return {"message": "Teacher with that ID does not exist"}, 400
        grade.id_teacher = request.json['id_teacher']
    except:
        return {"message": "JSON must containt id_teacher"}, 400
    
    try:
        if request.json['grade'] > 10 or request.json['grade'] <= 0:
            return {"message": "grades cannot be bigger than 10 and less or equal than 0"}, 400
        grade.grade = request.json['grade']
    except:
        return {"message": "JSON requires to have grade"}, 400
    
    db.session.commit()
    
    course_data = {"id": course.id,
                   "name": course.name
                   }
    student_data = {"id": student.id,
                    "name": student.name,
                    "surname": student.surname}
    
    teacher_data = {"id": teacher.id, 
                    "name": teacher.name, 
                    "surname": teacher.surname}
    
    return {"id": grade.id, 
            "student": student_data, 
            "teacher": teacher_data, 
            "course": course_data, 
            "grade": grade.grade}


@gradesroute_blueprint.route('/grades/<id>', methods={'DELETE'})
def delete_grade(id):
    try:
        if request.json['confirm'] == True:
            grade = Grade.query.get(id)
            if grade is None:
                return {"message": "Grade not found"}, 404
            
            db.session.delete(grade)
            db.session.commit()
            return {"message": "Grade successfully deleted"}, 200
        else:
            return {"message": "Confirmation needed"}, 400
    except:
        return {"message": "Confirmation needed"}, 400
	

