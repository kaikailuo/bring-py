import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  
  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const userRole = computed(() => user.value?.role || 'guest')
  const userName = computed(() => user.value?.name || '访客')
  
  // 方法
  const login = (userData, userToken) => {
    user.value = userData
    token.value = userToken
    localStorage.setItem('token', userToken)
    localStorage.setItem('user', JSON.stringify(userData))
  }
  
  const logout = () => {
    user.value = null
    token.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
  
  const initializeUser = () => {
    const savedUser = localStorage.getItem('user')
    if (savedUser && token.value) {
      try {
        user.value = JSON.parse(savedUser)
      } catch (error) {
        console.error('Failed to parse saved user data:', error)
        logout()
      }
    }
  }
  
  const updateUser = (userData) => {
    user.value = { ...user.value, ...userData }
    localStorage.setItem('user', JSON.stringify(user.value))
  }
  
  return {
    user,
    token,
    isLoggedIn,
    userRole,
    userName,
    login,
    logout,
    initializeUser,
    updateUser
  }
})
