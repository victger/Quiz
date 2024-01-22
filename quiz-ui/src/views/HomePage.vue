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
    <h1 class="scoreboard-title">LEADERBOARD</h1>
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

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Roboto:wght@400&display=swap');

.homepage {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  color: #333; /* Couleur de texte assortie au reste de l'application */
}


.score-item:hover {
  background-color: #f5f5f5; /* Changement de fond au survol */
}

.scores-container {
  max-height: 300px; /* Hauteur maximale pour le défilement */
  overflow-y: auto; /* Permet le défilement vertical si le contenu dépasse la hauteur maximale */
  margin-bottom: 20px; /* Espace entre la liste des scores et le bouton */
  width: 100%; /* Utilisez une largeur fixe ou en pourcentage selon la conception */
  max-width: 600px; /* Largeur maximale pour la liste des scores */
  background-color: #ffffff; /* Fond blanc pour la liste des scores */
  border-radius: 10px; /* Bords arrondis pour la liste des scores */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Ombre portée subtile pour la liste */
}

.score-list {
  list-style-type: none;
  padding: 0;
  margin: 0; /* Supprime la marge par défaut de la liste */
}

.score-item {
  background-color: #ffffff; /* Fond clair pour les items */
  color: #333; /* Texte en gris foncé pour une bonne lisibilité */
  font-family: 'Roboto', sans-serif;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  border: 1px solid #e1e1e1; /* Bordure subtile */
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
  transition: background-color 0.3s ease; /* Transition pour l'interaction */
}

.quiz-start-container {
  text-align: center;
  width: 100%;
}

.start-quiz-button {
  padding: 10px 20px;
  background-color: #650610; /* Couleur d'accent rouge sombre pour le bouton */
  color: white;
  text-decoration: none;
  border: none;
  border-radius: 5px;
  margin-top: 10px; /* Ajoute un peu d'espace au-dessus du bouton */
  font-weight: bold; /* Rendre le texte du bouton plus visible */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Ombre portée pour le bouton */
}

.start-quiz-button:hover {
  background-color: #5e050e; /* Couleur plus sombre lors du survol */
  transition: background-color 0.3s ease;
}

.scoreboard-title {
  font-family: 'Playfair Display', serif;
  font-weight: 700; /* Pour une police plus épaisse */
  color: #131006; /* Couleur dorée pour le titre */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* Ombre de texte plus prononcée pour le titre */
  margin-bottom: 20px;
  font-size: 2.5rem; /* Taille plus grande pour le titre */
}
</style>
