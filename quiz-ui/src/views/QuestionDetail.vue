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
  <div>
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
    <div v-else>
      <p>Chargement des détails de la question...</p>
    </div>
  </div>
</template>