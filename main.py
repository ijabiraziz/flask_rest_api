from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# Init db
db = SQLAlchemy(app)
# Init ma                           
ma = Marshmallow(app)


class Student(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    field = db.Column(db.String(50))
    gpa = db.Column(db.Float(200))

    def __init__(self, name, email, field, gpa):
        self.name = name
        self.email = email
        self.field = field
        self.gpa = gpa

# Serialize or DeSerialize model fields
class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'field', 'gpa')


# For single student record
student_schema = StudentSchema()
# For multiple students record
students_schema = StudentSchema(many=True)


# Add New Student
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.json['name']
    email = request.json['email']
    field = request.json['field']
    gpa = request.json['gpa']

    new_student = Student(name, email, field, gpa)
    db.session.add(new_student)
    db.session.commit()

    return student_schema.jsonify(new_student)


# List all Students
@app.route('/all_student', methods=['GET'])
def all_student():
    all_students = Student.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result)


# Get Single Student
@app.route('/a_student/<id>', methods=['GET'])
def single_student(id):
    a_student = Student.query.get(id)
    return student_schema.jsonify(a_student)


# Update/Edit Student
@app.route('/edit_student/<id>', methods=['PUT'])
def update_student(id):
    a_student = Student.query.get(id)

    name = request.json['name']
    email = request.json['email']
    field = request.json['field']
    gpa = request.json['gpa']

    a_student.name = name
    a_student.email = email
    a_student.field = field
    a_student.gpa = gpa

    db.session.commit()

    return student_schema.jsonify(a_student)


# Delete Student
@app.route('/del_student/<id>', methods=['DELETE'])
def delete_student(id):
    get_student = Student.query.get(id)
    db.session.delete(get_student)
    db.session.commit()

    return student_schema.jsonify(get_student)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
