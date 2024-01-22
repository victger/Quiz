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
  <div>
    <h2>{{ question.title }}</h2>
    <p>{{ question.text }}</p>
    <img v-if="question.image" :src="question.image" />

    <div class="options-container">
      <button
        type="button"
        v-for="(answer, index) in question.possibleAnswers"
        :key="index"
        @click="answerClickedHandler(index)"
      >
        {{ answer.text }}
      </button>
    </div>

   
  </div>
</template>