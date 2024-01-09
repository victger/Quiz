import sqlite3
from model.question import python_to_json
import json

def saveQuestion(question):
    
    db_connection = sqlite3.connect('./quiz.db')  
    cur = db_connection.cursor()
        
    try:
        cur.execute("begin")
        possible_answers_json = json.dumps(question['possibleAnswers'],ensure_ascii=False)
        cur.execute("INSERT INTO questions (position, title, text, image, possibleAnswers) VALUES (?, ?, ?, ?, ?)",
                       (question['position'], question['title'], question['text'], question['image'],possible_answers_json))
        question_id = cur.lastrowid  
        cur.execute("commit")
        return question_id
    except sqlite3.Error as e:
        cur.execute('rollback')
        raise e
    finally:
        db_connection.close()




