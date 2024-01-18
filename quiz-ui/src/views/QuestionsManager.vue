<script setup>
import quizApiService from "@/services/QuizApiService";
import QuestionsDisplay from "@/views/QuestionsDisplay.vue";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";


const currentQuestion = ref({});
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const router = useRouter();

onMounted(async () => {
  try {
    const response1 = await quizApiService.getQuestion(1);
    const response2 = await quizApiService.getQuizInfo();

    currentQuestion.value = response1.data;
    totalNumberOfQuestions.value = response2.data.size;

    console.log(response1.data);
  } catch (error) {
    console.error("Error:", error);
  }
});

async function loadQuestionByPosition(position) {
  try {
    const response = await quizApiService.getQuestion(position);
    currentQuestion.value = response.data;
    currentQuestionPosition.value = position;
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
    router.push('/score');
  } catch (error) {
    console.error("Erreur lors de la fin du quiz :", error);
  }
}

async function loadNextQuestion() {
  try {
    if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
      currentQuestionPosition.value++;
      await loadQuestionByPosition(currentQuestionPosition.value);
    } else {
      await endQuiz();
    }
  } catch (error) {
    console.error("Erreur lors du chargement de la question suivante :", error);
  }
}
</script>

<template>
  <div>
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
    <QuestionsDisplay :question="currentQuestion" @answer-clicked="answerClickedHandler" @next-question="loadNextQuestion" />
  </div>
</template>