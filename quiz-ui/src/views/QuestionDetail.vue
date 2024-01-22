<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const question = ref(null);

onMounted(() => {
  // Utiliser props pour récupérer les paramètres de la route
  question.value = router.currentRoute.value.params.id;
});
</script>

<template>
  <div>
    <h1>Détails de la question</h1>
    <div v-if="question">
      <h2>Question {{ question }} : {{ question.text }}</h2>
      <!-- Afficher d'autres détails de la question -->
    </div>
    <div v-else>
      <p>Chargement des détails de la question...</p>
    </div>
  </div>
</template>