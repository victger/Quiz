<script setup>
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

    // Array to store all promises
    const promises = [];

    // Fetch all questions for each position
    for (let position = 1; position <= totalQuestions; position++) {
      promises.push(quizApiService.getQuestion(position));
    }

    // Wait for all promises to resolve
    const responses = await Promise.all(promises);

    // Extract text from each response and update questions
    questions.value = responses.map(response => response.data.text);

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
      <p>Chargement des questions...</p>
    </div>
  </div>
</template>