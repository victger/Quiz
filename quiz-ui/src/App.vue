<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const token = ref('');
const isAuthenticated = ref(false);
const router = useRouter();

router.beforeEach((to, from, next) => {
  token.value = sessionStorage.getItem('token');
  isAuthenticated.value = !!token.value;
  console.log(token.value)
  console.log(isAuthenticated.value)
  next();
});

function handleHomeClick() {
  if (isAuthenticated.value) {
    sessionStorage.removeItem('token');
    isAuthenticated.value = false;
  }
}

function handleLogoutClick() {
  if (isAuthenticated.value) {
    sessionStorage.removeItem('token');
    isAuthenticated.value = false;
    router.push("/");
  } else {
    router.push("/login");
  }
}

</script>

<template>
  <div class="app">
    <header>
      <nav class="navbar">
        <div class="left-section">
          <img src="./assets/logo.png" alt="Logo CinemaScope" class="logo" />
          <span>CinemaScope</span>
        </div>
        <div class="center-section">
          <RouterLink to="/" class="nav-link" @click="handleHomeClick">Home</RouterLink>
        </div>
        <div class="right-section">
          <RouterLink :to="isAuthenticated ? '/' : '/login'" class="nav-link admin-link" @click="handleLogoutClick">{{ isAuthenticated ? 'Logout' : 'Admin' }}</RouterLink>
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

.nav-link {
  margin: 0 15px;
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

.nav-link:hover {
  color: #650610; /* Couleur d'accent lors du survol */
  transition: color 0.3s ease;
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
</style>
