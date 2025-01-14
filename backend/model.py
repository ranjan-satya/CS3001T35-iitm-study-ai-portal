from app import db

# Models

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    
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