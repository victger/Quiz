from flask import Flask, request
from flask_cors import CORS
from utils.jwt_utils import build_token
import hashlib
from routes.questions import questions 


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'hsdh'
	return f"Hello, {x}"


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200


@app.route('/login', methods=['POST'])
def Login():
	payload = request.get_json()
	tried_password = payload['password'].encode('UTF-8')
	tried_password_hash = hashlib.md5(tried_password).hexdigest()
	password = "94c0d1d9d64e6b31743ed1fbf685539c"
	if tried_password_hash == password : 
		token = build_token()
		return {'token': token}, 200
	else : 
		return 'Unauthorized', 401 
	
	
app.register_blueprint(questions)

if __name__ == "__main__":
    app.run()