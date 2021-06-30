from flask import Blueprint, request
from shared import db
from .models.Student import Student
from .models.Course import Course

studentsroute_blueprint = Blueprint('studentsroute_blueprint', __name__)


@studentsroute_blueprint.route('/students', methods=['GET'])
def get_students():
	students = Student.query.all()
	output = []
	# serializing
	for student in students:
		courses = []
		for course in student.course_info:
			thecourse = Course.query.get(course.id)
			thecourse_info = {
				"id": thecourse.id,
				"name": thecourse.name
			}
		courses.append(thecourse_info)
		student_data = {"id": student.id,
						"username": student.username,
                  		"name": student.name, 
                    	"surname": student.surname,
                     	"courses": courses}
		output.append(student_data)
	return {"students": output}


@studentsroute_blueprint.route('/students/<id>', methods=['GET'])
def get_student(id):
	student = Student.query.get(id)
	if student is None:
		return {"message": "Not Found"}, 404
	courses = []
	for course in student.course_info:
		thecourse = Course.query.get(course.id)
		thecourse_info = {
			"id": thecourse.id,
			"name": thecourse.name
		}
	courses.append(thecourse_info)
	return {"id": student.id, 
	   		"username": student.username,
         	"name": student.name, 
			"surname": student.surname, 
			"courses": courses}


@studentsroute_blueprint.route('/students/<id>', methods=['PUT'])
def put_student(id):
	if len(id) != 36:
	    return {"message": "ID is not valid"}
    
	student = Student.query.get(id)
	if student is None:
		return {"message": "Not Found"}, 404

	try:
	    if len(request.json['name']) > 30:
	        return {"message": "name cannot be longer than 30 characters"}, 400
	    student.name = request.json['name']
	except:
	    return {"message": "JSON requires to have name"}, 400

	try:
	    if len(request.json['surname']) > 30:
	        return {"message": "surname cannot be longer than 30 characters"}, 400
	    student.surname = request.json['surname']
	except:
	    return {"message": "JSON requires to have surname"}, 400
	
	try:
	    if len(request.json['username']) > 16:
	        return {"message": "username cannot be longer than 16 characters"}, 400
	    student.username = request.json['username']
	except:
	    return {"message": "JSON requires to have username"}, 400
     
	db.session.commit()
	return {"id": student.id, 
			"username":student.username,
         	"name": student.name, 
          	"surname": student.surname}


@studentsroute_blueprint.route('/students/<id>', methods={'DELETE'})
def delete_student(id):
	try:
		if len(id) != 36:
			return {"message": "ID is not valid"}
		if request.json['confirm'] == True:
			student = Student.query.get(id)
			if student is None:
				return {"message": "Student not Found"}, 404
			student.disabled = True
			db.session.commit()
			return {"message": "Student deleted successfully"}, 204
		else:
			return {"message": "Confirmation needed"}, 400
	except:
		return {"message": "Confirmation needed"}, 400

