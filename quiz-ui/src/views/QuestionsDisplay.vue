
<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  currentQuestion: Object
});
const emit = defineEmits(['answer-clicked']);
</script>

<template>
  <div>
    <img v-if="currentQuestion.image" :src="currentQuestion.image" />
    <a @click="emit('answer-clicked', 2)">La réponse D</a>
  </div>
</template>