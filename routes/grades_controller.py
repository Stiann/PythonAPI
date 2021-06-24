from flask import Blueprint, request
from shared import db
from .models.Grade import Grade
from .models.Student import Student
from .models.Teacher import Teacher

gradesroute_blueprint = Blueprint('gradesroute_blueprint', __name__)


@gradesroute_blueprint.route('/grades', methods=['GET'])
def get_grades():
    grades = Grade.query.all()
    output = []
	# serializing
    for grade in grades:
        student = Student.query.get(grade.id_student)
        student_data = {"id": student.id,
                "name": student.name,
                "surname": student.surname,
                "course": student.course}
    
        teacher = Teacher.query.get(grade.id_teacher)
        teacher_data = {"id": teacher.id, 
                    "name": teacher.name, 
                    "surname": teacher.surname, 
                    "course": teacher.course}
        
        grade_data = {"id": grade.id,
                      "id_student": student_data,
                      "id_teacher": teacher_data,
                      "course": grade.course,
                      "grade": grade.grade}
        output.append(grade_data)
        
    return {"grades": output}


@gradesroute_blueprint.route('/grades/<id>', methods=['GET'])
def get_grade(id):
    grade = Grade.query.get(id)
    if grade is None:
	    return {"message": "Not Found"}, 404
    
    student = Student.query.get(grade.id_student)
    student_data = {"id": student.id,
                    "name": student.name,
                    "surname": student.surname,
                    "course": student.course}
    
    teacher = Teacher.query.get(grade.id_teacher)
    teacher_data = {"id": teacher.id, 
                    "name": teacher.name, 
                    "surname": teacher.surname, 
                    "course": teacher.course}
    
    return {"id": grade.id,
            "id_student": student_data,
            "id_teacher": teacher_data,
            "course": grade.course,
            "grade": grade.grade}


@gradesroute_blueprint.route('/grades', methods=['POST'])
def post_grade():
    
    student = Student.query.get(request.json['id_student'])
    
    if student is None:
        return {"message": "Student with that ID does not exist"}, 400
    
    teacher = Teacher.query.get(request.json['id_teacher'])
    
    if teacher is None:
        return {"message": "Teacher with that ID does not exist"}, 400
    
    # TODO check is course exists
    
    if len(request.json['course']) > 30:
        return {"message": "course cannot be longer than 30 characters"}, 400
    
    if request.json['grade'] > 10 or request.json['grade'] <= 0:
        return {"message": "grades cannot be bigger than 10 and less or equal than 0"}, 400
    
    grade = Grade(id_student=request.json['id_student'], 
                  id_teacher=request.json['id_teacher'], 
                  course=request.json['course'],
                  grade=request.json['grade'])
    db.session.add(grade)
    db.session.commit()
    
    student_data = {"id": student.id,
                    "name": student.name,
                    "surname": student.surname,
                    "course": student.course}
    
    teacher_data = {"id": teacher.id, 
                    "name": teacher.name, 
                    "surname": teacher.surname, 
                    "course": teacher.course}
    
    return {"id": grade.id, 
            "student": student_data, 
            "teacher": teacher_data, 
            "course": grade.course, 
            "grade": grade.grade}, 201


@gradesroute_blueprint.route('/grades/<id>', methods=['PUT'])
def put_grade(id):
    grade = Grade.query.get(id)
    if grade is None:
        return {"message": "Grade not Found"}, 404
    try:
        student = Student.query.get(request.json['id_student'])
        if student is None:
            return {"message": "Student with that ID does not exist"}, 400
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
        return {"message": "JSON requires to have course"}, 400
    
    db.session.commit()
    
    return {"id": grade.id, 
            "id_student": grade.id_student, 
            "id_teacher": grade.id_teacher, 
            "course": grade.course, 
            "grade": grade.grade}


@gradesroute_blueprint.route('/grades/<id>', methods={'DELETE'})
def delete_grade(id):
	grade = Grade.query.get(id)
	if grade is None:
		return {"message": "grade not Found"}, 404
	db.session.delete(grade)
	db.session.commit()
	return {"message": "grade deleted successfully"}, 204

