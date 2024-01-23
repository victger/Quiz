<script setup>
import { ref, onMounted } from 'vue';
import participationStorageService from "@/services/ParticipationStorageService";
import { useRouter } from 'vue-router';
import axios from 'axios'; 

const router = useRouter();
const username = ref('');
const errorMessage = ref('');

async function isUsernameUnique(username) {
  try {
    const response = await axios.post('http://127.0.0.1:5000//check-username', { playerName: username });
    return response.data.isUnique;
  } catch (error) {
    console.error('Erreur lors de la vérification du nom d’utilisateur:', error);
    return false; 
  }
}

async function launchNewQuiz() {
  if (username.value.trim() === '') {
    errorMessage.value = "Vous devez entrer un username.";
  } else if (!(await isUsernameUnique(username.value))) {
    errorMessage.value = 'Ce nom d’utilisateur est déjà pris.';
  } else {
    errorMessage.value = ''; 
    participationStorageService.savePlayerName(username.value);
    router.push('/questions');
  }
}

</script>

<template>
  <div class="container-mt-3">
    <div class="row">
      <div class="col-12">
        <form @submit.prevent="launchNewQuiz">
          <div class="mb-3">
            <label for="usernameInput" class="form-label">Saisissez votre nom :</label>
            <input type="text" class="form-control" id="usernameInput" placeholder="Username" v-model="username"/>
            <p class="text-danger">{{ errorMessage }}</p>
          </div>
          <button type="button" class="btn-primary" @click="launchNewQuiz">GO!</button>
        </form>
      </div>
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Nunito:wght@400&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap');

.container-mt-3 {
  display: flex;
  justify-content: center;
  align-items: start; /* Aligns items to the start of the container */
  padding-top: 10vh; /* Pushes the container down from the top */
  height: 90vh; /* Takes up less height to move up the content */
  background: #f5f5f5; /* Background color of the page */
}

.row {
  background: #7b2a3b; /* Background color of the form container */
  padding: 2rem;
  border-radius: 15px; /* Rounded corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Adds depth with shadow */
  max-width: 400px; /* Maximum width of the container */
  width: 100%; /* Adjusts to the width of the viewport */
  margin-top: -5vh; /* Negative margin to move the container higher */
}

.mb-3 {
  margin-bottom: 1rem;
}

.form-control {
  width: 100%; /* Full width of the container */
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #e1e1e1; /* Subtle border */
  border-radius: 5px; /* Rounded corners for the input field */
  background-color: rgba(255, 255, 255, 0.8); /* Slightly transparent white */
  color: #333; /* Dark text for readability */
  font-family: 'Merriweather', sans-serif;
}

.form-label {
  color: #fff; /* White text color for the label */
}

/* Additional styles for other states like hover, active, etc. may be required */

</style>
