from shared import db

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('student.id'))
    id_teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    course = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
 
    def __repr__(self):
        return f"{self.id} - {self.name} {self.surname}"