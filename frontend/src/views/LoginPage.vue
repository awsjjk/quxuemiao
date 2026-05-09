<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1>趣学喵</h1>
      <p class="subtitle">天津市家教供需匹配平台</p>
      <form @submit.prevent="handleLogin">
        <input v-model="username" placeholder="用户名" required />
        <input v-model="password" type="password" placeholder="密码" required />
        <button :disabled="loading">{{ loading ? '登录中...' : '登录' }}</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
      <p class="link">还没有账号？<router-link to="/register">立即注册</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await auth.login(username.value, password.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.msg || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { display:flex; align-items:center; justify-content:center; min-height:100vh; background:#f5f5f5; }
.auth-card { background:#fff; padding:40px; border-radius:12px; box-shadow:0 2px 12px rgba(0,0,0,0.08); width:360px; text-align:center; }
.auth-card h1 { margin:0 0 4px; color:#2563eb; }
.subtitle { color:#6b7280; font-size:13px; margin-bottom:24px; }
input { width:100%; padding:10px; margin-bottom:12px; border:1px solid #d1d5db; border-radius:8px; font-size:14px; box-sizing:border-box; }
button { width:100%; padding:10px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
button:disabled { opacity:0.6; }
.error { color:#dc2626; font-size:13px; margin-top:8px; }
.link { margin-top:16px; font-size:13px; color:#6b7280; }
</style>
