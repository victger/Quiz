import sqlite3
from model.models import insert_request_generator, obj_from_select_request_generator
from model.models import Question,PossibleAnswer
from datetime import datetime


def save_question_positions(cur, new_position):
    cur.execute("SELECT MAX(position) FROM question")
    max_position_result = cur.fetchone()
    max_position = max_position_result[0] if max_position_result[0] is not None else 0

    if new_position <= max_position:
        cur.execute("""
            UPDATE question
            SET position = position + 1
            WHERE position >= ?
        """, (new_position,))

def update_question_positions(cur, new_position, current_position):
    if new_position > current_position:
        cur.execute("""
            UPDATE question
            SET position = position - 1
            WHERE position > ? AND position <= ?
        """, (current_position, new_position))
    else:
        cur.execute("""
            UPDATE question
            SET position = position + 1
            WHERE position >= ? AND position < ?
        """, (new_position, current_position))

def saveQuestion(question):
    
    db_connection = sqlite3.connect('./quiz.db')  
    cur = db_connection.cursor()
        
    try:
       
        cur.execute("begin")
        save_question_positions(cur, question.position)
        insert_query = insert_request_generator(question)
        cur.execute(insert_query)
        question_id = cur.lastrowid
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
        cur = db_connection.cursor()

        cur.execute("begin")

        cur.execute("SELECT id FROM question WHERE id = ?", (questionId,))
        if cur.fetchone() is None:
            cur.execute('rollback') 
            return False

        cur.execute("SELECT position FROM question WHERE id = ?", (questionId,))
        row = cur.fetchone()
        current_position = row[0]

        new_position = data['position']
        if current_position != new_position:
            update_question_positions(cur, new_position, current_position)

        cur.execute("""
            UPDATE question SET title = ?, text = ?, image = ?, position = ?
            WHERE ID = ?
        """, (data['title'], data['text'], data['image'], new_position, questionId))

        cur.execute("commit")
        return True
    except sqlite3.Error as e:
        cur.execute('rollback')  
        raise e
    finally:
        cur.close()
        db_connection.close()

def updatePossibleAnswers(questionId, possibleAnswers):
    db_connection = sqlite3.connect('./quiz.db')
    cur = db_connection.cursor()

    try:
        db_connection.execute("begin") 

        cur.execute("DELETE FROM possibleanswer WHERE question_id = ?", (questionId,))

        for answer in possibleAnswers:
            cur.execute("""
                INSERT INTO possibleanswer (question_id, text, isCorrect)
                VALUES (?, ?, ?);
            """, (questionId, answer['text'], answer['isCorrect']))

        db_connection.commit()  
    except sqlite3.Error as e:
        db_connection.rollback()  
        raise e
    finally:
        cur.close()
        db_connection.close()

def update_positions_after_deletion(cur, deleted_position):
    cur.execute("""
        UPDATE question
        SET position = position - 1
        WHERE position > ?
    """, (deleted_position,))

def removeQuestion(questionId):
    try:
        db_connection = sqlite3.connect('./quiz.db')
        cur = db_connection.cursor()
        cur.execute("begin")

        cur.execute("SELECT position FROM question WHERE id = ?", (questionId,))
        row = cur.fetchone()
        if row is None:
            cur.execute('rollback') 
            return False
        deleted_position = row[0]

        cur.execute("DELETE FROM question WHERE id = ?", (questionId,))

        cur.execute("DELETE FROM possibleanswer WHERE question_id = ?", (questionId,))

        update_positions_after_deletion(cur, deleted_position)

        cur.execute("commit")
        return True
    except sqlite3.Error as e:
        cur.execute('rollback')  
        raise e
    finally:
        cur.close()
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

        correct_answer_position = None
        user_answer_correct = False

        for pos, (answer_id, isCorrect) in enumerate(possible_answers):
            if isCorrect:
                correct_answer_position = pos + 1
            if pos + 1 == user_answer_position and isCorrect:
                user_answer_correct = True


        if user_answer_correct:
            score += 1

        answers_summaries.append({
            "correctAnswerPosition": correct_answer_position,
            "wasCorrect": user_answer_correct
        })

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
        cur.execute("DELETE FROM participationResult")

        db_connection.commit()
    except sqlite3.Error as e:
        db_connection.rollback()
    finally:
        db_connection.close()

def isUsernameUnique(username):
    db_connection = sqlite3.connect('./quiz.db')
    cursor = db_connection.cursor()

    cursor.execute('''
        SELECT COUNT(*) FROM participation WHERE player_name = ?
    ''', (username,))

    count = cursor.fetchone()[0]

    db_connection.close()

    return count == 0

def isQuizComplet():
    db_connection = sqlite3.connect('./quiz.db')
    cur = db_connection.cursor()

    try:
        
        count_query = "SELECT COUNT(*) FROM question" 
        cur.execute(count_query)
        count = cur.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return -1
    finally:
        db_connection.close()

def create_tables(db_file):

    sql_drop_participation_table = "DROP TABLE IF EXISTS participation;"
    sql_drop_participationResult_table = "DROP TABLE IF EXISTS participationResult;"
    sql_drop_possibleanswer_table = "DROP TABLE IF EXISTS possibleanswer;"
    sql_drop_question_table = "DROP TABLE IF EXISTS question;"

    sql_create_participation_table = """ CREATE TABLE "participation" (
                                        "id" INTEGER,
                                        "player_name" TEXT NOT NULL,
                                        "answer_positions" TEXT NOT NULL,
                                        "score" INTEGER,
                                        PRIMARY KEY("id" AUTOINCREMENT)
                                    ); """

    sql_create_participationResult_table = """CREATE TABLE "participationResult" (
                                              "id" INTEGER,
                                              "participation_id" INTEGER,
                                              "date" TEXT NOT NULL,
                                              FOREIGN KEY("participation_id") REFERENCES "participation"("id"),
                                              PRIMARY KEY("id" AUTOINCREMENT)
                                            );"""

    sql_create_possibleanswer_table = """CREATE TABLE "possibleanswer" (
                                         "id" INTEGER,
                                         "question_id" INTEGER NOT NULL,
                                         "text" TEXT NOT NULL,
                                         "isCorrect" BOOLEAN NOT NULL,
                                         FOREIGN KEY("question_id") REFERENCES "question"("id"),
                                         PRIMARY KEY("id")
                                       );"""

    sql_create_question_table = """CREATE TABLE "question" (
                                   "id" INTEGER,
                                   "text" TEXT NOT NULL,
                                   "title" VARCHAR(255) NOT NULL,
                                   "image" TEXT,
                                   "position" INTEGER NOT NULL,
                                   PRIMARY KEY("id")
                                 );"""


    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        c.execute(sql_drop_participation_table)
        c.execute(sql_drop_participationResult_table)
        c.execute(sql_drop_possibleanswer_table)
        c.execute(sql_drop_question_table)

        c.execute(sql_create_participation_table)
        c.execute(sql_create_participationResult_table)
        c.execute(sql_create_possibleanswer_table)
        c.execute(sql_create_question_table)

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)