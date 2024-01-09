from flask import Blueprint, request,jsonify
import sqlite3
from database.db import saveQuestion
from model.question import Question


questions = Blueprint('questions', __name__)

@questions.route('/questions', methods=['POST'])
def post_question():
    data = request.get_json()
    acces_token = request.headers.get('Authorization')
    if not acces_token: 
        return 401
    try:
        question_id = saveQuestion(data)
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"id": question_id}), 200
