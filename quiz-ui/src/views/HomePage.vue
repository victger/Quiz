<script setup>
import { ref, onMounted } from "vue";
import quizApiService from "@/services/QuizApiService";

onMounted(async () => {
  console.log("Home page mounted");
});

const registeredScores = ref([]);
</script>

<template>
  <h1>Home page</h1>
</template>
