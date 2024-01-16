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

    console.log(response.data.scores);
  } catch (error) {
    console.error("Error fetching quiz info:", error);
  }
});

</script>

<template>
  <div v-for="scoreEntry in registeredScores" :key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>

  <router-link to="/new-quiz">Démarrer</router-link>
</template>