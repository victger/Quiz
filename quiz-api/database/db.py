import sqlite3
from model.models import generate_Insert_request

def saveQuestion(question):
    db_connection = sqlite3.connect('./quiz.db')  
    cur = db_connection.cursor()
        
    try:
        cur.execute("begin")
        insert_query = generate_Insert_request(question)
        cur.execute(insert_query)
        question_id = cur.lastrowid
        print(insert_query) 
        cur.execute("commit")
        return question_id
    except sqlite3.Error as e:
        cur.execute('rollback')
        raise e
    finally:
        db_connection.close()

def savePossibleAnswer(possible_answer):
    db_connection = sqlite3.connect('./quiz.db')
    db_connection.isolation_level = None
    cur = db_connection.cursor()
    
    try:
        cur.execute("begin")
        insert_query = generate_Insert_request(possible_answer)
        cur.execute(insert_query)
        print(insert_query)
        cur.execute("commit")
    except sqlite3.Error as e:
        cur.execute("rollback")
        raise e
    finally:
        db_connection.close()

def updateQuestion(data, questionId):
    try:
        db_connection = sqlite3.connect('./quiz.db')
        cur = db_connection.cursor()

        cur.execute("""
            UPDATE question SET title = ?, text = ?, image = ?, position = ?
            WHERE ID = ?
        """, (data['title'], data['text'], data['image'], data['position'], questionId))
        
        cur.execute("commit")
    except sqlite3.Error as e:
        cur.execute('rollback')
    finally:
        cur.close()

def updatePossibleAnswers(questionId, possibleAnswers):
    try:
        db_connection = sqlite3.connect('./quiz.db')
        cur = db_connection.cursor()

        for answer in possibleAnswers:
            cur.execute("""
                INSERT INTO possibleanswer (question_id, text, is_correct)
                VALUES (?, ?, ?)
                ON CONFLICT(answer_id)
                DO UPDATE SET
                    text = excluded.text,
                    is_correct = excluded.is_correct
                WHERE question_id = ?;
            """, (questionId, answer['text'], answer['isCorrect'], questionId))

        cur.execute("commit")
    except sqlite3.Error as e:
        cur.execute('rollback')
    finally:
        cur.close()


def removeQuestion(questionId):
    try:
        db_connection = sqlite3.connect('./quiz.db')
        cur = db_connection.cursor()

        cur.execute("DELETE FROM questions WHERE ID = ?", (questionId,))
        cur.execute("DELETE FROM possibleanswer WHERE ID = ?", (questionId,))
        db_connection.commit()
    except sqlite3.Error as e:
        db_connection.rollback()
    finally:
        db_connection.close()

def removeAllQuestion():
    try:
        db_connection = sqlite3.connect('./quiz.db')
        cur = db_connection.cursor()

        cur.execute("DELETE FROM question")
        cur.execute("DELETE FROM possibleanswer")
        db_connection.commit()
    except sqlite3.Error as e:
        db_connection.rollback()
    finally:
        db_connection.close()

def removeAllParticipant():
    try:
        db_connection = sqlite3.connect('./quiz.db')
        cur = db_connection.cursor()
        cur.execute("DELETE FROM participant")
        db_connection.commit()
    except sqlite3.Error as e:
        db_connection.rollback()
    finally:
        db_connection.close()