from shared import db
from .students_courses import association_table
import uuid
from .GUID import GUID

class Student(db.Model):
	id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
	username = db.Column(db.String(16), nullable=False)
	password = db.Column(db.String, nullable=False)
	name = db.Column(db.String(30), nullable=False)
	surname = db.Column(db.String(30), nullable=False)
	disabled = db.Column(db.Boolean, nullable=False, default=False)
	courses = db.relationship('Course', secondary=association_table, backref='student_info')
	grades = db.relationship('Grade', backref='student_grades')
	# course_info

	def __repr__(self):
		return f"{self.id}"
