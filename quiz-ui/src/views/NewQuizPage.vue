<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const router = useRouter();

function launchNewQuiz() {
  console.log("Launch new quiz with", username.value);
  // Ici, vous stockerez le nom du joueur pour une utilisation ultérieure
  // et vous redirigerez vers la première question du quiz.
  // Par exemple, si vous aviez une route pour la première question, vous pourriez faire :
  router.push({ name: 'new-quiz' });
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
          <button type="submit" class="btn btn-primary" @click="launchNewQuiz">GO!</button>
        </form>
      </div>
    </div>
  </div>
</template>

<style>

</style>
