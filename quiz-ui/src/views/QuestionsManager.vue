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

async function answerClickedHandler(answerIndex) {
  try {
    answers.value.push(answerIndex);
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
    const playerName = participationStorageService.getPlayerName();
    const response = await quizApiService.postParticipation(playerName, answers.value);
    const finalScore = response.data.score
    participationStorageService.saveFinalScore(finalScore)

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