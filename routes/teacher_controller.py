from flask import Blueprint, request
from shared import db
from .models.Teacher import Teacher

teachersroute_blueprint = Blueprint('teachersroute_blueprint', __name__)


@teachersroute_blueprint.route('/teachers', methods=['GET'])
def get_teachers():
	teachers = Teacher.query.all()
	output = []
	# serializing
	for teacher in teachers:
		teacher_data = {"id": teacher.id, 
                        "name": teacher.name, 
                        "surname": teacher.surname, 
                        "course": teacher.course}
		output.append(teacher_data)
	return {"teachers": output}


@teachersroute_blueprint.route('/teachers/<id>', methods=['GET'])
def get_teacher(id):
	teacher = Teacher.query.get(id)
	if teacher is None:
		return {"message": "Not Found"}, 404
	return {"id": teacher.id, 
            "name": teacher.name, 
            "surname": teacher.surname, 
            "course": teacher.course}


@teachersroute_blueprint.route('/teachers', methods=['POST'])
def post_teacher():
    
    try:
	    if request.json['name'].length > 30:
	        return {"message": "name cannot be longer than 30 characters"}, 400
    except:
	    return {"message": "JSON requires to have name"}, 400

    try:
	    if request.json['surname'].length > 30:
	        return {"message": "surname cannot be longer than 30 characters"}, 400
    except:
	    return {"message": "JSON requires to have surname"}, 400

    try:
	    if request.json['course'].length > 30:
	    	return {"message": "course cannot be longer than 30 characters"}, 400
    except:
	    return {"message": "JSON requires to have course"}, 400
    
    teacher = Teacher(name=request.json['name'], 
                      surname=request.json['surname'], 
                      course=request.json['course'])
    
    db.session.add(teacher)
    db.session.commit()
    
    return {"id": teacher.id, 
            "name": teacher.name, 
            "surname": teacher.surname, 
            "course": teacher.course}, 201


@teachersroute_blueprint.route('/teachers/<id>', methods=['PUT'])
def put_teacher(id):
	teacher = Teacher.query.get(id)
	if teacher is None:
		return {"message": "Not Found"}, 404

	try:
	    if len(request.json['name']) > 30:
	        return {"message": "name cannot be longer than 30 characters"}, 400
	    teacher.name = request.json['name']
	except:
	    return {"message": "JSON requires to have name"}, 400

	try:
	    if len(request.json['surname']) > 30:
	        return {"message": "surname cannot be longer than 30 characters"}, 400
	    teacher.surname = request.json['surname']
	except:
	    return {"message": "JSON requires to have surname"}, 400
 
	try:
	    if len(request.json['course']) > 30:
	        return {"message": "course cannot be longer than 30 characters"}, 400
	    teacher.course = request.json['course']
	except:
	    return {"message": "JSON requires to have course"}, 400

	db.session.commit()
 
	return {"id": teacher.id, 
            "name": teacher.name, 
            "surname": teacher.surname, 
            "course": teacher.course}


@teachersroute_blueprint.route('/teachers/<id>', methods={'DELETE'})
def delete_teacher(id):
	teacher = Teacher.query.get(id)
	if teacher is None:
		return {"message": "Teacher not Found"}, 404
	db.session.delete(teacher)
	db.session.commit()
	return {"message": "Teacher deleted successfully"}, 204

