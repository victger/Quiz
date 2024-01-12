import json 

class PossibleAnswer():
    def __init__(self, question_id: int, text: str, isCorrect: bool, id=None):
        self.id = id
        self.question_id = question_id
        self.text = text
        self.isCorrect =  bool(isCorrect)

class Question():
    def __init__(self, text: str, title: str, image: str, position: int, id=None):
        self.id = id
        self.text = text
        self.title = title
        self.image = image
        self.position = position

class Participation:
    def __init__(self, player_name, answer_positions, score=0, id=None):
        self.id = id
        self.player_name = player_name
        self.answer_positions = answer_positions  
        self.score = score
        
class ParticipationResult:
    def __init__(self, participation_id, date, id=None):
        self.id = id
        self.participation_id = participation_id
        self.date = date


def serialization(obj):
    return json.dumps( obj.__dict__, indent=2)
    

def deserialization(data, obj_class):
    return obj_class(**json.loads(data))

def insert_request_generator(obj):
    table_name = obj.__class__.__name__.lower()
    columns = ', '.join([key for key in obj.__dict__.keys() if key != 'id'])
    values = ', '.join(["'" + str(value).replace("'", "''") + "'" if isinstance(value, str) else str(value) for key, value in obj.__dict__.items() if key != 'id'])
    return f"INSERT INTO {table_name} ({columns}) VALUES ({values});"

def obj_from_select_request_generator(sql_query_res, obj_class):
    if obj_class == Question:
        return obj_class(id=sql_query_res[0], title=sql_query_res[1], text=sql_query_res[2], image=sql_query_res[3], position=sql_query_res[4])
    elif obj_class == PossibleAnswer:
        return obj_class(id=sql_query_res[0], question_id=sql_query_res[1], text=sql_query_res[2], isCorrect=sql_query_res[3])
    else:
        raise ValueError("Unsupported class for object creation")


def delete_all_query_generator(obj):
    table_name = obj.__class__.__name__.lower()
    return f"DELETE FROM {table_name} ;"