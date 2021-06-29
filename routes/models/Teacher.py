from shared import db
import uuid
from .GUID import GUID

class Teacher(db.Model):
    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    disabled = db.Column(db.Boolean, nullable=False, default=False)
    grades = db.relationship('Grade', backref='teacher_info')
    course = db.relationship('Course', backref='teacher_info')

    def __repr__(self):
        return f"{self.id} - {self.name} {self.surname}"