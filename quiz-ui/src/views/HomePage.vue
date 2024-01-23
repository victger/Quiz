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
    <h1 class="scoreboard-title">Leaderboard</h1>
    <div class="scores-container">
      <ul class="score-list">
        <li v-for="(scoreEntry, index) in registeredScores" :key="scoreEntry.date" class="score-item">
          <div class="ranking-container">
            <img src="../assets/bobine.png" class="ranking-image" />
            <span class="ranking-number">{{ index + 1 }}</span>
          </div>
          <div class="score-details">
            {{ scoreEntry.playerName }} 
            <span class="stars">
              <span v-for="n in Math.min(10, scoreEntry.score)" :key="n">&#9733;</span>
              <span v-for="n in Math.max(0, 10 - scoreEntry.score)" :key="n">&#9734;</span>
            </span>
          </div>
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Nunito:wght@400&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');

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
    background-color: rgba(255, 255, 255, 0.1); /* Fond légèrement transparent */
    color: #000000; /* Texte blanc */
    border: none; /* Pas de bordure */
    margin: 10px 0;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4); /* Ombre des items */
    display: flex;
    align-items: center; /* Alignement vertical des éléments */
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
  color: #d4af37;
}

.scoreboard-title {
  font-family: 'Lobster', serif;
  font-weight: 700; /* Pour une police plus épaisse */
  color: #131006; /* Couleur dorée pour le titre */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.25); /* Ombre de texte plus prononcée pour le titre */
  margin-bottom: 20px;
  font-size: 2.5rem; /* Taille plus grande pour le titre */
}

.ranking-container {
    position: relative; /* Position relative pour le conteneur */
    display: inline-flex; /* Utilisation de flex pour un meilleur alignement */
    align-items: center; /* Aligner verticalement les éléments */
    justify-content: center; /* Centrer horizontalement les éléments */
    margin-right: 15px;
  }

  .ranking-image {
    width: 60px;
    height: auto;
  }

  .ranking-number {
    position: absolute; /* Position absolue pour le numéro */
    top: 50%; /* Centrer verticalement */
    left: 50%; /* Centrer horizontalement */
    transform: translate(-50%, -50%); /* Ajuster la position */
    font-size: 1.4rem; /* Taille de la police pour le numéro */
    color: #ffbf00; /* Couleur du numéro */
    font-weight: bold; /* Rendre le numéro plus visible */
  }
  .score-details {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem; /* Plus grande taille de police pour les détails */
  }

  .stars {
    color: #ffd700; /* Couleur des étoiles plus vibrante */
    margin-left: 10px; /* Espacement entre le nom et les étoiles */
  }

</style>
