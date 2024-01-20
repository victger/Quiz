  <script setup>
  import { ref, reactive } from 'vue';
  import { useRouter } from 'vue-router';
  import quizApiService from '@/services/QuizApiService';
  
  const router = useRouter();
  
  const position = ref(1);
  const title = ref('');
  const text = ref('');
  const possibleAnswers = ref([{ text: '', isCorrect: false }]);
  const imageUrl = ref('');
  
  function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
      // Assume you have a function to upload the image and get the URL
      uploadImageAndGetUrl(file)
        .then(url => {
          imageUrl.value = url;
        })
        .catch(error => {
          console.error('Error uploading image:', error);
        });
    }
  }
  
  function uploadImageAndGetUrl(file) {
    // Implement your image upload logic here and return the URL
    // For example, you can use a service or an API endpoint
    return new Promise((resolve, reject) => {
      // Simulate image upload success after a short delay
      setTimeout(() => {
        resolve('https://example.com/image.jpg');
      }, 1000);
    });
  }
  
  function cancel() {
    router.push('/admin');
  }
  
  async function save() {
    try {
      const questionData = {
        position: position.value,
        title: title.value,
        text: text.value,
        possibleAnswers: possibleAnswers.value,
        imageUrl: imageUrl.value,
      };
  
      // Assume you have an API service method to save the question
      await quizApiService.saveQuestion(questionData);
  
      // Redirect to the admin page after saving
      router.push('/admin');
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
  
      <label for="image">Upload image :</label>
      <input type="file" @change="handleImageUpload" id="image" accept="image/*" />
  
      <div v-if="imageUrl">
        <p>Aperçu de l'image :</p>
        <img :src="imageUrl" alt="Aperçu de l'image" />
      </div>
  
      <button @click="cancel">Annuler</button>
      <button @click="save">Sauvegarder</button>
    </div>
  </template>