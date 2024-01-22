<script setup>
import { defineProps, defineEmits, ref, watch } from 'vue';

const props = defineProps({
  question: Object
});
const emit = defineEmits(['answer-clicked', 'next-question']);
const selectedAnswerIndex = ref(null);

watch(() => props.question, () => {
  selectedAnswerIndex.value = null;
});

function answerClickedHandler(answerIndex) {
  selectedAnswerIndex.value = answerIndex;
  emit('answer-clicked', answerIndex);
}
</script>

<template>
  <div>
    <h2>{{ question.title }}</h2>
    <p>{{ question.text }}</p>
    <img v-if="question.image" :src="question.image" />

    <ul style="list-style-type: none; padding: 0;">
      <li v-for="(answer, index) in question.possibleAnswers" :key="index" style="margin-bottom: 10px;">
        <label>
          <input type="radio" :value="index" v-model="selectedAnswerIndex" @click="answerClickedHandler(index)" />
          {{ answer.text }}
        </label>
      </li>
    </ul>

    <button @click="emit('next-question', selectedAnswerIndex)">Suivant</button>
  </div>
</template>