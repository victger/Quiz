from flask import Blueprint, request,jsonify
import sqlite3
import json
from database.db import saveQuestion, savePossibleAnswer , retrieveQuestion, retrievePossibleAnswers,updateQuestion, updatePossibleAnswers, removeQuestion, removeAllQuestion, isQuizComplet
from model.models import Question,PossibleAnswer, serialization

questions = Blueprint('questions', __name__)

@questions.route('/questions/<int:questionId>', methods=['GET'])
def get_question_by_id(questionId):
    question = retrieveQuestion("id", questionId)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    possible_answers = retrievePossibleAnswers(questionId)
    question_json = serialization(question)
    question_dict = json.loads(question_json)

    possible_answers_list = [
    {"id": ans.id, "text": ans.text, "isCorrect": ans.isCorrect}
    for ans in possible_answers
    ]
    question_dict["possibleAnswers"] = possible_answers_list
    return jsonify(question_dict), 200

@questions.route('/questions', methods=['GET'])
def get_question_by_position():
    position = request.args.get('position', type=int)
    if position is None:
        return jsonify({"error": "Position parameter is required"}), 400

    question = retrieveQuestion("position", position)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    possible_answers = retrievePossibleAnswers(question.id)
    question_json = serialization(question)
    question_dict = json.loads(question_json)

    possible_answers_list = [
        {"id": ans.id, "text": ans.text, "isCorrect": ans.isCorrect}
        for ans in possible_answers
    ]
    question_dict["possibleAnswers"] = possible_answers_list
    return jsonify(question_dict), 200

@questions.route('/questions', methods=['POST', 'OPTIONS'])
def post_question():
    data = request.get_json()
    access_token = request.headers.get('Authorization')

    if not access_token: 
        return jsonify({"error": "Unauthorized"}), 401
    
    if isQuizComplet() >= 10:
        return jsonify({"error": "Quiz complet"}), 400

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

        question_to_update = updateQuestion(data, questionId)
        if not question_to_update:
            return jsonify({"error": "Question not found"}), 404
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
        question_removed = removeQuestion(questionId)
        if not question_removed:
            return jsonify({"error": "Question not found"}), 404
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