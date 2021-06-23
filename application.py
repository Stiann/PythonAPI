from flask import Flask
from shared import db
from routes.students_controller import studentsroute_blueprint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(studentsroute_blueprint)

#with app.app_context():
#    db.create_all()

if __name__ == '__main__':
	app.run(debug=True)