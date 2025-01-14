from flask import request, jsonify
from flask_jwt_extended import (
     jwt_required, create_access_token,
    get_jwt_identity
)
from os.path import basename
import hashlib
from app import app, db, jwt
from model import  User,Course,Exam,ExamQuestion,QuestionOption,UserAnswer,UserExam,AssignmentExam,AssignmentExamQuestion,AssignmentQuestionOption,UserAssignmentAnswer
import json
import sys
import io
import os
import traceback
from datetime import datetime
from ai import get_ai_response,get_ai_response_code, get_ai_response_feedback


@app.route("/genaicode",methods=["POST"])
@jwt_required()
def genaicode():
    data = request.json
    question=data.get('question')
    query=data.get('query')
    if query =='sample query':
        query=""
    code=data.get('code')
    ans=get_ai_response_code(question,query,code)
    ans["query"]=query
    return ans ,200

@app.route("/genaifeedback",methods=["POST"])
@jwt_required()
def genaifeedback():
    data = request.json
    question=data.get('question')
    code=data.get('code')
    ans=get_ai_response_feedback(question,code)
    return ans ,200

@app.route("/dummy",methods=["POST"])
@jwt_required()
def dummy():
    data = request.json
    question=data.get('question')
    query=data.get('query')
    if query =='sample query':
        query=""
    option_selected=data.get('ans')
    qid=data.get('qid')
    ans=get_ai_response(question,query,option_selected)
    ans["query"]=query
    ans["qid"]=qid
    return ans ,200

@app.route("/login", methods=["POST"])
def login():
    try:
        if request.content_type == 'application/json':
            # Handling JSON data
            username = request.json.get("username")
            password = request.json.get("password")
        else:
            # Handling form data
            username = request.form.get("username")
            password = request.form.get("password")

        if not username or not password:
            return jsonify({"message": "Username and password are required", "status": "error"})

        user = User.query.filter_by(username=username).first()
        if user and user.password == hashlib.md5(password.encode()).hexdigest():
            access_token = create_access_token(identity={"username": username})
            return jsonify({"access_token": access_token, "message": "Login successful", "status": "success"}),200
        else:
            return jsonify({"message": "Invalid credentials", "status": "error"}),404
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}),400

@app.route("/courses", methods=["GET"])
@jwt_required() 
def get_all_courses():
    courses = Course.query.all()
    course_list = []
    for course in courses:
        course_data = {
            "course_id": course.id,
            "course_name": course.course_name,

        }
        course_list.append(course_data)

    return jsonify({"courses": course_list})

@app.route("/course/<int:course_id>/<string:parameter>", methods=["GET"])
@jwt_required() 
def get_course_detail(course_id, parameter):
    course = Course.query.filter_by(id=course_id).first()
    if course:
        if parameter == "about":
            course_data = {
                "about": course.about
            }
        elif parameter == "general_instruction":
            course_data = {
                "general_instruction": course.general_instruction
            }
        elif parameter == "please_read":
            course_data = {
                "please_read": course.please_read
            }
        elif parameter == "placement_activity":
            course_data = {
                "placement_activity": course.placement_activity
            }

        else:
            return jsonify({"message": "Invalid parameter", "status": "error"}), 400
        
        return jsonify(course_data), 200
    else:
        return jsonify({"message": "Course not found", "status": "error"}), 404

    
@app.route("/course/<int:course_id>/week/<int:week>/exam/<int:grade>", methods=["GET"])
@jwt_required() 
def get_weekly_exam_questions(course_id, week,grade):
    exam = Exam.query.filter_by(course_id=course_id, week=week,graded=bool(grade)).first()
    if exam:
        questions = ExamQuestion.query.filter_by(exam_id=exam.id).all()
        questions_data = []
        for question in questions:
            options = QuestionOption.query.filter_by(question_id=question.id).all()
            options_data = [{"option_id": option.id, "option_text": option.option_text} for option in options]
            questions_data.append({
                "question_id": question.id,
                "question_text": question.question_text,
                "correct_answer_id":question.correct_answer_id,
                "options": options_data
            })
        
        response = {
            "course_id": course_id,
            "week": week,
            "exam_id": exam.id,
            "exam_name": exam.exam_name,
            "exam_description": exam.exam_description,
            "exam_end_time":exam.exam_end_time,
            "questions": questions_data,
            "graded":exam.graded,
            "duepassed":(exam.exam_end_time < datetime.now())
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "No exam found for the given course and week."}), 404
 
@app.route("/course/<int:course_id>/week/<int:week>/demo", methods=["GET"])
@jwt_required()
def get_weekly_demo(course_id, week):
    exam = Exam.query.filter_by(id=course_id, week=week,graded=1).first()
    if exam:
        response = {
            "course_id": course_id,
            "week": week,
            "demo": exam.demo  # Include the demo field
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "No demo found for the given course and week."}), 404
    
    
@app.route('/submit-answers', methods=['POST'])
@jwt_required()  # Ensure the user is authenticated
def submit_answers():
    data = request.json
    
    # Validate incoming data
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    course_id = data.get('course_id')
    exam_id = data.get('exam_id')
    user_answers = data.get('user_answers', [])
    
    if not course_id or not exam_id or not user_answers:
        return jsonify({'message': 'Missing required fields'}), 400
    
    total_questions = len(user_answers)
    correct_answers = 0
    score = 0
    
    current_user = get_jwt_identity()
    user_id = current_user['username']  # Extract the username from the current_user dictionary
    user = User.query.filter_by(username=user_id).first()
    user_id=user.id

    if not isinstance(user_id, int):
        return jsonify({'message': 'Invalid user ID'}), 400

    for answer in user_answers:
        question_id = answer.get('question_id')
        selected_option_id = answer.get('selected_option_id')
        
        if not question_id or selected_option_id is None:
            continue  # Skip if any required field is missing
        
        # Retrieve the question to check the correct answer
        question = ExamQuestion.query.get(question_id)
        if not question:
            continue  # Skip if question not found
        
        # Check if selected option is correct
        is_correct = (selected_option_id == question.correct_answer_id)
        
        # Save user answer
        user_answer = UserAnswer(
            user_id=user_id,
            question_id=question_id,
            selected_option_id=selected_option_id,
            is_correct=is_correct
        )
        db.session.add(user_answer)
        
        # Calculate score
        if is_correct:
            correct_answers += 1
            score += 1
    
    # Calculate percentage
    percentage_score = (score / total_questions) * 100 if total_questions > 0 else 0
    
    # Save user exam details to UserExam table
    user_exam = UserExam(
        user_id=user_id,
        exam_id=exam_id,
        score=score,
        percentage=percentage_score
    )
    db.session.add(user_exam)
    
    # Commit all changes in a transaction
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    
    return jsonify({'score': score, 'percentage': percentage_score}), 200

@app.route('/usergrades', methods=['GET'])
@jwt_required()
def get_user_grades():
    current_user = get_jwt_identity()
    user_id = current_user.get('username')
    user = User.query.filter_by(username=user_id).first()


    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_id = user.id

    # Subquery to get the latest UserExam entries for each exam_id
    subquery = (
        db.session.query(
            UserExam.exam_id,
            db.func.max(UserExam.id).label('max_id')
        )
        .filter_by(user_id=user_id)
        .group_by(UserExam.exam_id)
        .subquery()
    )

    # Main query to get the latest UserExam entries using the subquery
    latest_user_exams = (
        db.session.query(UserExam)
        .join(subquery, UserExam.id == subquery.c.max_id)
        .all()
    )

    if not latest_user_exams:
        return jsonify({'message': 'No exam results found for the user.'}), 404

    results = []
    for user_exam in latest_user_exams:
        exam = Exam.query.get(user_exam.exam_id)
        if exam:
            results.append({
                'exam_id': exam.id,
                'exam_name': exam.exam_name,
                'score': user_exam.score,
                'percentage': user_exam.percentage
            })

    return jsonify({'grades': results}), 200

@app.route("/course/<int:course_id>/week/<int:week>/assignmentexam/<int:grade>", methods=["GET"])
@jwt_required() 
def get_weekly_assignment_exam_questions(course_id, week,grade):
    exam = AssignmentExam.query.filter_by(course_id=course_id, week=week,graded=bool(grade)).first()
    if exam:
        questions = AssignmentExamQuestion.query.filter_by(exam_id=exam.id).all()
        questions_data = []
        for question in questions:
            options = AssignmentQuestionOption.query.filter_by(question_id=question.id).all()
            options_data = [{"option_id": option.id, "sample_input": option.input,"expected_output": option.expected_output}for option in options]
            questions_data.append({
                "question_id": question.id,
                "question_text": question.question_text,
                "options": options_data
            })
        
        response = {
            "course_id": course_id,
            "week": week,
            "exam_id": exam.id,
            "exam_name": exam.exam_name,
            "exam_description": exam.exam_description,
            "exam_end_time":exam.exam_end_time,
            "questions": questions_data
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "No exam found for the given course and week."}), 404
    
    



@app.route('/submit-code', methods=['POST'])
@jwt_required()
def submit_code():
    data = request.json
    user_code = data.get('code')
    question_id = data.get('question_id')

    # Check if user code and question_id are provided
    if not user_code or not question_id:
        return jsonify({"message": "Missing 'code' or 'question_id' in request"}), 400

    # Retrieve the question and options from the database
    question = AssignmentExamQuestion.query.filter_by(id=question_id).first()
    if not question:
        return jsonify({"message": "Invalid question ID"}), 404
    exam_id = question.exam_id

    options = AssignmentQuestionOption.query.filter_by(question_id=question_id).all()
    if not options:
        return jsonify({"message": "No options found for the given question"}), 404

    # Prepare to test user code
    results = []
    for option in options:
        input_data = json.loads(option.input)
        expected_output = option.expected_output

        # Prepare to capture stdout
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        # Simulate the input() function
        old_stdin = sys.stdin
        new_stdin = io.StringIO("\n".join(map(str, input_data.values())))
        sys.stdin = new_stdin

        try:
            # Execute the user code directly
            exec(user_code, {}, {})

            # Capture the output
            actual_output = new_stdout.getvalue().strip()

            # Check if actual output matches expected output
            is_correct = actual_output == expected_output
            results.append({
                "input": input_data,
                "expected_output": expected_output,
                "actual_output": actual_output,
                "is_correct": is_correct
            })
        except Exception as e:
            traceback_str = traceback.format_exc()
            return jsonify({"message": f"Error executing user code: {str(e)}", "traceback": traceback_str}), 500
        finally:
            sys.stdout = old_stdout
            sys.stdin = old_stdin
            
        # Save the result to UserAssignmentAnswer table
    current_user = get_jwt_identity()
    user_id = current_user.get('username')
    user = User.query.filter_by(username=user_id).first()


    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_id = user.id
     # Check if an entry for the same user and exam already exists
    user_answer = UserAssignmentAnswer.query.filter_by(user_id=user_id, exam_id=exam_id).first()
    
    if user_answer:
        # Update the existing entry
        user_answer.result_json = json.dumps(results)
        db.session.commit()   
    else:
        # Insert a new entry
        user_answer = UserAssignmentAnswer(
            user_id=user_id,
            question_id=question_id,
            exam_id=exam_id,
            result_json=json.dumps(results)
        )
        db.session.add(user_answer)
        db.session.commit() 

    return jsonify({"results": results}), 200


@app.route('/user-assignment-result', methods=['GET'])
@jwt_required()
def get_user_assignment_result():
    current_user = get_jwt_identity()
    user_id = current_user.get('username')
    user = User.query.filter_by(username=user_id).first()
    

    if not user:
        return jsonify({'message': 'User not found'}), 404
    user_id=user.id

    try:
        # Fetch all entries for the given user_id
        user_answers = UserAssignmentAnswer.query.filter_by(user_id=user_id).all()

        result = [
            {
                "id": answer.id,
                "user_id": answer.user_id,
                "question_id": answer.question_id,
                "exam_id": answer.exam_id,
                "result_json": answer.result_json,
            }
            for answer in user_answers
        ]

        return jsonify(result), 200

    except Exception as e:
        traceback_str = traceback.format_exc()
        return jsonify({"message": f"Error fetching user assignment answers: {str(e)}", "traceback": traceback_str}), 500

