<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter, RouterLink } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

authStore.checkAuth();

function logout() {
  authStore.logout();
  router.push('/');
}
</script>



<template>
  <div class="app">
    <header>
      <nav class="navbar">
        <div class="left-section">
          <RouterLink to="/" class="nav-link-logo" @click="handleHomeClick">
            <img src="./assets/logo.png" alt="Logo CinemaScope" class="logo" />
            <span class="cinemascope">CinemaScope</span>
          </RouterLink>
        </div>
        <div class="center-section">
          <RouterLink to="/" class="nav-link">Home</RouterLink>
        </div>
        <div>
          <nav class="nav" :class="{ 'navbar-logged-in': authStore.isLoggedIn }">
            <RouterLink v-if="authStore.isLoggedIn" to="/admin" class="nav-link">Admin</RouterLink>
            <RouterLink class="nav-link" v-if="!authStore.isLoggedIn" to="/login">Admin</RouterLink>
            <button v-else class="btn-primary" @click="logout">Déconnexion </button>
          </nav>
          
          
        </div>
      </nav>
    </header>
    
    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  background: #f5f5f5; /* Fond neutre clair */
  color: #333; /* Texte en gris foncé pour une bonne lisibilité */
  font-family: 'Lobster', cursive;
}
/* ... autres styles ... */





.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap; /* Permet aux éléments de passer à la ligne suivante */
  padding: 10px;
  background: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  color: #333;
  /* Autres propriétés existantes */
  min-height: 70px; /* Définissez une hauteur minimale pour votre barre de navigation */
}

/* Lorsque le bouton de déconnexion est présent, augmentez la hauteur du header. */
.navbar-logged-in {
  min-height: 100px; /* Augmentez la hauteur minimale lorsque l'utilisateur est connecté */
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap; /* Permet aux éléments de passer à la ligne suivante */
  padding: 10px;
  background: #ffffff;
  color: #333;
  /* Autres propriétés existantes */
  min-height: 70px; /* Définissez une hauteur minimale pour votre barre de navigation */
}


.btn-primary:hover {
  background-color: #5e050e;
}

/* Assurez-vous que le reste du contenu est correctement espacé par rapport au header élargi. */
.app-main {
  padding-top: 3rem; /* Augmentez le padding supérieur pour l'espace supplémentaire du header */
}


.left-section {
  display: flex;
  align-items: center;
}

.logo {
  height: 60px; /* Ajusté pour une meilleure visibilité */
  width: auto;
  margin-right: 15px;
  border-radius: 30%; /* Moins arrondi que le cercle complet pour une forme plus subtile */
}


html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  background: #f5f5f5; /* Assurez-vous que le fond de body correspond au .app */
}


/* ... autres styles ... */

.nav-link {
  margin: 0 15px;
  text-decoration: none;
  color: #333;
  font-weight: bold;
  position: relative; /* Position relative pour les pseudo-éléments */
  font-size: 1.2rem;
}

.nav-link:before {
  content: '';
  position: absolute;
  width: 100%;
  height: 3px;
  bottom: -5px;
  left: 0;
  background-color: transparent;
  visibility: hidden;
  border-radius: 5px;
  transition: all 0.3s ease-in-out 0s;
}

.nav-link:hover:before {
  visibility: visible;
  background-color: #650610;
}

.nav-link:hover {
  color: #650610; /* Couleur d'accent lors du survol */
  transition: color 0.3s ease;
}

.admin-link:before {
  background-color: #650610; 
}

.admin-link:hover:before {
  background-color: #5e050e;
}

.admin-link {
  font-size: 1.2rem; 
}

.nav-link-logo {
  margin: 0 15px;
  text-decoration: none;
  color: #333;
  font-weight: bold;
  position: relative; /* Position relative pour les pseudo-éléments */
  font-size: 1.2rem;
}

.nav-link-logo:before {
  content: '';
  position: absolute;
  width: 100%;
  height: 3px;
  bottom: -5px;
  left: 0;
  background-color: transparent;
  visibility: visible;
  border-radius: 5px;
  color: #333;
  transition: all 0.3s ease-in-out 0s;
}

.nav-link-logo:hover {
  color: #650610; /* Couleur d'accent lors du survol */
  transition: color 0.3s ease;
}
</style>
