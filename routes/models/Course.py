from shared import db
from .students_courses import association_table
import uuid
from .GUID import GUID

class Course(db.Model):
    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String, nullable=False)
    teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    disabled = db.Column(db.Boolean, nullable=False, default=False)
    students = db.relationship('Student', secondary=association_table, backref='course_info')
    # student_info
    # teacher_info
    
    def __repr__(self):
        return f"{self.id} - {self.name}"