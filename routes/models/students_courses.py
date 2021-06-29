from shared import db 
import uuid
from .GUID import GUID

association_table = db.Table('students_courses',
    db.Column('id', GUID(), primary_key=True, default=lambda: str(uuid.uuid4())),
    db.Column('student_id', GUID(), db.ForeignKey('student.id')),
    db.Column('course_id', GUID(), db.ForeignKey('course.id'))
    )