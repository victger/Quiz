from flask import Blueprint, request,jsonify
import sqlite3
from database.db import saveQuestion, savePossibleAnswer ,updateQuestion, updatePossibleAnswers, removeQuestion, removeAllQuestion
from model.models import Question,PossibleAnswer

questions = Blueprint('questions', __name__)

@questions.route('/questions', methods=['POST'])
def post_question():
    data = request.get_json()
    acces_token = request.headers.get('Authorization')
    if not acces_token: 
        return 401
    try:
        question = Question(title=data['title'], text=data['text'], image=data['image'], position=data['position'])
        question_id = saveQuestion(question)

        for answer_data in data['possibleAnswers']:
            possible_answer = PossibleAnswer(question_id, answer_data['text'], answer_data['isCorrect'])
            savePossibleAnswer(possible_answer)
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"id": question_id}), 200

@questions.route('/questions/<int:questionId>', methods=['PUT'])
def update_question(questionId):
    data = request.get_json()
    access_token = request.headers.get('Authorization')

    if not access_token:
        return jsonify({"error": "Unauthorized"}), 401

    try: 
        updateQuestion(data, questionId)
        if 'possibleAnswers' in data:
            updatePossibleAnswers(questionId, data['possibleAnswers'])
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

    return ('', 204)


@questions.route('/questions/<int:questionId>', methods=['DELETE'])
def delete_question(questionId):
    acces_token = request.headers.get('Authorization')

    if not acces_token:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        removeQuestion(questionId)
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    return ('', 204)
    
@questions.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
    acces_token = request.headers.get('Authorization')

    if not acces_token:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        removeAllQuestion()
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    return ('', 204)