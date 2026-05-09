import { defineStore } from 'pinia'
import { authAPI } from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || '',
    isLoggedIn: !!localStorage.getItem('token')
  }),
  actions: {
    async login(username, password) {
      const res = await authAPI.login({ username, password })
      this.token = res.token
      this.isLoggedIn = true
      localStorage.setItem('token', res.token)
      await this.fetchUser()
    },
    async register(data) {
      await authAPI.register(data)
    },
    async fetchUser() {
      const res = await authAPI.getUserInfo()
      this.user = res.data
    },
    logout() {
      this.token = ''
      this.user = null
      this.isLoggedIn = false
      localStorage.removeItem('token')
    }
  }
})
