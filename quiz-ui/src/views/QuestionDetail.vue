<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import quizApiService from "@/services/QuizApiService";

const router = useRouter();
const position = ref(null);
const question = ref(null);
const totalQuestions = ref(0);

onMounted(async () => {
  position.value = router.currentRoute.value.params.position;
  const response = await quizApiService.getQuestion(position.value);
  question.value = response.data;

  const quizInfoResponse = await quizApiService.getQuizInfo();
  totalQuestions.value = quizInfoResponse.data.size;
});

function editQuestion() {
  router.push({ name: 'edit-question', params: { position: position.value } });
}

function goToAdminPage() {
  router.push('/admin');
}

async function deleteQuestion() {
  if (totalQuestions.value > 1 && confirm("Voulez-vous vraiment supprimer cette question?")) {
    try {
      await quizApiService.deleteQuestion(question.value.id);
      router.push('/admin');
    } catch (error) {
      console.error('Erreur lors de la suppression de la question:', error);
    }
  } else {
    alert("Impossible de supprimer la dernière question. Assurez-vous qu'il y a au moins une question dans la base de données.");
  }
}
</script>

<template>
  <div class="page-details">
    <h1>Détails de la question</h1>
    <div v-if="question">
      <h2>Question {{ question.position }} : {{ question.title }}</h2>
      <ul>
        <li>ID : {{ question.id }}</li>
        <li>Position : {{ question.position }}</li>
        <li>Image : <img v-if="question.image" :src="question.image" alt="Image Question" /></li>
        <li>Texte : {{ question.text }}</li>
        <li>Réponses possibles :
          <ul>
            <li v-for="(answer, index) in question.possibleAnswers" :key="index">
              {{ answer.text }} ({{ answer.isCorrect ? 'Correcte' : 'Incorrecte' }})
            </li>
          </ul>
        </li>
      </ul>
      <button @click="editQuestion">Éditer</button>
      <button @click="goToAdminPage">Retour aux questions</button>
      <button @click="deleteQuestion">Supprimer</button>
    </div>
    <div v-else class="loading">
      <p>Chargement des détails de la question...</p>
    </div>
  </div>
</template>

<style>
/* Réutilisation des styles définis pour AdminHomePage */
.page-details {
  font-family: 'Roboto Slab', serif;
  color: #333;
  background: #f5f5f5;
  padding: 2rem;
}

.page-details h1 {
  text-align: center;
  color: #000000;
  font-family: 'Lobster', serif;
  font-weight: 700;
  color: #131006;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.25);
  margin-bottom: 20px;
  font-size: 2.5rem;
}

.page-details h2 {
  color: #650610;
  font-weight: 700;
  margin-bottom: 1rem;
}

.page-details ul {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.page-details li {
  margin-bottom: 0.5rem;
}

.page-details img {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.page-details button {
  background-color: #650610;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  display: block;
  width: 200px;
  margin: 10px auto;
  text-align: center;
  font-weight: bold;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.page-details button:hover {
  background-color: #5e050e;
  color: #d4af37;
}

.loading {
  text-align: center;
}
</style>
