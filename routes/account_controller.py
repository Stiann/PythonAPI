from flask import Blueprint, request
from shared import db
import bcrypt
import datetime
import jwt
from .models.Student import Student
from .models.Teacher import Teacher

account_types = ['teacher', 'student']

accountroute_blueprint = Blueprint('accountroute_blueprint', __name__)

@accountroute_blueprint.route('/login', methods=['POST'])
def login():
    
    try:
        if len(request.json['username']) > 16:
            return {'message': 'Username must be less or equal than 16 characters'}, 400
    except:
        return {"message": "JSON requires to have username"}
    
    try:
        if len(request.json['password']) < 8:
            return {'message': "password must be at least 8 characters"}
    except:
        return {"message": "JSON requires to have password"}, 400
    
    teacher = Teacher.query.filter_by(username=request.json['username']).first()
    
    if teacher is None:
        student = Student.query.filter_by(username=request.json['username']).first()
        
        if student is None:
            return {'message': 'Username or password are wrong, login failed'}, 400
        # continue with student
        if bcrypt.checkpw(request.json['password'].encode('utf-8'), student.password):
            token = jwt.encode({"user_id": student.id, "name": student.name}, "something", algorithm="HS256")
            return {"token": token}
    # continue with teacher
    if bcrypt.checkpw(request.json['password'].encode('utf-8'), teacher.password):
            token = jwt.encode({"user_id": teacher.id, "name": teacher.name}, "something", algorithm="HS256")
            return {"token": token.decode('UTF-8')}
        
@accountroute_blueprint.route('/register', methods=['POST'])
def register():
    
    try:    
        if len(request.json['username']) > 16:
            return {'message': 'Username must be less or equal than 16 characters'}, 400
    except:
        return {"message": "JSON requires to have username"}
    
    try:
        if len(request.json['password']) < 8:
            return {'message': "password must be at least 8 characters"}
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
        if len(request.json['course']) > 30:
        	return {"message": "course cannot be longer than 30 characters"}, 400
    except:
    	return {"message": "JSON requires to have course"}, 400
    
    try:
        if request.json['type'] not in account_types:
            return {'message': 'account type not valid'}
    except:
        return {"message": "JSON requires to have type"}
    
    hashed_password = bcrypt.hashpw(request.json['password'].encode("utf-8"), bcrypt.gensalt())
    
    if request.json['type'] == "teacher":
        if Teacher.query.filter_by(username=request.json['username']).first() is None:
                
            new_teacher = Teacher(username=request.json['username'],
                                  password=hashed_password,
                                  name=request.json['name'],
                                  surname=request.json['surname'],
                                  course=request.json['course'])
            db.session.add(new_teacher)
            db.session.commit()
            teacher_created = Teacher.query.filter_by(username=request.json['username']).first()
            return {"id": teacher_created.id,
                    "username": teacher_created.username,
                    "password": teacher_created.password.decode('utf-8'),
                    "name": teacher_created.name, 
                    "surname": teacher_created.surname, 
                    "course": teacher_created.course}, 201
        else:
            return {'message': 'username is taken'}, 400
    
    if request.json['type'] == "student":
        if Student.query.filter_by(username=request.json['username']).first() is None:
                
            new_student = Student(username=request.json['username'],
                                  password=hashed_password.decode('utf-8'),
                                  name=request.json['name'],
                                  surname=request.json['surname'],
                                  course=request.json['course'])
            db.session.add(new_student)
            db.session.commit()
            student_created = Student.query.filter_by(username=request.json['username']).first()
            return {"id": student_created.id,
                    "username": student_created.username,
                    "password": student_created.password,
                    "name": student_created.name, 
                    "surname": student_created.surname, 
                    "course": student_created.course}, 201
        else:
            return {'message': 'username is taken'}, 400
    