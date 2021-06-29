from shared import db
import uuid
from .GUID import GUID

class Grade(db.Model):
    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    student = db.Column(db.Integer, db.ForeignKey('student.id'))
    teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    grade = db.Column(db.String, nullable=False)
    # student_grades
    # teacher_info
    
    def __repr__(self):
        return f"{self.grade}"