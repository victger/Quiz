export default {
    clear() {
      window.localStorage.removeItem("playerName");
      window.localStorage.removeItem("participationScore");
    },
    savePlayerName(playerName) {
      window.localStorage.setItem("playerName", playerName);
    },
    getPlayerName() {
      return window.localStorage.getItem("playerName");
    },
    saveParticipationScore(participationScore) {
      window.localStorage.setItem("participationScore", participationScore);
    },
    getParticipationScore() {
      return window.localStorage.getItem("participationScore");
    },
    saveFinalScore(finalScore) {
      window.localStorage.setItem("finalScore", finalScore);
    },
    getFinalScore() {
      return window.localStorage.getItem("finalScore");
    }
  };
  