<script setup>
import { ref, onMounted } from "vue";
import participationStorageService from "@/services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";

const finalScore = ref(0);
const registeredScores = ref([]);
const playerRanking = ref(null);
const totalParticipants = ref(0);

onMounted(async () => {
  finalScore.value = participationStorageService.getFinalScore();
  try {
    const response = await quizApiService.getQuizInfo();
    if (Array.isArray(response.data.scores)) {
      registeredScores.value = response.data.scores;

      const playerScoreEntry = registeredScores.value.findIndex(
        (scoreEntry) => parseFloat(scoreEntry.score) === parseFloat(finalScore.value)
      );

      playerRanking.value = playerScoreEntry !== -1 ? playerScoreEntry + 1 : null;
      totalParticipants.value = registeredScores.value.length;

      console.log("Player Ranking:", playerRanking.value);
    } else {
      console.error("Invalid data structure for scores:", response.data);
    }
  } catch (error) {
    console.error("Error fetching quiz info:", error);
  }
});
</script>

<template>
  <div class="score-page">
    <div class="score-container">
      <h1 class="score-title">Votre Score</h1>
      <p class="score-value">Le score de votre session : <strong>{{ finalScore }}</strong></p>

      <p class="ranking" v-if="playerRanking !== null">
        Votre classement : <em>{{ playerRanking }} / {{totalParticipants}}</em>
      </p>
      <p class="ranking" v-else>
        Votre classement : <em>Non disponible</em>
      </p>

      <ul class="score-list">
        <p>Les meilleurs scores</p>
        <li v-for="scoreEntry in registeredScores" :key="scoreEntry.date" class="score-item">
          {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style>
.score-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
  padding: 20px;
  background: var(--color-background-soft);
}

.score-container {
  border: 2px solid #333; /* Couleur de la bordure */
  border-radius: 15px; /* Bords arrondis */
  padding: 2rem; /* Espace à l'intérieur du cadre */
  margin: 2rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Ombre portée optionnelle pour un effet de profondeur */
  background: #ffffff; /* Fond blanc pour le cadre, ou une autre couleur de fond de votre choix */
  max-width: 600px; /* Largeur maximale du cadre pour ne pas étirer le texte sur de grandes largeurs d'écran */
  width: 100%; /* Assurez-vous que le cadre ne dépasse pas les bords de l'écran */
}

.score-title {
  font-size: 2.5rem;
  color: var(--color-heading);
  margin-bottom: 1rem;
}

.score-value {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.score-value strong {
  color: var(--color-text);
  font-weight: bold;
}

.ranking {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.ranking em {
  font-style: italic;
}
</style>
