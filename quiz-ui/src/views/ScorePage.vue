<script setup>
import participationStorageService from "@/services/ParticipationStorageService";

const finalScore= participationStorageService.getFinalScore()

</script>

<template>
    
<p>Le score de votre session : {{ finalScore }} </p>

<p>Votre classement : Compléter le backend</p>

</template>