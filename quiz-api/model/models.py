import json

class Question():
	def __init__(self, title: str, text: str, image: str, position: int):
		self.title = title
		self.text = text
		self.image = image
		self.position = position

class PossibleAnswer:
    def __init__(self, question_id: int, text: str, is_correct: bool):
        self.question_id = question_id
        self.text = text
        self.is_correct = is_correct

class Participant:
    def __init__(self, player_name: str, score: int = 0):
        self.player_name = player_name
        self.score = score
        
class ParticipantAnswer:
    def __init__(self, participant_id: int, question_id: int, answer_id: int, is_correct: bool):
        self.participant_id = participant_id
        self.question_id = question_id
        self.answer_id = answer_id
        self.is_correct = is_correct
        
def python_to_json(obj):
    try:
        return json.dumps(obj.__dict__)
    except AttributeError: 
        raise ("The Question can not be converted to Json.")

def json_to_python(obj):
    try:
        data = json.loads(obj)
        return Question(**data)
    except TypeError:
        raise ValueError("Json Can not be converted  to Question")
    
def generate_Insert_request(obj):
    table = obj.__class__.__name__.lower()
    columns = ', '.join(obj.__dict__.keys())
    values = ', '.join([f"'{valeur.replace("'", "''")}'" if isinstance(valeur, str) else str(valeur) for valeur in obj.__dict__.values()])
    sql_req = f"INSERT INTO {table} ({columns}) VALUES ({values});"
    return sql_req

def select_sql_req_to_python(select_sql_result, obj):
    return obj(**select_sql_result)