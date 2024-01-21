<script setup>
import { ref } from 'vue';
import quizApiService from "@/services/QuizApiService";
import { useRouter } from "vue-router";

const router = useRouter();
const position = ref(1);
const title = ref('');
const text = ref('');
const possibleAnswers = ref([{ text: '', isCorrect: false }]);

async function save() {
  try {
    const questionData = {
      position: position.value,
      title: title.value,
      text: text.value,
      possibleAnswers: possibleAnswers.value,
      image: "null",
    };
    console.log(questionData)
    // Utilisation du token stocké dans le service QuizApiService
    await quizApiService.saveQuestion(questionData);
    // router.push('/admin');
  } catch (error) {
    console.error('Error saving question:', error);
  }
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
        <input type="text" v-model="possibleAnswers[index].text" />
        <label>
          Réponse correcte
          <input type="checkbox" v-model="possibleAnswers[index].isCorrect" />
        </label>
      </div>
  
      <button @click="cancel">Annuler</button>
      <button @click="save">Sauvegarder</button>
    </div>
  </template>