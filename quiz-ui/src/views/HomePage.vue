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
    <div class="scores-container">
      <ul class="score-list">
        <li v-for="scoreEntry in registeredScores" :key="scoreEntry.date" class="score-item">
          {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
        </li>
      </ul>
    </div>
    <div class="quiz-start-container">
      <router-link to="/new-quiz" class="start-quiz-button">Start Quiz</router-link>
    </div>
  </div>
</template>



<style>
.homepage {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.scores-container {
  max-height: 300px; /* Hauteur maximale pour le défilement */
  overflow-y: auto; /* Permet le défilement vertical si le contenu dépasse la hauteur maximale */
  margin-bottom: 20px; /* Espace entre la liste des scores et le bouton */
  width: 100%; /* Utilisez une largeur fixe ou en pourcentage selon la conception */
  max-width: 600px; /* Largeur maximale pour la liste des scores */
}

.score-list {
  list-style-type: none;
  padding: 0;
  margin: 0; /* Supprime la marge par défaut de la liste */
}

.score-item {
  background-color: #f0f0f0;
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
}

.quiz-start-container {
  text-align: center;
  width: 100%;
}

.start-quiz-button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border: none;
  border-radius: 5px;
  margin-top: 10px; /* Ajoute un peu d'espace au-dessus du bouton */
}

.start-quiz-button:hover {
  background-color: #45a049;
}

.scoreboard-title {
  text-align: center;
  margin-bottom: 20px; /* Espace après le titre */
}
</style>
