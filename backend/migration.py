from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from sqlite3 import dbapi2 as sqlite
from sqlalchemy.exc import IntegrityError
import hashlib
app = Flask(__name__)
# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Set the path to the database file
database_file = os.path.join(current_directory, "iitdatabase.db")

# Configure the Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database_file + "?charset=utf8"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'connect_args': {'detect_types': sqlite.PARSE_DECLTYPES | sqlite.PARSE_COLNAMES}}
app.config['DEBUG'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    
 # Define additional models for courses, course details, exams, exam questions, and question options
class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(255), nullable=False)
    about = db.Column(db.Text)  # Add an 'about' field as a text type
    general_instruction = db.Column(db.Text)  # Add a 'general_instruction' field as a text type
    please_read = db.Column(db.Text)  # Add a 'please_read' field as a text type
    placement_activity = db.Column(db.Text) 



class Exam(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)  # Corrected ForeignKey
    exam_name = db.Column(db.String(255))
    exam_description = db.Column(db.TEXT)
    graded = db.Column(db.Boolean, default=True) 
    week = db.Column(db.Integer, nullable=False)
    course = db.relationship('Course', backref=db.backref('exams', lazy=True))
    exam_end_time = db.Column(db.DateTime)
    demo=db.Column(db.Text) 


class ExamQuestion(db.Model):
    __tablename__ = "exam_questions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    question_text = db.Column(db.TEXT)
    correct_answer_id = db.Column(db.Integer)
    exam = db.relationship('Exam', backref=db.backref('questions', lazy=True))

class QuestionOption(db.Model):
    __tablename__ = "question_options"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('exam_questions.id'), nullable=False)
    option_text = db.Column(db.String(255))
    question = db.relationship('ExamQuestion', backref=db.backref('options', lazy=True))   
    
class UserExam(db.Model):
    __tablename__ = "user_exam"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, nullable=False)

class UserAnswer(db.Model):
    __tablename__ = "user_answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('exam_questions.id'), nullable=False)
    selected_option_id = db.Column(db.Integer, db.ForeignKey('question_options.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)  
    
    
class AssignmentExam(db.Model):
    __tablename__ = "assignment_exams"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)  # Corrected ForeignKey
    exam_name = db.Column(db.String(255))
    exam_description = db.Column(db.TEXT)
    graded = db.Column(db.Boolean, default=True) 
    week = db.Column(db.Integer, nullable=False)
    course = db.relationship('Course', backref=db.backref('assignment_exams', lazy=True))
    exam_end_time = db.Column(db.DateTime)
 


class AssignmentExamQuestion(db.Model):
    __tablename__ = "assignment_exam_questions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('assignment_exams.id'), nullable=False)
    question_text = db.Column(db.TEXT)
    
class AssignmentQuestionOption(db.Model):
    __tablename__ = "assignment_question_options"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('assignment_exam_questions.id'), nullable=False)
    input = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)
    
    
class UserAssignmentAnswer(db.Model):
    __tablename__ = "user_assignment_result"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('assignment_exam_questions.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('assignment_exams.id'), nullable=False)
    result_json = db.Column(db.Text, nullable=False)  
   
    # Function to create the admin user
def create_user():
    admin_username = "ciril@gmail.com"  # Set the admin username
    admin_password = "ciril"  # Set the admin password (you should use a secure password in a production environment)
    admin = User(username=admin_username, password=hashlib.md5(admin_password.encode()).hexdigest())
    db.session.add(admin)
    db.session.commit()
    print("ciril user created successfully.")
    




def insert_courses():
    courses_data = [
        {
            'course_name': 'Software Testing',
            'about': 'This course covers principles and techniques of software testing.',
            'general_instruction': 'Attend all lectures and complete assignments on time.',
            'please_read': 'Please read the course syllabus and recommended textbooks.',
            'placement_activity': 'Students will participate in a final project to apply learned concepts.'
        },
        {
            'course_name': 'Deep Learning',
            'about': 'Explore advanced neural networks and deep learning algorithms.',
            'general_instruction': 'Prepare for intensive hands-on coding sessions.',
            'please_read': 'Please read the prerequisite materials on machine learning.',
            'placement_activity': 'Students will work on real-world deep learning projects.'
        },
        {
            'course_name': 'Software Engineering',
            'about': 'Study software development methodologies and practices.',
            'general_instruction': 'Collaborate with team members on group projects.',
            'please_read': 'Please review the course schedule and project deadlines.',
            'placement_activity': 'Students will present their software projects in the final evaluation.'
        },
        {
            'course_name': 'AI: Search Methods for Problem Solving',
            'about': 'Learn various search algorithms and their applications in AI.',
            'general_instruction': 'Participate actively in discussions and problem-solving sessions.',
            'please_read': 'Please read the recommended papers on search algorithms.',
            'placement_activity': 'Students will implement search algorithms in a programming project.'
        }
    ]

    try:
        for data in courses_data:
            course = Course(**data)
            db.session.add(course)
        db.session.commit()
        print("Courses inserted successfully.")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error inserting courses: {str(e)}")


def insert_exams():
    
    exams_data = [
        {'course_id': 1, 'exam_name': 'Software Testing Exam Week 1', 'week': 1, 'graded': True, 'demo': 'https://www.youtube.com/watch?v=jG5S38teiDg', 'exam_description': 'Week 1 exam for Software Testing covering basic concepts.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 1, 'exam_name': 'Software Testing Exam Week 2', 'week': 2, 'graded': True, 'exam_description': 'Week 2 exam for Software Testing covering advanced topics.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 1, 'exam_name': 'Software Testing Exam Week 3', 'week': 3, 'graded': True, 'exam_description': 'Week 3 exam for Software Testing focusing on practical testing techniques.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 1, 'exam_name': 'Software Testing Exam Week 4', 'week': 4, 'graded': True, 'exam_description': 'Week 4 exam for Software Testing including a comprehensive review.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 2, 'exam_name': 'Deep Learning Exam Week 1', 'week': 1, 'graded': True, 'exam_description': 'Week 1 exam for Deep Learning covering introduction to neural networks.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 2, 'exam_name': 'Deep Learning Exam Week 2', 'week': 2, 'graded': True, 'exam_description': 'Week 2 exam for Deep Learning focusing on deep neural networks.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 2, 'exam_name': 'Deep Learning Exam Week 3', 'week': 3, 'graded': True, 'exam_description': 'Week 3 exam for Deep Learning covering convolutional neural networks.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 2, 'exam_name': 'Deep Learning Exam Week 4', 'week': 4, 'graded': True, 'exam_description': 'Week 4 exam for Deep Learning focusing on recurrent neural networks.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 3, 'exam_name': 'Software Engineering Exam Week 1', 'week': 1, 'graded': True, 'exam_description': 'Week 1 exam for Software Engineering covering software development lifecycle.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 3, 'exam_name': 'Software Engineering Exam Week 2', 'week': 2, 'graded': True, 'exam_description': 'Week 2 exam for Software Engineering focusing on software design principles.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 3, 'exam_name': 'Software Engineering Exam Week 3', 'week': 3, 'graded': True, 'exam_description': 'Week 3 exam for Software Engineering covering software testing methodologies.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 3, 'exam_name': 'Software Engineering Exam Week 4', 'week': 4, 'graded': True, 'exam_description': 'Week 4 exam for Software Engineering including project management techniques.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 4, 'exam_name': 'AI: Search Methods for Problem Solving Exam Week 1', 'week': 1, 'graded': True, 'exam_description': 'Week 1 exam for AI covering basic search algorithms.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 4, 'exam_name': 'AI: Search Methods for Problem Solving Exam Week 2', 'week': 2, 'graded': True, 'exam_description': 'Week 2 exam for AI focusing on heuristic search techniques.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 4, 'exam_name': 'AI: Search Methods for Problem Solving Exam Week 3', 'week': 3, 'graded': True, 'exam_description': 'Week 3 exam for AI covering optimization algorithms.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 4, 'exam_name': 'AI: Search Methods for Problem Solving Exam Week 4', 'week': 4, 'graded': True, 'exam_description': 'Week 4 exam for AI focusing on advanced problem-solving techniques.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 1, 'exam_name': 'Non-Graded Software Testing Exam Week 1', 'week': 1, 'graded': False, 'exam_description': 'Non-graded Week 1 exam for Software Testing.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 1, 'exam_name': 'Non-Graded Software Testing Exam Week 2', 'week': 2, 'graded': False, 'exam_description': 'Non-graded Week 2 exam for Software Testing.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 1, 'exam_name': 'Non-Graded Software Testing Exam Week 3', 'week': 3, 'graded': False, 'exam_description': 'Non-graded Week 3 exam for Software Testing.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 1, 'exam_name': 'Non-Graded Software Testing Exam Week 4', 'week': 4, 'graded': False, 'exam_description': 'Non-graded Week 4 exam for Software Testing.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 2, 'exam_name': 'Non-Graded Deep Learning Exam Week 1', 'week': 1, 'graded': False, 'exam_description': 'Non-graded Week 1 exam for Deep Learning.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 2, 'exam_name': 'Non-Graded Deep Learning Exam Week 2', 'week': 2, 'graded': False, 'exam_description': 'Non-graded Week 2 exam for Deep Learning.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 2, 'exam_name': 'Non-Graded Deep Learning Exam Week 3', 'week': 3, 'graded': False, 'exam_description': 'Non-graded Week 3 exam for Deep Learning.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 2, 'exam_name': 'Non-Graded Deep Learning Exam Week 4', 'week': 4, 'graded': False, 'exam_description': 'Non-graded Week 4 exam for Deep Learning.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 3, 'exam_name': 'Non-Graded Software Engineering Exam Week 1', 'week': 1, 'graded': False, 'exam_description': 'Non-graded Week 1 exam for Software Engineering.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 3, 'exam_name': 'Non-Graded Software Engineering Exam Week 2', 'week': 2, 'graded': False, 'exam_description': 'Non-graded Week 2 exam for Software Engineering.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 3, 'exam_name': 'Non-Graded Software Engineering Exam Week 3', 'week': 3, 'graded': False, 'exam_description': 'Non-graded Week 3 exam for Software Engineering.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 3, 'exam_name': 'Non-Graded Software Engineering Exam Week 4', 'week': 4, 'graded': False, 'exam_description': 'Non-graded Week 4 exam for Software Engineering.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 4, 'exam_name': 'Non-Graded AI: Search Methods for Problem Solving Exam Week 1', 'week': 1, 'graded': False, 'exam_description': 'Non-graded Week 1 exam for AI.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 4, 'exam_name': 'Non-Graded AI: Search Methods for Problem Solving Exam Week 2', 'week': 2, 'graded': False, 'exam_description': 'Non-graded Week 2 exam for AI.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)},
        {'course_id': 4, 'exam_name': 'Non-Graded AI: Search Methods for Problem Solving Exam Week 3', 'week': 3, 'graded': False, 'exam_description': 'Non-graded Week 3 exam for AI.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
        {'course_id': 4, 'exam_name': 'Non-Graded AI: Search Methods for Problem Solving Exam Week 4', 'week': 4, 'graded': False, 'exam_description': 'Non-graded Week 4 exam for AI.', 'exam_end_time': datetime(2024, 8, 18, 23, 59)}
    ]

    try:
        for data in exams_data:
            exam = Exam(**data)
            db.session.add(exam)
        db.session.commit()
        print("Exams inserted successfully.")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error inserting exams: {str(e)}")

def insert_exam_questions():
    
    questions_data = [
        {'exam_id': 1, 'question_text': 'What is Software Testing?', 'correct_answer_id': 2},
        {'exam_id': 1, 'question_text': 'Which tool is used for testing?', 'correct_answer_id': 6},
        {'exam_id': 17, 'question_text': 'What is the purpose of a test case?', 'correct_answer_id': 10},
        {'exam_id': 17, 'question_text': 'Which testing phase comes first?', 'correct_answer_id': 14},
        # Add more questions as needed
    ]

    try:
        for data in questions_data:
            question = ExamQuestion(**data)
            db.session.add(question)
        db.session.commit()
        print("Exam questions inserted successfully.")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error inserting exam questions: {str(e)}")

def insert_question_options():
    
    options_data = [
        # Options for Question 1 of exam 1
        {'question_id': 1, 'option_text': 'Option A for Question 1'},
        {'question_id': 1, 'option_text': 'Option B for Question 1'},
        {'question_id': 1, 'option_text': 'Option C for Question 1'},
        {'question_id': 1, 'option_text': 'Option D for Question 1'},
        
        # Options for Question 2 of exam 1
        {'question_id': 2, 'option_text': 'Option A for Question 2'},
        {'question_id': 2, 'option_text': 'Option B for Question 2'},
        {'question_id': 2, 'option_text': 'Option C for Question 2'},
        {'question_id': 2, 'option_text': 'Option D for Question 2'},
        
        # Options for Question 1 of exam 17
        {'question_id': 3, 'option_text': 'Option A for Question 1 of exam 17'},
        {'question_id': 3, 'option_text': 'Option B for Question 1 of exam 17'},
        {'question_id': 3, 'option_text': 'Option C for Question 1 of exam 17'},
        {'question_id': 3, 'option_text': 'Option D for Question 1 of exam 17'},
        
        # Options for Question 2 of exam 17
        {'question_id': 4, 'option_text': 'Option A for Question 2 of exam 17'},
        {'question_id': 4, 'option_text': 'Option B for Question 2 of exam 17'},
        {'question_id': 4, 'option_text': 'Option C for Question 2 of exam 17'},
        {'question_id': 4, 'option_text': 'Option D for Question 2 of exam 17'},
        
    ]
    try:
        for data in options_data:
            option = QuestionOption(**data)
            db.session.add(option)
        db.session.commit()
        print("Question options inserted successfully.")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error inserting question options: {str(e)}")
        
def insert_assignment_exams():
    
    exams_data = [
     {'course_id': 1, 'exam_name': 'Software Testing Exam Week 1 graded', 'week': 1, 'graded': True, 'exam_description': 'Week 1 exam for Software Testing covering basic concepts.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
     {'course_id': 1, 'exam_name': 'Software Testing Exam Week 1', 'week': 1, 'graded': False, 'exam_description': 'Week 1 exam for Software Testing covering basic concepts.', 'exam_end_time': datetime(2024, 8, 12, 23, 59)},
    ]
    try:
        for data in exams_data:
            exam = AssignmentExam(**data)
            db.session.add(exam)
        db.session.commit()
        print("Exams inserted successfully.")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error inserting exams: {str(e)}")
    
def insert_assignment_exam_questions(): 
    # Insert questions
    questions_data = [
        {'exam_id': 1, 'question_text': 'Find sum of two numbers?'},
        {'exam_id': 2, 'question_text': 'Find multiplication of two numbers?'},
        {'exam_id': 3, 'question_text': 'Find diffence of two numbers?'}
    ]

    try:
        for question_data in questions_data:
            question = AssignmentExamQuestion(**question_data)
            db.session.add(question)
        db.session.commit()
        print("Questions inserted successfully.")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error inserting questions: {str(e)}")   
        
        
        
def insert_assignment_question_options():
    # You need to ensure that questions are already inserted before this
    options_data = [
        {'question_id': 1, 'input': '{"a": 5, "b": 3}', 'expected_output': '8'},
        {'question_id': 1, 'input': '{"a": 10, "b": 2}', 'expected_output': '12'},
        {'question_id': 1, 'input': '{"a": 1, "b": 1}', 'expected_output': '2'},
        {'question_id': 2, 'input': '{"a": 2, "b": 4}', 'expected_output': '8'},
        {'question_id': 2, 'input': '{"a": 3, "b": 5}', 'expected_output': '15'},
        {'question_id': 2, 'input': '{"a": 7, "b": 6}', 'expected_output': '42'},
        {'question_id': 3, 'input': '{"a": 10, "b": 7}', 'expected_output': '3'},
        {'question_id': 3, 'input': '{"a": 9, "b": 4}', 'expected_output': '5'}
    ]

    try:
        options = [AssignmentQuestionOption(**option_data) for option_data in options_data]
        db.session.bulk_save_objects(options)
        db.session.commit()
        print("Options inserted successfully.")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error inserting options: {str(e)}")
          
        

if __name__ == '__main__':
    with app.app_context():
        # Insert data into tables
        db.create_all()
        insert_courses()
        insert_exams()
        insert_exam_questions()
        insert_question_options()
        create_user()
        insert_assignment_exams()
        insert_assignment_exam_questions()
        insert_assignment_question_options()
