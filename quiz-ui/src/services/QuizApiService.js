import axios from "axios";

const instance = axios.create({
	baseURL: 'http://localhost:5000',
  json: true
});

let token = null;

export default {
  setToken(newToken) {
    token = newToken;
  },

  async call(method, resource, data = null) {
    var headers = {
      "Content-Type": "application/json",
    };

    if (token) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method, 
      headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
        return error.response;
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestion(position) {
    return this.call("get", `questions?position=${position}`);
  },
  postParticipation(playerName, answers) {
    return this.call("post", "participations", {
      playerName,
      answers});
  },
  postLogin(password){
    return this.call("post", "login",{password});
  },
  saveQuestion(questionData){
    return this.call("post", "questions", questionData, token);
  },
  deleteQuestion(questionId){
    return this.call("delete", `questions/${questionId}`, null, token);
  },
  updateQuestion(questionId, questionData){
    return this.call("put", `questions/${questionId}`, questionData, token);
  }

};