from flask import Blueprint, request
from shared import db
from .models.Student import Student

studentsroute_blueprint = Blueprint('studentsroute_blueprint', __name__)


@studentsroute_blueprint.route('/students', methods=['GET'])
def get_students():
	students = Student.query.all()
	output = []
	# serializing
	for student in students:
		student_data = {"id": student.id, 
                  		"name": student.name, 
                    	"surname": student.surname, 
                     	"course": student.course}
		output.append(student_data)
	return {"students": output}


@studentsroute_blueprint.route('/students/<id>', methods=['GET'])
def get_student(id):
	student = Student.query.get(id)
	if student is None:
		return {"message": "Not Found"}, 404
	return {"id": student.id, 
         	"name": student.name, 
			"surname": student.surname, 
			"course": student.course}


@studentsroute_blueprint.route('/students', methods=['POST'])
def post_student():
    
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
    
	student = Student(name=request.json['name'], 
					  surname=request.json['surname'], 
					  course=request.json['course'])
	db.session.add(student)
	db.session.commit()
	return {"id": student.id, 
			"name": student.name, 
			"surname": student.surname,
			"course": student.course}, 201


@studentsroute_blueprint.route('/students/<id>', methods=['PUT'])
def put_student(id):
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
	    if len(request.json['course']) > 30:
	        return {"message": "course cannot be longer than 30 characters"}, 400
	    student.course = request.json['course']
	except:
	    return {"message": "JSON requires to have course"}, 400

	
	db.session.commit()
	return {"id": student.id, 
         	"name": student.name, 
          	"surname": student.surname, 
           	"course": student.course}


@studentsroute_blueprint.route('/students/<id>', methods={'DELETE'})
def delete_student(id):
	student = Student.query.get(id)
	if student is None:
		return {"message": "Student not Found"}, 404
	db.session.delete(student)
	db.session.commit()
	return {"message": "Student deleted successfully"}, 204

