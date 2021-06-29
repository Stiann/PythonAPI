from flask import Blueprint, request
from shared import db
import bcrypt
import jwt
from .models.Student import Student
from .models.Teacher import Teacher
from .models.Course import Course

account_types = ['teacher', 'student']

accountroute_blueprint = Blueprint('accountroute_blueprint', __name__)

@accountroute_blueprint.route('/login', methods=['POST'])
def login():
    
    try:
        if len(request.json['username']) > 16:
            return {'message': 'Username must be less or equal than 16 characters'}, 400
    except:
        return {"message": "JSON requires to have username"}, 400
    
    try:
        if len(request.json['password']) < 8:
            return {'message': "password must be at least 8 characters"}, 400
    except:
        return {"message": "JSON requires to have password"}, 400
    
    teacher = Teacher.query.filter_by(username=request.json['username']).first()
    
    if teacher is None:
        student = Student.query.filter_by(username=request.json['username']).first()
        
        if student is None:
            return {'message': 'Username or password are wrong, login failed'}, 400
        # continue with student
        if bcrypt.checkpw(request.json['password'].encode('utf-8'), student.password):
            token = jwt.encode({"name": student.name}, "something", algorithm="HS256")
            print(student)
            return {"token": token, 
                    "id": student.id, 
                    "username": student.username, 
                    "name": student.name,
                    "surname": student.surname,
                    "type": "student"}
        return {'message': 'Username or password are wrong, login failed'}, 400
    # continue with teacher
    if teacher.disabled is True:
        return {"message": "Teacher is disabled, login failed"}, 400
    
    if bcrypt.checkpw(request.json['password'].encode('utf-8'), teacher.password):
        token = jwt.encode({"name": teacher.name}, "something", algorithm="HS256")
        return {"token": token, 
                "id": teacher.id, 
                "username": teacher.username, 
                "name": teacher.name,
                "surname": teacher.surname,
                "type": "teacher"}
    return {'message': 'Username or password are wrong, login failed'}, 400
        
@accountroute_blueprint.route('/register', methods=['POST'])
def register():
    
    try:    
        if len(request.json['username']) > 16:
            return {'message': 'Username must be less or equal than 16 characters'}, 400
    except:
        return {"message": "JSON requires to have username"}, 400
    
    try:
        if len(request.json['password']) < 8:
            return {'message': "password must be at least 8 characters"}, 400
    except:
        return {"message": "JSON requires to have password"}, 400
        
    try:
	    if len(request.json['name']) > 30:
	        return {"message": "name cannot be longer than 30 characters"}, 400
    except:
    	return {"message": "JSON requires to have name"}, 400
    
    try:
        if len(request.json['surname']) > 30:
            return {"message": "surname cannot be longer than 30 characters"}, 400
    except:
        return {"message": "JSON requires to have surname"}, 400

    try:
        if request.json['type'] not in account_types:
            return {'message': 'account type not valid'}, 400
    except:
        return {"message": "JSON requires to have type"}, 400
    
    try:
        if request.json['type'] == 'student':
            course = Course.query.get(request.json['course'])
            if course is None:
                return {"message": "course with that ID does not exist"}, 404
            if course.disabled is True:
                return {"message": "course disabled, no more students can be assigned to this course"}
    except:
    	return {"message": "JSON requires to have course"}, 400
    
    hashed_password = bcrypt.hashpw(request.json['password'].encode("utf-8"), bcrypt.gensalt())
    
    if request.json['type'] == "teacher":
        if Teacher.query.filter_by(username=request.json['username']).first() is None:
                
            new_teacher = Teacher(username=request.json['username'],
                                  password=hashed_password,
                                  name=request.json['name'],
                                  surname=request.json['surname'])
            db.session.add(new_teacher)
            db.session.commit()
            teacher_created = Teacher.query.filter_by(username=request.json['username'],password=hashed_password).first()
            return {"id": teacher_created.id,
                    "username": teacher_created.username,
                    "password": teacher_created.password.decode('utf-8'),
                    "name": teacher_created.name, 
                    "surname": teacher_created.surname}, 201
        else:
            return {'message': 'username is taken'}, 400
    
    if request.json['type'] == "student":
        if Student.query.filter_by(username=request.json['username'],password=hashed_password).first() is None:
            course = Course.query.get(request.json['course'])
            new_student = Student(username=request.json['username'],
                                  password=hashed_password,
                                  name=request.json['name'],
                                  surname=request.json['surname'])
            db.session.add(new_student)
            # commit before appending cause UUID is not yet created
            db.session.commit()
            student_added = Student.query.filter_by(username=request.json['username'],password=hashed_password).first()
            course.students.append(student_added)
            db.session.commit()
            student_created = Student.query.filter_by(username=request.json['username'],password=hashed_password).first()
            return {"id": student_created.id,
                    "username": student_created.username,
                    "password": student_created.password.decode('utf-8'),
                    "name": student_created.name, 
                    "surname": student_created.surname}, 201
        else:
            return {'message': 'username is taken'}, 400
    