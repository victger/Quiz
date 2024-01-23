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

async function endQuiz() {
  try {
    const playerName = participationStorageService.getPlayerName();
    const arrayAnswers= Array.from(answers.value);
    console.log(arrayAnswers);
    const response = await quizApiService.postParticipation(playerName, arrayAnswers);
    const finalScore = response.data.score
    participationStorageService.saveFinalScore(finalScore)

    router.push('/score');
  } catch (error) {
    console.error("Erreur lors de la fin du quiz :", error);
  }
}

</script>

<template>
  <div class="question-container">
    <h1 class = "question-number">Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
    <QuestionsDisplay :question="currentQuestion" @next-question="loadNextQuestion" class="question-text"/>
  </div>
</template>

<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Nunito:wght@400&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap');


.question-container {
  width: 100%;
  box-sizing: border-box;
  padding: 0 20px;
  text-align: center
}
.question-number{
  font-family: 'Lobster', cursive;
  font-weight: bold;
}

.question-text {
  font-family: 'Merriweather', serif;
}
</style>
