<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1>注册账号</h1>
      <form @submit.prevent="handleRegister">
        <input v-model="form.username" placeholder="用户名" required />
        <input v-model="form.password" type="password" placeholder="密码" required />
        <input v-model="form.phone" placeholder="手机号" />
        <input v-model="form.email" placeholder="邮箱" />
        <select v-model.number="form.user_type" required>
          <option :value="1">我是家长</option>
          <option :value="2">我是家教</option>
        </select>
        <button :disabled="loading">{{ loading ? '注册中...' : '注册' }}</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>
      <p class="link">已有账号？<router-link to="/login">去登录</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const form = reactive({ username: '', password: '', phone: '', email: '', user_type: 1 })
const loading = ref(false)
const error = ref('')
const success = ref('')

async function handleRegister() {
  loading.value = true
  error.value = ''
  success.value = ''
  try {
    await auth.register({ ...form })
    success.value = '注册成功，请登录'
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    error.value = e.response?.data?.msg || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { display:flex; align-items:center; justify-content:center; min-height:100vh; background:#f5f5f5; }
.auth-card { background:#fff; padding:40px; border-radius:12px; box-shadow:0 2px 12px rgba(0,0,0,0.08); width:360px; text-align:center; }
.auth-card h1 { margin:0 0 20px; color:#2563eb; }
input, select { width:100%; padding:10px; margin-bottom:12px; border:1px solid #d1d5db; border-radius:8px; font-size:14px; box-sizing:border-box; }
button { width:100%; padding:10px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
button:disabled { opacity:0.6; }
.error { color:#dc2626; font-size:13px; }
.success { color:#16a34a; font-size:13px; }
.link { margin-top:16px; font-size:13px; color:#6b7280; }
</style>
