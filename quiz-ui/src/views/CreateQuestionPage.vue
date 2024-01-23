<script setup>
import { ref } from 'vue';
import quizApiService from "@/services/QuizApiService";
import { useRouter } from "vue-router";
import { useToast } from 'vue-toastification';

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
const correctAnswerIndex = ref(-1); 
const toast = useToast();

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

    // Utilisation du token stocké dans le service QuizApiService
    await quizApiService.saveQuestion(questionData);

    router.push('/admin');
  } catch (error) {
    if (error.response && error.response.status === 400 ) {
      toast.error("Impossible d'ajouter plus de 10 questions !");
    } else {
      toast.error("Une erreur est survenue.");
    }
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
  <div class="container-mt-3">
    <div class="row">
      <div class="col-12">
        <form>
          <h1 class="form-title">Créer une question</h1>
          
          <div class="mb-3">
            <label for="position" class="form-label">Position :</label>
            <input type="number" v-model="position" id="position" class="form-control" />
          </div>
          
          <div class="mb-3">
            <label for="title" class="form-label">Titre :</label>
            <input type="text" v-model="title" id="title" class="form-control" />
          </div>
          
          <div class="mb-3">
            <label for="text" class="form-label">Intitulé :</label>
            <textarea v-model="text" id="text" class="form-control"></textarea>
          </div>
          
          <label class="form-label">Réponses possibles :</label>
          <div v-for="(answer, index) in possibleAnswers" :key="index" class="mb-3">
            <input type="text" v-model="answer.text" class="form-control" />
            <div class="form-check">
              <input
                type="checkbox"
                v-model="answer.isCorrect"
                @change="setCorrectAnswer(index)"
                class="form-check-input"
                :id="'correct-' + index"
              />
              <label class="form-check-label" :for="'correct-' + index">
                Réponse correcte
              </label>
            </div>
          </div>
          
          <div class="mb-3">
            <label for="image" class="form-label">Téléverser une image :</label>
            <input type="file" accept="image/*" @change="handleImageUpload" id="image" class="form-control" />
          </div>
          
          <div v-if="imagePreview" class="mb-3 image-preview-container">
            <p class="form-label">Aperçu de l'image :</p>
            <img :src="imagePreview" alt="Image Preview" class="image-preview" style="max-width: 300px;"/>
          </div>
          
          <div class="button-group">
            <router-link to="/admin" class="btn-cancel">Annuler</router-link>
            <button type="button" class="btn-save" @click="save">Sauvegarder</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style>

@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap');


</style>