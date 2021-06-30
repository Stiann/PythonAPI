from flask import Blueprint, request
from shared import db
from .models.Teacher import Teacher
from .models.Course import Course
from .models.Student import Student

coursesroute_blueprint = Blueprint('coursesroute_blueprint', __name__)


@coursesroute_blueprint.route('/courses', methods=['GET'])
def get_course():
    courses = Course.query.all()
    output = []
	# serializing
    for course in courses:
        teacher = Teacher.query.get(course.teacher)
        teacher_data = {"id": teacher.id,
                        "username": teacher.username, 
                        "name": teacher.name, 
                        "surname": teacher.surname}
        students = []
        for student in course.student_info:
            thestudent = Student.query.get(student.id)
            student_data = {"id": thestudent.id,
                            "username": thestudent.username,
                            "name": thestudent.name,
                            "surname": thestudent.surname}
            students.append(student_data)
        course_data = {"id": course.id,
                       "name": course.name,
                       "teacher": teacher_data,
                       "students": students}
        
        output.append(course_data)
    return {"courses": output}


@coursesroute_blueprint.route('/courses/<id>', methods=['GET'])
def get_course_all(id):
    if len(id) != 36:
        return {"message": "ID not valid"}
    
    course = Course.query.get(id)
    if course is None:
	    return {"message": "Not Found"}, 404
        
    teacher = Teacher.query.get(course.teacher)
    teacher_data = {"id": teacher.id, 
                    "username": teacher.username,
                    "name": teacher.name,
                    "surname": teacher.surname}
    students = []
    for student in course.student_info:
        thestudent = Student.query.get(student.id)
        thestudent_info = {
            "id": thestudent.id,
            "username": thestudent.username,
            "name": thestudent.name,
            "surname": thestudent.surname
        }
        students.append(thestudent_info)
        
    return {"id": course.id,
            "name": course.name,
            "teacher": teacher_data,
            "students": students}


@coursesroute_blueprint.route('/courses', methods=['POST'])
def post_course():
    
    try:
        if len(request.json['name']) > 30:
            return {"message": "name cannot be longer than 30 characters"}, 400
    except:
        return {"message": "JSON requires name"}, 400
    try:
        if len(request.json['teacher']) != 36:
            return {"message": "ID is not valid"}
        teacher = Teacher.query.get(request.json['teacher'])
        if teacher is None:
            return {"message": "teacher not found"}, 404
    except:
        return {"message": "JSON requires teacher"}, 400
    
    course = Course(name=request.json['name'], 
                  teacher=request.json['teacher'])
    db.session.add(course)
    db.session.commit()
    
    
    teacher_data = {"id": teacher.id,
                    "username": teacher.username, 
                    "name": teacher.name, 
                    "surname": teacher.surname}
    
    return {"id": course.id, 
            "name": course.name, 
            "teacher": teacher_data}, 201


@coursesroute_blueprint.route('/courses/<id>', methods=['PUT'])
def put_course(id):
    
    if len(id) != 36:
        return {"message": "ID not valid"}
    
    course = Course.query.get(id)
    
    if course is None:
        return {"message": "Grade not Found"}, 404
    
    try:
        if len(request.json['name']) > 30:
            return {"message": "name can't be longer than 30 characters"}, 400
        course.name = request.json['name']
    except:
        return {"message": "JSON must contain name"}, 400
    
    try:
        if len(request.json['teacher']) != 36:
            return {"message": "ID not valid"}
        teacher = Teacher.query.get(request.json['teacher'])
        if teacher is None:
            return {"message": "Teacher with that ID does not exist"}, 400
        course.teacher = request.json['teacher']
    except:
        return {"message": "JSON must containt teacher"}, 400
    
    db.session.commit()
    
    teacher_data = {"id": teacher.id,
                    "username": teacher.username, 
                    "name": teacher.name, 
                    "surname": teacher.surname}
    
    return {"id": course.id, 
            "name": course.name, 
            "teacher": teacher_data}


@coursesroute_blueprint.route('/courses/<id>', methods={'DELETE'})
def delete_course(id):
    try:
        if request.json['confirm'] == True:
            course = Course.query.get(id)
            if course is None:
                return {"message": "Course not found"}, 404
            
            course.disabled = True
            db.session.commit()
            return {"message": "course disabled successfully, no more students can be added to this course"}, 200
        
        else:
            return {"message": "Confirmation needed"}, 400
    except:
        return {"message": "Confirmation needed"}, 400
    
    
