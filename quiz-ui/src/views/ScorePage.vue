<script setup>
import participationStorageService from "@/services/ParticipationStorageService";

const finalScore= participationStorageService.getFinalScore()

</script>

<template>
    <div class="score-page">
      <div class="score-container">
        <h1 class="score-title">Votre Score</h1>
        <p class="score-value">Le score de votre session : <strong>{{ finalScore }}</strong></p>
        <p class="ranking">Votre classement : <em>Compléter le backend</em></p>
      </div>
    </div>
  </template>
  
  <style>
  .score-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    text-align: center;
    padding: 20px;
    background: var(--color-background-soft);
  }
  
  .score-container {
    border: 2px solid #333; /* Couleur de la bordure */
    border-radius: 15px; /* Bords arrondis */
    padding: 2rem; /* Espace à l'intérieur du cadre */
    margin: 2rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Ombre portée optionnelle pour un effet de profondeur */
    background: #ffffff; /* Fond blanc pour le cadre, ou une autre couleur de fond de votre choix */
    max-width: 600px; /* Largeur maximale du cadre pour ne pas étirer le texte sur de grandes largeurs d'écran */
    width: 100%; /* Assurez-vous que le cadre ne dépasse pas les bords de l'écran */
  }
  
  .score-title {
    font-size: 2.5rem;
    color: var(--color-heading);
    margin-bottom: 1rem;
  }
  
  .score-value {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }
  
  .score-value strong {
    color: var(--color-text);
    font-weight: bold;
  }
  
  .ranking {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
  }
  
  .ranking em {
    font-style: italic;
  }
  </style>
  