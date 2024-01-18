<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  
  <header>
    <div class="navbar">
      <div class="left-section">
        <span>Texte à gauche</span>
      </div>
      <div class="center-section">
        <RouterLink to="/">Accueil</RouterLink>
      </div>
      <div class="right-section">
        <RouterLink to="/login">Administration</RouterLink>
      </div>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  width: 100%;
  background-color: #333; /* Couleur de fond de la barre de navigation */
  color: white; /* Couleur du texte */
  padding: 1rem 0; /* Espace interne en haut et en bas */
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px; /* Largeur maximale de la barre de navigation */
  margin: 0 auto; /* Centrer la barre de navigation horizontalement */
}

.left-section, .center-section, .right-section {
  display: flex;
  align-items: center;
}

.left-section span {
  margin-right: 1rem;
}
</style>