<script setup>
import { ref, onMounted, reactive } from 'vue';
import quizApiService from '@/services/QuizApiService';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

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
  questionId: null,
  formErrors: {
    position: false,
    title: false,
    text: false,
    answers: false,
    oneCorrectAnswer: false,
  }
});
const toast = useToast();

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

  const correctAnswersCount = state.possibleAnswers.filter(answer => answer.isCorrect).length;
  
  state.formErrors.oneCorrectAnswer = correctAnswersCount !== 1;
  state.formErrors.position = !state.position;
  state.formErrors.title = !state.title.trim();
  state.formErrors.text = !state.text.trim();
  state.formErrors.answers = state.possibleAnswers.some(answer => !answer.text.trim());
  

  if (Object.values(state.formErrors).some(error => error)) {
    toast.error('Veuillez remplir tous les champs nécessaires.');
    return;
  }

  try {
    const questionData = {
      position : state.position,
      title: state.title,
      text: state.text,
      possibleAnswers: state.possibleAnswers,
      image: state.imageFile ? await convertImageToBase64(state.imageFile) : null
    };
    await quizApiService.updateQuestion(state.questionId, questionData);
    toast.success("Question modifié");
    router.push('/admin');
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
  <div class="container-mt-3">
    <div class="row">
      <div class="col-12">
        <form>
          <h1 class="form-title">Modifier la question</h1>
          
          <div class="mb-3">
            <label for="position" class="form-label">Position :</label>
            <input type="number" v-model="state.position" id="position" class="form-control" min="1" max="10"/>
            <div v-if="state.formErrors.position" class="error-message">Ce champ est requis.</div>
          </div>
          
          <div class="mb-3">
            <label for="title" class="form-label">Titre :</label>
            <input type="text" v-model="state.title" id="title" class="form-control" />
            <div v-if="state.formErrors.title" class="error-message">Ce champ est requis.</div>
          </div>
          
          <div class="mb-3">
            <label for="text" class="form-label">Intitulé :</label>
            <textarea v-model="state.text" id="text" class="form-control"></textarea>
            <div v-if="state.formErrors.text" class="error-message">Ce champ est requis.</div>
          </div>
          
          <label class="form-label">Réponses possibles :</label>
          <div v-for="(answer, index) in state.possibleAnswers" :key="index" class="mb-3">
            <input type="text" v-model="answer.text" class="form-control" />
            <div v-if="state.formErrors.answers && !answer.text" class="error-message">Ce champ est requis.</div>
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
              <div v-if="state.formErrors.oneCorrectAnswer" class="error-message">
                Veuillez sélectionner une seule réponse correcte.
              </div>
            </div>
          </div>
          
          <div class="mb-3">
            <label for="image" class="form-label">Téléverser une image :</label>
            <input type="file" accept="image/*" @change="handleImageUpload" id="image" class="form-control" />
          </div>
          
          <div v-if="state.imagePreview" class="mb-3 image-preview-container">
            <p class="form-label">Aperçu de l'image :</p>
            <img :src="state.imagePreview" alt="Image Preview" style="max-width: 300px;" />
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
  transition: all 0.3s ease-in-out 0s;
}

.btn-save:hover {
  color: #1556b1;
}

.form-title {
  /* Ajoutez des styles pour le titre du formulaire, si nécessaire */
  color: white; /* Text color */
}

.form-check-label {
  /* Ajoutez des styles pour le groupe de boutons, si nécessaire */
  color: white; /* Text color */
}

.error-message {
    color: red;
    font-size: 0.8em;
  }


</style>

