<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  question: Object
});
const emit = defineEmits(['answer-clicked', 'next-question']);


function answerClickedHandler(answerIndex) {

  emit('answer-clicked', answerIndex);

  
  emit('next-question');
}
</script>

<template>
  <div class="quiz-container">
    <h2 class="quiz-title">{{ question.title }}</h2>
    <p class="question-text">{{ question.text }}</p>
    <img v-if="question.image" class="question-image" :src="question.image" />

    <div class="options-container">
      <button
        type="button"
        class="answer-item"
        v-for="(answer, index) in question.possibleAnswers"
        :key="index"
        @click="answerClickedHandler(index)"
      >
        {{ answer.text }}
      </button>
    </div>
  </div>
</template>

<style>
.quiz-container {
  width: 100%;
  box-sizing: border-box;
  padding: 0 20px;
  /* ... autres styles ... */
}

.quiz-title, .question-text {
  margin: 10px 0;
}

.question-image {
  max-width: 100%;
  max-height: 500px;
  object-fit: contain;
  border-radius: 8px;
  border: 3px solid #333;
  display: block;
  margin: 20px auto;
}

.options-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.answer-item {
  background-color: #f0f0f0;
  margin: 10px 0;
  padding: 10px 20px;
  border-radius: 5px;
  border: 1px solid #ccc; /* Ajout d'une légère bordure pour les boutons */
  cursor: pointer;
  text-align: center;
  width: 100%; /* Optionnel: définissez une largeur maximale si nécessaire */
}

.answer-item:hover {
  background-color: #e9e9e9; /* Un léger changement de fond au survol */
}

/* Vous pouvez retirer .next-button si ce bouton n'est plus utilisé */
</style>
