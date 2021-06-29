from flask import Flask
from shared import db
from routes.students_controller import studentsroute_blueprint
from routes.teacher_controller import teachersroute_blueprint
from routes.grades_controller import gradesroute_blueprint
from routes.account_controller import accountroute_blueprint
from routes.courses_controller import coursesroute_blueprint
from routes.students_courses_controller import associationroute_blueprint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(studentsroute_blueprint)
app.register_blueprint(teachersroute_blueprint)
app.register_blueprint(gradesroute_blueprint)
app.register_blueprint(accountroute_blueprint)
app.register_blueprint(coursesroute_blueprint)
app.register_blueprint(associationroute_blueprint)

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
	app.run(debug=True)