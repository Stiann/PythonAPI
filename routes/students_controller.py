from flask import Blueprint, request
from shared import db
from .models.Student import Student

studentsroute_blueprint = Blueprint('studentsroute_blueprint', __name__)


@studentsroute_blueprint.route('/students')
def get_students():
	students = Student.query.all()
	output = []
	# serializing
	for student in students:
		student_data = {"id": student.id, "name": student.name, "surname": student.surname, "course": student.course}
		output.append(student_data)
	return {"students": output}


@studentsroute_blueprint.route('/students/<id>')
def get_student(id):
	student = Student.query.get(id)
	if student is None:
		return {"message": "Not Found"}, 404
	return {"id": student.id, "name": student.name, "surname": student.surname, "course": student.course}


@studentsroute_blueprint.route('/students', methods=['POST'])
def post_student():
	student = Student(name=request.json['name'], surname=request.json['surname'], course=request.json['course'])
	db.session.add(student)
	db.session.commit()
	return {"id": student.id, "name": student.name, "surname": student.surname, "course": student.course}, 201


@studentsroute_blueprint.route('/students/<id>', methods=['PUT'])
def put_student(id):
	student = Student.query.get(id)
	if student is None:
		return {"message": "Not Found"}, 404
	try:
		student.name = request.json['name']
		student.surname = request.json['surname']
		student.course = request.json['course']
	except:
		return {"message": "JSON payload requires all data"}
	db.session.commit()
	return {"id": student.id, "name": student.name, "surname": student.surname, "course": student.course}


@studentsroute_blueprint.route('/students/<id>', methods={'DELETE'})
def delete_student(id):
	student = Student.query.get(id)
	if student is None:
		return {"message": "Student not Found"}, 404
	db.session.delete(student)
	db.session.commit()
	return {"message": "Studente deleted successfully"}, 204

