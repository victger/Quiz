import json

class Question():
	def __init__(self, title: str, text: str, image: str, position: int, possible_answers: dict):
		self.title = title
		self.text = text
		self.image = image
		self.position = position
		self.possible_answers = possible_answers
		
def python_to_json(self):
        data = {
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "position": self.position,
            "possible_answers": self.possible_answers
        }
        return json.dumps(data, ensure_ascii=False)

@staticmethod
def json_to_python(data):
    return Question(
        title=data["title"],
        text=data["text"],
        image=data["image"],
        position=data["position"],
        possible_answers=data["possible_answers"]
    )




