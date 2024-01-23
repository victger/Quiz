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
      <h2><b>Question {{ question.position }} : {{ question.title }}</b></h2>
      <ul>
        <li><b>ID : </b>{{ question.id }}</li>
        <li><b>Position : </b>{{ question.position }}</li>
        <li>
          <div class="image-container">
            <strong>Image :</strong>
            <img v-if="question.image" :src="question.image" alt="Image de la question" />
          </div>
        </li>
        <li><b>Texte : </b>{{ question.text }}</li>
        <li><b>Réponses possibles : </b>
          <ul>
            <li class="answer-list" v-for="(answer, index) in question.possibleAnswers" :key="index">
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
.page-details {
  font-family: 'Roboto Slab', serif;
  color: #333;
  background: #f5f5f5;
  padding: 2rem;
  max-width: 800px; /* Limiter la largeur pour une meilleure lisibilité */
  margin: auto; /* Centrer dans la page */
}

.page-details h1 {
  text-align: center;
  font-family: 'Lobster', serif;
  color: #650610;
  margin-bottom: 1rem;
}

.page-details h2 {
  background-color: #ffffff;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.page-details ul {
  list-style: none;
  padding: 0;
  margin-top: 2rem; /* Ajoutez cette ligne pour l'espacement */
}

.page-details li {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.title-id{
  font-weight: bold;
}

.page-details img {
  max-width: 100%;
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  margin: 1rem 0;
  
}

.page-details button {
  background-color: #650610;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 1rem;
  margin-right: 0.5rem; /* Espacement entre les boutons */
  transition: background-color 0.3s;
}

.page-details button:hover {
  background-color: #5e050e;
  color: #d4af37;
  transition: all 0.3s ease-in-out 0s;
}

.page-details .answer-list {
  margin-top: 0.5rem;
}


.page-details .answer-item {
  background-color: #f5f5f5;
  padding: 0.5rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.page-details .answer-item.correct {
  background-color: #d4f8e8;
}

.page-details .answer-item.incorrect {
  background-color: #ffd4d4;
}

.page-details .answer-list {
  margin-top: 2rem; /* Ajouter plus d'espace au-dessus de la liste des réponses */
}

.image-container strong {
  display: block; /* Rend le titre comme un bloc pour qu'il soit sur sa propre ligne */
  margin-bottom: 0.5rem; /* Ajoute un petit espace sous le titre avant l'image */
}

.image-container img {
  max-width: 100%;
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  /* Supprimez la marge de l'image ici si vous l'avez définie dans .page-details img */
}
</style>

