<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <div class="app">
    <header>
      <nav class="navbar">
        <div class="left-section">
          <span>CinemaScope</span>
        </div>
        <div class="center-section">
          <RouterLink to="/" class="nav-link">Home</RouterLink>
        </div>
        <div class="right-section">
          <RouterLink to="/login" class="nav-link admin-link">Admin</RouterLink>
        </div>
      </nav>
    </header>
    
    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<style>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #333;
  color: white;
  width: 100%; 
  box-sizing: border-box;
}

.nav-link {
  margin: 0 10px;
  color: white;
  text-decoration: none;
}

.app-main {
  width: 100%;
  box-sizing: border-box;
  padding: 0 20px;
  /* ... autres styles ... */
}
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* utilise toute la hauteur de la fenêtre de visualisation */
  width: 100%;
}
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}
/* Ajoutez d'autres styles globaux ici si nécessaire */
</style>
