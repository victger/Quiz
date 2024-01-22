<script setup>
import { ref, onMounted } from "vue";
import quizApiService from "@/services/QuizApiService";

const registeredScores = ref([]);

onMounted(async () => {
  try {
    // Appel du service getQuizInfo() depuis QuizApiService.js
    const response = await quizApiService.getQuizInfo();

    // Assurez-vous que la structure de données est correcte
    if (Array.isArray(response.data.scores)) {
      // Stockage de la valeur adéquate dans registeredScores
      registeredScores.value = response.data.scores;
    } else {
      console.error("Invalid data structure for scores:", response.data);
    }
  } catch (error) {
    console.error("Error fetching quiz info:", error);
  }
});

</script>

<template>
  <div class="homepage">
    <h1 class="scoreboard-title">Top Scores</h1>
    <ul class="score-list">
      <li v-for="scoreEntry in registeredScores" :key="scoreEntry.date" class="score-item">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </li>
    </ul>
    <router-link to="/new-quiz" class="start-quiz-button">Start Quiz</router-link>
  </div>
</template>


<style>
.homepage {
  width: 100%;
  box-sizing: border-box;
  padding: 0 20px;
  /* ... autres styles ... */
}

.score-list {
  list-style-type: none;
  padding: 0;
}

.score-item {
  background-color: #f0f0f0;
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
}

.start-quiz-button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border: none;
  border-radius: 5px;
}

.start-quiz-button:hover {
  background-color: #45a049;
}

.scoreboard-title{
  text-align: center;
}
</style>

