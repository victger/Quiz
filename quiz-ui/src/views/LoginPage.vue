<script setup>
import { ref } from 'vue';
import quizApiService from "@/services/QuizApiService";
import { useRouter } from "vue-router";

const password = ref('');
const router = useRouter();

async function login() {
  try {
    const response = await quizApiService.postLogin(password.value);
    console.log(password.value);
    console.log(response);
  } catch (error) {
    console.error("Erreur lors de la connexion :", error);
  }
}
</script>

<template>
  <div class="login-page">
    <h2>Page de connexion administrateur</h2>
    <form @submit.prevent="login">
      <label for="password">Password:</label>
      <input type="password" v-model="password" id="password" placeholder="Password"/>
      <button type="submit">Connexion</button>
    </form>
  </div>
</template>

<style scoped>
.login-page {
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

label {
  margin-bottom: 10px;
}

input {
  padding: 10px;
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>