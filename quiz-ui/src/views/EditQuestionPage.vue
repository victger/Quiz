<script setup>
import { ref, onMounted, reactive } from 'vue';
import quizApiService from '@/services/QuizApiService';
import { useRouter } from 'vue-router';

const router = useRouter();
const state = reactive({
  position: 0,
  title: '',
  text: '',
  possibleAnswers: [
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false }
  ],
  imageFile: null,
  imagePreview: null,
  correctAnswerIndex: -1,
  questionId: null
});

onMounted(async () => {
  // Utiliser props pour récupérer les paramètres de la route
  state.position = router.currentRoute.value.params.position;
  const response = await quizApiService.getQuestion(state.position);
  const questionData = response.data;
  state.position= questionData.position;
  state.questionId = questionData.id;

  // Assigner les valeurs de la question aux références
  state.title = questionData.title;
  state.text = questionData.text;
  state.possibleAnswers = questionData.possibleAnswers;

  // Afficher l'aperçu de l'image si elle existe
  if (questionData.image) {
    state.imagePreview = questionData.image;
  }
});

function handleImageUpload(event) {
  const file = event.target.files[0];

  if (file) {
    state.imageFile = file;

    const reader = new FileReader();
    reader.onload = () => {
      state.imagePreview = reader.result;
    };
    reader.readAsDataURL(file);
  }
}

function setCorrectAnswer(index) {
  state.correctAnswerIndex = index;

  state.possibleAnswers.forEach((answer, i) => {
    if (i !== index) {
      answer.isCorrect = false;
    }
  });
}

async function save() {
  try {
    const questionData = {
      position : state.position,
      title: state.title,
      text: state.text,
      possibleAnswers: state.possibleAnswers,
      image: state.imageFile ? await convertImageToBase64(state.imageFile) : "false"
    };
    await quizApiService.updateQuestion(state.questionId, questionData);
    console.log(questionData);
    // router.push('/admin');
  } catch (error) {
    console.error('Error updating question:', error);
  }
}

function convertImageToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      resolve('data:image/jpeg;base64,' + reader.result.split(',')[1]);
    };
    reader.onerror = (error) => reject(error);
    reader.readAsDataURL(file);
  });
}
</script>

<template>
  <div>
    <h1>Modifier la question</h1>

    <label for="position">Position :</label>
    <input type="number" v-model="state.position" id="position" />

    <label for="title">Titre :</label>
    <input type="text" v-model="state.title" id="title" />

    <label for="text">Intitulé :</label>
    <textarea v-model="state.text" id="text"></textarea>

    <label>Réponses possibles :</label>
    <div v-for="(answer, index) in state.possibleAnswers" :key="index">
      <input type="text" v-model="answer.text" />
      <label>
        Réponse correcte
        <input
          type="checkbox"
          v-model="answer.isCorrect"
          @change="setCorrectAnswer(index)"
        />
      </label>
    </div>

    <label for="image">Téléverser une image :</label>
    <input type="file" accept="image/*" @change="handleImageUpload" id="image" />

    <div v-if="state.imagePreview">
      <p>Aperçu de l'image :</p>
      <img :src="state.imagePreview" alt="Image Preview" style="max-width: 300px;" />
    </div>

    <button @click="cancel">Annuler</button>
    <button @click="save">Sauvegarder</button>
  </div>
</template>