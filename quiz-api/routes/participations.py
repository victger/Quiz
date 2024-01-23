from flask import Blueprint, request,jsonify
import sqlite3
from database.db import removeAllParticipations , saveParticipation, calculateScore, isUsernameUnique
from model.models import Participation

participations  = Blueprint('participations ', __name__)

@participations.route('/participations', methods=['POST'])
def post_participations():
    data = request.get_json()
    player_name = data.get('playerName')  
    answer_positions = data.get('answers')

    if len(answer_positions) != 10:
        return jsonify({"error": "Bad request"}), 400
    

    score, answers_summaries = calculateScore(answer_positions)

    participation = Participation(player_name, answer_positions, score)
    
    saveParticipation(participation)

    return jsonify({
        "answersSummaries": answers_summaries,
        "playerName": player_name,
        "score": score
    }), 200

@participations.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
    acces_token = request.headers.get('Authorization')

    if not acces_token:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        removeAllParticipations()
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    return ('', 204)

@participations.route('/check-username', methods=['POST'])
def check_username():
    data = request.get_json()
    player_name = data.get('playerName')

    if not player_name:
        return jsonify({"error": "Username is required"}), 400

    if isUsernameUnique(player_name):
        return jsonify({"isUnique": True}), 200
    else:
        return jsonify({"isUnique": False}), 200