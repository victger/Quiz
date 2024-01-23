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


.container-mt-3 {
  /* Vos styles de container-mt-3 ici, similaires à NewQuizPage */
  display: flex;
  justify-content: center;
  align-items: start; /* Aligns items to the start of the container */
  padding-top: 10vh; /* Pushes the container down from the top */
  height: 90vh; /* Takes up less height to move up the content */
  background: #f5f5f5; /* Background color of the page */
}

.row {
  /* Vos styles de row ici, similaires à NewQuizPage */
  background: #7b2a3b; /* Background color of the form container */
  padding: 2rem;
  border-radius: 15px; /* Rounded corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Adds depth with shadow */
  max-width: 400px; /* Maximum width of the container */
  width: 100%; /* Adjusts to the width of the viewport */
  margin-top: -5vh; /* Negative margin to move the container higher */
}

.mb-3 {
  /* Vos styles de mb-3 ici, similaires à NewQuizPage */
  margin-bottom: 1rem;
}

.form-control {
  /* Vos styles de form-control ici, similaires à NewQuizPage */
  width: 100%; /* Full width of the container */
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #e1e1e1; /* Subtle border */
  border-radius: 5px; /* Rounded corners for the input field */
  background-color: rgba(255, 255, 255, 0.8); /* Slightly transparent white */
  color: #333; /* Dark text for readability */
  font-family: 'Merriweather', sans-serif;
}

.btn-primary, .btn-cancel, .btn-save {
  /* Vos styles de bouton ici, adaptés pour les différents boutons */
  display: block; /* Block display to fill the width */
  width: auto; /* Auto width based on content */
  padding: 0.5rem 1rem; /* Smaller padding for a smaller button */
  margin: 0 auto; /* Center the button */
  margin-top: 1rem; /* Space above the button */
  background-color: #d4af37; /* Button color */
  color: white; /* Text color */
  border: none; /* No border */
  border-radius: 5px; /* Rounded corners */
  text-align: center; /* Center text within the button */
  text-decoration: none; /* Removes underline */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Subtle shadow for depth */
}

.form-title {
  /* Ajoutez des styles pour le titre du formulaire, si nécessaire */
  color: white; /* Text color */
}

.form-check-label {
  /* Ajoutez des styles pour le groupe de boutons, si nécessaire */
  color: white; /* Text color */
}

</style>