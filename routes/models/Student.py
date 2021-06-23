from shared import db

class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	surname = db.Column(db.String(30), nullable=False)
	course = db.Column(db.String(30), nullable=False)


	def __repr__(self):
		return f"{self.id} - {self.name} {self.surname}"