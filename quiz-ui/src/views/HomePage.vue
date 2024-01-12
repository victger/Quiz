<script setup>
import { ref, onMounted } from "vue";
import quizApiService from "@/services/QuizApiService";

onMounted(async () => {
  try {
    // Appel du service getQuizInfo() depuis QuizApiService.js
    const response = await quizApiService.getQuizInfo();

    // Stockage de la valeur adéquate dans registeredScores
    registeredScores.value = response.data.scores; // Assurez-vous que la structure de données est correcte

    console.log("Home page mounted");
  } catch (error) {
    console.error("Error fetching quiz info:", error);
  }
});

</script>

<template>

  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
  {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>

  <p>Test</p>

</template>