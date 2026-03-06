import { createRouter, createWebHistory } from 'vue-router'
import KnowledgeBase from '../views/KnowledgeBase.vue'
import Chat from '../views/Chat.vue'

const routes = [
  { path: '/', redirect: '/chat' },
  { path: '/knowledge-base', name: 'KnowledgeBase', component: KnowledgeBase },
  { path: '/chat', name: 'Chat', component: Chat }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
