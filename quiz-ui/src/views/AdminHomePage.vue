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
    questions.value = responses.map(response => response.data);
  } catch (error) {
    console.error("Error fetching questions:", error);
  }
});

function showQuestionDetail(question) {
  router.push({ name: 'question-detail', params: { id: question.position }, query: { question: question } });
}

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
        <li v-for="question in questions" :key="question.position" @click="showQuestionDetail(question)">
          Intitulé Question {{ question.position }} : {{ question.text }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Chargement des questions...</p>
    </div>
  </div>
</template>
