<script setup>
import { ref } from 'vue';
import participationStorageService from "@/services/ParticipationStorageService";
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');

function launchNewQuiz() {
  participationStorageService.savePlayerName(username.value)
  console.log("Launch new quiz with", username.value);
}

</script>

<template>
  <div class="container mt-3">
    <div class="row">
      <div class="col-12">
        <form>
          <div class="mb-3">
            <label for="usernameInput" class="form-label">Saisissez votre nom :</label>
            <input type="text" class="form-control" id="usernameInput" placeholder="Username" v-model="username"/>
          </div>
          <router-link to="/questions"><button type="submit" class="btn btn-primary" @click="launchNewQuiz">GO!</button></router-link>
        </form>
      </div>
    </div>
  </div>
</template>

<style>

</style>
