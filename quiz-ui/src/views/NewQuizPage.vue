<script setup>
import { ref } from 'vue';
import participationStorageService from "@/services/ParticipationStorageService";
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');

function launchNewQuiz() {
  participationStorageService.savePlayerName(username.value);
}

</script>

<template>
  <div class="container-mt-3">
    <div class="row">
      <div class="col-12">
        <form>
          <div class="mb-3">
            <label for="usernameInput" class="form-label">Saisissez votre nom :</label>
            <input type="text" class="form-control" id="usernameInput" placeholder="Username" v-model="username"/>
          </div>
          <router-link to="/questions"><button type="submit" class="btn-primary" @click="launchNewQuiz">GO!</button></router-link>
        </form>
      </div>
    </div>
  </div>
</template>


<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Nunito:wght@400&display=swap');

.container-mt-3 {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Utilisez toute la hauteur de la fenêtre */
  padding: 2rem;
  background: #f5f5f5; /* Fond global de la page */
}

.row {
  background: #7b2a3b; /* Fond rouge du conteneur du formulaire */
  padding: 2rem;
  border-radius: 15px; /* Bords arrondis */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Ombre portée pour donner de la profondeur */
  max-width: 400px; /* Largeur maximale du conteneur */
  width: 100%; /* S'adapte à la largeur de la fenêtre */
}

.mb-3 {
  margin-bottom: 1rem;
}

.form-control {
  width: 100%; /* Utilisez la pleine largeur du conteneur */
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #e1e1e1; /* Bordure subtile */
  border-radius: 5px; /* Bords arrondis pour l'input */
}

.btn-primary {
  display: block; /* Afficher le lien comme un bloc pour appliquer une largeur */
  width: 100%; /* Utilisez la pleine largeur du conteneur */
  padding: 0.5rem 0; /* Padding vertical sans padding horizontal */
  background-color: #d4af37; /* Couleur du bouton */
  color: white;
  border-radius: 5px; /* Bords arrondis pour le bouton */
  transition: background-color 0.3s ease;
  text-decoration: none; /* Supprime le soulignement du lien */
  font-family: 'Nunito', sans-serif;
}

.form-label{
  color: #ffffff; /* Fond clair pour les items */
  font-family: 'Nunito', sans-serif;
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
  transition: background-color 0.3s ease; /* Transition pour l'interaction */
}

.form-control{
  color: #ffffff; /* Fond clair pour les items */
  font-family: 'Nunito', sans-serif;
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
  transition: background-color 0.3s ease; /* Transition pour l'interaction */
}

</style>
