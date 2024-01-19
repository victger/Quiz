<script setup>
import participationStorageService from "@/services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const questions = ref([]);

onMounted(async () => {
  try {
    // Fetch the total number of questions
    const response = await quizApiService.getQuizInfo();
    const totalQuestions = response.data.size;

    // Fetch all questions for each position
    for (let position = 1; position <= totalQuestions; position++) {
      const response = await quizApiService.getQuestion(position);
      questions.value.push(response.data.text);
    }

    console.log("Questions texts:", questions.value);
  } catch (error) {
    console.error("Error fetching questions:", error);
  }
});
</script>

<template>
  <div>
    <h1>Page d'Administration</h1>

    <!-- Bouton pour créer une nouvelle question -->
    <router-link to="/create-question">
      <button>Créer une question</button>
    </router-link>

    <!-- Display the list of questions -->
    <div v-if="questions.length">
      <h2>Liste des questions :</h2>
      <ul>
        <li v-for="(text, index) in questions" :key="index">
          Intitulé Question {{ index + 1 }} : {{ text }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Aucune question disponible.</p>
    </div>
  </div>
</template>
