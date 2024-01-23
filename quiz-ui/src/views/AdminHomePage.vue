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
  router.push({ name: 'question-detail', params: { position: question.position }, query: { question: question } });
}

</script>

<template>
  <div class="page-admin">
    <h1>Page d'Administration</h1>

    <router-link to="/create-question" class="create-question-button">
      Créer une question
    </router-link>

    <div v-if="questions.length">
      <h2>Liste des questions :</h2>
      <ul class="question-list">
        <li
          v-for="question in questions"
          :key="question.position"
          @click="showQuestionDetail(question)"
          class="question-item"
        >
          <b>Question {{ question.position }}  : </b>{{ question.text }}
        </li>
      </ul>
    </div>
    <div v-else class="loading">
      <p>Chargement des questions...</p>
    </div>
  </div>
</template>


<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&display=swap');


.page-admin {
  font-family: 'Roboto Slab', serif;
  color: #333;
  background: #f5f5f5;
  padding: 2rem;
}

.page-admin h1 {
  text-align: center;
  color: #000000;
  font-family: Lobster, serif;
  font-weight: 700; /* Pour une police plus épaisse */
  color: #131006; /* Couleur dorée pour le titre */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.25); /* Ombre de texte plus prononcée pour le titre */
  margin-bottom: 20px;
  font-size: 2.5rem; /* Taille plus grande pour le titre */
}

.create-question-button {
  background-color: #650610;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  display: block;
  width: 200px;
  margin: 1rem auto;
  text-align: center;
  text-decoration: none;
  margin-top: 10px; /* Ajoute un peu d'espace au-dessus du bouton */
  font-weight: bold; /* Rendre le texte du bouton plus visible */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.create-question-button:hover{
  background-color: #5e050e; /* Couleur plus sombre lors du survol */
  transition: background-color 0.3s ease;
  color: #d4af37;
  transition: color 0.3s ease;
}

.question-list {
  list-style-type: none;
  padding: 0;
}

.question-item {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 5px;
  transition: background-color 0.3s ease, transform 0.2s ease;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.question-item:hover {
  background-color: #606060;
  color: white;
  transform: translateY(-2px);
}

.loading {
  text-align: center;
}
</style>
