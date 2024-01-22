<script setup>
import participationStorageService from "@/services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";
import QuestionsDisplay from "@/views/QuestionsDisplay.vue";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const currentQuestion = ref({});
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const answers = ref([]); 
const router = useRouter();

onMounted(async () => {
  try {
    const response1 = await quizApiService.getQuestion(1);
    const response2 = await quizApiService.getQuizInfo();

    currentQuestion.value = response1.data;
    totalNumberOfQuestions.value = response2.data.size;

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

async function endQuiz() {
  try {
    const playerName = participationStorageService.getPlayerName();
    const response = await quizApiService.postParticipation(playerName, answers.value);
    const finalScore = response.data.score
    participationStorageService.saveFinalScore(finalScore)

    router.push('/score');
  } catch (error) {
    console.error("Erreur lors de la fin du quiz :", error);
  }
}

async function loadNextQuestion(answerIndex) {
  try {
    if (answerIndex !== null) {
      answers.value.push(answerIndex+1);
    }

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
  <div class="question-container">
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
    <QuestionsDisplay :question="currentQuestion" @next-question="loadNextQuestion" />
  </div>
</template>

<style>
.question-container {
  width: 100%;
  box-sizing: border-box;
  padding: 0 20px;
  text-align: center
  /* ... autres styles ... */
}

</style>
