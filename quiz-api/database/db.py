import sqlite3
from model.models import insert_request_generator, obj_from_select_request_generator
from model.models import Question,PossibleAnswer
from datetime import datetime


def saveQuestion(question):
    
    db_connection = sqlite3.connect('./quiz.db')  
    cur = db_connection.cursor()
        
    try:
        cur.execute("begin")
        insert_query = insert_request_generator(question)
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
        insert_query = insert_request_generator(possible_answer)
        cur.execute(insert_query)
        print(insert_query)
        cur.execute("commit")
    except sqlite3.Error as e:
        cur.execute("rollback")
        raise e
    finally:
        db_connection.close()

def retrieveQuestion(by, value):
    db_connection = sqlite3.connect('./quiz.db')
    db_connection.isolation_level = None

    cur = db_connection.cursor()

    try:
        if by == "id":
            cur.execute("SELECT ID, title, text, image, position FROM question WHERE ID = ?", (value,))
        elif by == "position":
            cur.execute("SELECT ID, title, text, image, position FROM question WHERE position = ?", (value,))
        else:
            raise ValueError("Invalid search criteria")

        result = cur.fetchone()
        print(result)
        return obj_from_select_request_generator(result, Question) if result else None

    except sqlite3.Error as e:
        print("Database error:", e)
        return None
    finally:
        db_connection.close()

def retrievePossibleAnswers(questionId):
    db_connection = sqlite3.connect('./quiz.db')
    db_connection.isolation_level = None

    cur = db_connection.cursor()
    possible_answers = []

    try:
        cur.execute("begin")
        cur.execute("SELECT * FROM possibleanswer WHERE question_id = ?", (questionId,))
        results = cur.fetchall()

        for result in results:
            possible_answers.append(obj_from_select_request_generator(result, PossibleAnswer))

        return possible_answers

    except sqlite3.Error as e:
        print("Database error:", e)
        return []
    finally:
        db_connection.close()

def updateQuestion(data, questionId):
    try:
        db_connection = sqlite3.connect('./quiz.db')
        db_connection.isolation_level = None

        cur = db_connection.cursor()
        cur.execute("begin")
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
    db_connection = sqlite3.connect('./quiz.db')
    cur = db_connection.cursor()

    try:
        db_connection.execute("begin") 
        for answer in possibleAnswers:
            cur.execute("""
                INSERT INTO possibleanswer (question_id, text, isCorrect)
                VALUES (?, ?, ?)
                ON CONFLICT(id)
                DO UPDATE SET
                    text = excluded.text,
                    isCorrect = excluded.isCorrect
                WHERE question_id = ?;
            """, (questionId, answer['text'], answer['isCorrect'], questionId))

        db_connection.commit()  
    except sqlite3.Error as e:
        db_connection.rollback()  
        raise e
    finally:
        cur.close()
        db_connection.close()

def removeQuestion(questionId):
    try:
        db_connection = sqlite3.connect('./quiz.db')
        cur = db_connection.cursor()

        cur.execute("DELETE FROM question WHERE id = ?", (questionId,))
        cur.execute("DELETE FROM possibleanswer WHERE  question_id= ?", (questionId,))
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

def saveParticipation(participation):
    answer_positions_str = ','.join(map(str, participation.answer_positions))

    db_connection = sqlite3.connect('./quiz.db')
    cursor = db_connection.cursor()

    cursor.execute('''
        INSERT INTO participation (player_name, answer_positions, score)
        VALUES (?, ?, ?)
    ''', (participation.player_name, answer_positions_str, participation.score))

    participation_id = cursor.lastrowid  

    
    participation_date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO participationResult (participation_id, date)
        VALUES (?, ?)
    ''', (participation_id, participation_date_str))

    db_connection.commit()
    db_connection.close()

def calculateScore(answer_positions):
    score = 0
    answers_summaries = []

    db_connection = sqlite3.connect('./quiz.db')
    cur = db_connection.cursor()

    for question_pos, user_answer_position in enumerate(answer_positions, start=1):
        print(f"Question Position: {question_pos}, User Answer Position: {user_answer_position}")

        cur.execute("""
            SELECT id, isCorrect 
            FROM possibleanswer 
            WHERE question_id = (
                SELECT id 
                FROM question 
                WHERE position = ?
            )
            ORDER BY id
        """, (question_pos,))

        possible_answers = cur.fetchall()
        print(f"Possible Answers for Question {question_pos}: {possible_answers}")

        correct_answer_position = None
        user_answer_correct = False

        for pos, (answer_id, isCorrect) in enumerate(possible_answers):
            if isCorrect:
                correct_answer_position = pos + 1
            if pos + 1 == user_answer_position and isCorrect:
                user_answer_correct = True

        print(f"Correct Answer Position: {correct_answer_position}, User Answer Correct: {user_answer_correct}")

        if user_answer_correct:
            score += 1

        answers_summaries.append({
            "correctAnswerPosition": correct_answer_position,
            "wasCorrect": user_answer_correct
        })

    print(f"Final Score: {score}, Answers Summaries: {answers_summaries}")

    db_connection.close()

    return score, answers_summaries

def saveParticipationResult(participation_result):
    db_connection = sqlite3.connect('./quiz.db')
    cursor = db_connection.cursor()

    cursor.execute('''
        INSERT INTO participationResult (participation_id, date)
        VALUES (?, ?)
    ''', (participation_result.participation_id, participation_result.date.strftime('%Y-%m-%d %H:%M:%S')))

    db_connection.commit()
    db_connection.close()

def getParticipationResults():
    db_connection = sqlite3.connect('./quiz.db')
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT p.id, p.player_name, p.score, pr.date 
        FROM participationResult pr 
        JOIN participation p ON pr.participation_id = p.id 
        ORDER BY p.score DESC
    """)
    results = cursor.fetchall()

    db_connection.close()
    return results

def removeAllParticipations():
    try:
        db_connection = sqlite3.connect('./quiz.db')
        cur = db_connection.cursor()

        cur.execute("DELETE FROM participation")
    
        db_connection.commit()
    except sqlite3.Error as e:
        db_connection.rollback()
    finally:
        db_connection.close()