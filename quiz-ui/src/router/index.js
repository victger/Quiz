import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import QuestionsManager from '../views/QuestionsManager.vue'
import ScorePage from '../views/ScorePage.vue'
import LoginPage from '../views/LoginPage.vue'
import AdminHomePage from '../views/AdminHomePage.vue'
import CreateQuestionPage from '../views/CreateQuestionPage.vue'
import QuestionDetail from '../views/QuestionDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/new-quiz',
      name: 'new-quiz',
      component: NewQuizPage
    },
    {
      path: '/questions',
      name: 'questions',
      component: QuestionsManager
    },
    {
      path: '/score',
      name: 'score',
      component: ScorePage
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminHomePage
    },
    {
      path: '/create-question',
      name: 'create-question',
      component: CreateQuestionPage
    },
    {
      path: '/question-detail/:position',
      name: 'question-detail',
      component: QuestionDetail,
      props : true
    }
  ]
})

export default router