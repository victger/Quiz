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
          <RouterLink v-if="!authStore.isLoggedIn" to="/login">Admin</RouterLink>
          <button v-else class="nav-link" @click="logout">Déconnexion</button>
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

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #ffffff; /* Fond blanc pour le header */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Ombre portée pour donner de la profondeur */
  color: #333;
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

.app-main {
  padding: 2rem;
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

.cinemascope{
  color: #333;
}
</style>
