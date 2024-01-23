<script setup>
import { ref, reactive } from 'vue';
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

const formErrors = reactive({
  position: false,
  title: false,
  text: false,
  answers: false,
  image: false,
  oneCorrectAnswer: false,
});

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

  const correctAnswersCount = possibleAnswers.value.filter(answer => answer.isCorrect).length;

  formErrors.position = !position.value;
  formErrors.title = !title.value.trim();
  formErrors.text = !text.value.trim();
  formErrors.answers = possibleAnswers.value.some(answer => !answer.text.trim());
  formErrors.image = !imageFile.value; 
  formErrors.oneCorrectAnswer = correctAnswersCount !== 1;
  

  if (formErrors.position || formErrors.title || formErrors.text || formErrors.answers || formErrors.image || formErrors.oneCorrectAnswer ) {
    toast.error("Veuillez remplir tous les champs nécessaires.");
    return;
  }


  try {
    const questionData = {
      position: position.value,
      title: title.value,
      text: text.value,
      possibleAnswers: possibleAnswers.value,
      image: imageFile.value ? await convertImageToBase64(imageFile.value) : null,
    };

    const response = await quizApiService.saveQuestion(questionData);

    if (response.status === 200) {
      toast.success("Question ajouté");
      router.push('/admin');
    } else {
      toast.error("You can not add more than 10 questions.");
    }
  } catch (error) {
    toast.error("Error occured during saving question.");
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
            <input type="number" v-model="position" id="position" class="form-control" min="1" max="10"/>
            <div v-if="formErrors.position" class="error-message">Ce champ est requis.</div>
          </div>
          
          <div class="mb-3">
            <label for="title" class="form-label">Titre :</label>
            <input type="text" v-model="title" id="title" class="form-control" />
            <div v-if="formErrors.title" class="error-message">Ce champ est requis.</div>
          </div>
          
          <div class="mb-3">
            <label for="text" class="form-label">Intitulé :</label>
            <textarea v-model="text" id="text" class="form-control"></textarea>
            <div v-if="formErrors.text" class="error-message">Ce champ est requis.</div>
          </div>
          
          <label class="form-label">Réponses possibles :</label>
          <div v-for="(answer, index) in possibleAnswers" :key="index" class="mb-3">
            <input type="text" v-model="answer.text" class="form-control" />
            <div v-if="formErrors.answers && !answer.text" class="error-message">Ce champ est requis.</div>
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
              <div v-if="formErrors.oneCorrectAnswer" class="error-message">
                Veuillez sélectionner une seule réponse correcte.
              </div>
            </div>
          </div>
          
          <div class="mb-3">
            <label for="image" class="form-label">Téléverser une image :</label>
            <input type="file" accept="image/*" @change="handleImageUpload" id="image" class="form-control" />
            <div v-if="formErrors.image" class="error-message">Veuillez sélectionner une image.</div>
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

.error-message {
    color: rgb(252, 46, 46);
    font-size: 0.8em;
  }

</style>