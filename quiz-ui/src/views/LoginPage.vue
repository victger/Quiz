<script setup>
import { ref } from 'vue';
import quizApiService from "@/services/QuizApiService";
import { useRouter } from "vue-router";
import { useAuthStore } from '@/stores/auth';


const password = ref('');
const errorMessage = ref('');
const router = useRouter();
const authStore = useAuthStore();

async function login() {
  const response = await quizApiService.postLogin(password.value);

  if (response.status === 200 && response.data.token) {
    // Stocker le token dans le service QuizApiService
    quizApiService.setToken(response.data.token);
    authStore.login(response.data.token);
    router.push('/admin');
  } else {
    // Afficher un message d'erreur
    errorMessage.value = "Mot de passe incorrect";
  }
}
</script>

<template>
  <div class="login-page">
    <h2>Page de connexion administrateur</h2>
    <form @submit.prevent="login">
      <input type="password" class = "password-text" v-model="password" id="password" placeholder="Password"/>
      <button type="submit" class="connexion-btn">Connexion</button>
    </form>
      <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap');
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

.connexion-btn {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.connexion-btn:hover {
  background-color: #0355ad; /* Couleur plus sombre lors du survol */
  transition: background-color 0.3s ease;
}

.password-text{
  font-family: Merriweather;
}

p {
  color: red;
}
</style>