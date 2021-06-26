from shared import db

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    course = db.Column(db.String(30), nullable=False)
    grades = db.relationship('Grade', backref='teacher')

    def __repr__(self):
        return f"{self.id} - {self.name} {self.surname}"