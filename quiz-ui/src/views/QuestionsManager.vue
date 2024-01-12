<script setup>

import { ref, onMounted } from "vue";
// import QuestionDisplay from "@/views/QuestionDisplay.vue";
import quizApiService from "@/services/QuizApiService";

const currentQuestion = ref({});
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const firstQuestion = ref({})

onMounted(async () => {
  try {

    const response1 = await quizApiService.getQuestion(1);
    const response2 = await quizApiService.getQuizInfo();

    firstQuestion.value= response1.data
    totalNumberOfQuestions.value= response2.data.size

    console.log(response1.data);
  } catch (error) {
    console.error("Error:", error);
  }
});

async function loadQuestionByPosition(position) {
  try {
    const response = await quizApiService.getQuestion(position);
    currentQuestion.value = response.data;
    totalNumberOfQuestions.value = response.total; 
  } catch (error) {
    console.error("Erreur lors du chargement de la question :", error);
  }
}

async function answerClickedHandler(answerIndex) {
  try {
    await quizApiService.saveAnswer(currentQuestion.value.id, answerIndex);
    if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
      currentQuestionPosition.value++;
      await loadQuestionByPosition(currentQuestionPosition.value);
    } else {
      await endQuiz();
    }
  } catch (error) {
    console.error("Erreur lors de l'enregistrement de la réponse :", error);
  }
}

async function endQuiz() {
  try {
    const finalScore = await quizApiService.getQuizInfo();
    console.log(`Le score final est : ${finalScore}`);
    router.push('/result');
  } catch (error) {
    console.error("Erreur lors de la fin du quiz :", error);
  }
}


</script>

<template>

  <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
  <p>Coucou</p>
  <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" />

  <p>{{firstQuestion}}</p>

</template>