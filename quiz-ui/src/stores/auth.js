
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
  }),
  actions: {
    login(token) {
      sessionStorage.setItem('token', token);
      this.isLoggedIn = true;
    },
    logout() {
      sessionStorage.removeItem('token');
      this.isLoggedIn = false;
    },
    checkAuth() {
      this.isLoggedIn = sessionStorage.getItem('token') !== null;
    },
  },
});
