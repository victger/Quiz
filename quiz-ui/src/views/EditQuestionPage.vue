<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import { useRouter } from 'vue-router';

const router = useRouter();
const position = ref(0);
const title = ref('');
const text = ref('');
const possibleAnswers = ref([
  { text: '', isCorrect: false },
  { text: '', isCorrect: false },
  { text: '', isCorrect: false },
  { text: '', isCorrect: false }
]);
const imageFile = ref(null);
const imagePreview = ref(null);
const correctAnswerIndex = ref(-1); // -1 means no correct answer selected
const questionId = ref(null);

function handleImageUpload(event) {
  const file = event.target.files[0];

  if (file) {
    imageFile.value = file;

    const reader = new FileReader();
    reader.onload = () => {
      imagePreview.value = reader.result;
    };
    reader.readAsDataURL(file);
  }
}

function setCorrectAnswer(index) {
  correctAnswerIndex.value = index;

  possibleAnswers.value.forEach((answer, i) => {
    if (i !== index) {
      answer.isCorrect = false;
    }
  });
}

async function save() {
  try {
    const questionData = {
      title: title.value,
      text: text.value,
      possibleAnswers: possibleAnswers.value,
      image: imageFile.value ? await convertImageToBase64(imageFile.value) : null,
    };
    await quizApiService.updateQuestion(questionId.value, questionData);

    // router.push('/admin');
  } catch (error) {
    console.error('Error updating question:', error);
  }
}

function convertImageToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      resolve("data:image/jpeg;base64," + reader.result.split(',')[1]);
    };
    reader.onerror = (error) => reject(error);
    reader.readAsDataURL(file);
  });
}

onMounted(async () => {
  // Utiliser props pour récupérer les paramètres de la route
  position.value = router.currentRoute.value.params.position;
  const response = await quizApiService.getQuestion(position.value);
  const questionData = response.data;

  // Assigner les valeurs de la question aux références
  title.value = questionData.title;
  text.value = questionData.text;
  possibleAnswers.value = questionData.possibleAnswers;

  // Afficher l'aperçu de l'image si elle existe
  if (questionData.image) {
    imagePreview.value = questionData.image;
  }
});


</script>

<template>
  <div>
    <h1>Modifier la question</h1>

    <label for="position">Position :</label>
    <input type="number" v-model="position" id="position" disabled />

    <label for="title">Titre :</label>
    <input type="text" v-model="title" id="title" />

    <label for="text">Intitulé :</label>
    <textarea v-model="text" id="text"></textarea>

    <label>Réponses possibles :</label>
    <div v-for="(answer, index) in possibleAnswers" :key="index">
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

    <div v-if="imagePreview">
      <p>Aperçu de l'image :</p>
      <img :src="imagePreview" alt="Image Preview" style="max-width: 300px;" />
    </div>

    <button @click="cancel">Annuler</button>
    <button @click="save">Sauvegarder</button>
  </div>
</template>
