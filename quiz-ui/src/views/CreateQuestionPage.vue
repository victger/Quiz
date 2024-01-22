<script setup>
import { ref } from 'vue';
import quizApiService from "@/services/QuizApiService";
import { useRouter } from "vue-router";

const router = useRouter();
const position = ref(1);
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

function handleImageUpload(event) {
  const file = event.target.files[0];

  if (file) {
    // Stocker le fichier dans la référence imageFile
    imageFile.value = file;

    // Afficher un aperçu de l'image
    const reader = new FileReader();
    reader.onload = () => {
      imagePreview.value = reader.result;
    };
    reader.readAsDataURL(file);
  }
}

function setCorrectAnswer(index) {
  correctAnswerIndex.value = index;
  // Décocher toutes les autres checkboxes
  possibleAnswers.value.forEach((answer, i) => {
    if (i !== index) {
      answer.isCorrect = false;
    }
  });
}

async function save() {
  try {
    const questionData = {
      position: position.value,
      title: title.value,
      text: text.value,
      possibleAnswers: possibleAnswers.value,
      image: imageFile.value ? await convertImageToBase64(imageFile.value) : null,
    };

    console.log(questionData);

    // Utilisation du token stocké dans le service QuizApiService
    await quizApiService.saveQuestion(questionData);

    router.push('/admin');
  } catch (error) {
    console.error('Error saving question:', error);
  }
}

function convertImageToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      resolve("data:image/jpeg;base64,"+reader.result.split(',')[1]);
    };
    reader.onerror = (error) => reject(error);
    reader.readAsDataURL(file);
  });
}
</script>

<template>
  <div>
    <h1>Créer une question</h1>

    <label for="position">Position :</label>
    <input type="number" v-model="position" id="position" />

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