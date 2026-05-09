<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 p-4">
    <div class="bg-white rounded-xl card-shadow p-8 w-full max-w-md fade-in">
      <div class="flex items-center justify-center space-x-2 mb-6">
        <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center">
          <i class="fa fa-paw text-white text-xl"></i>
        </div>
        <span class="text-xl font-bold text-primary">趣学喵</span>
      </div>
      <h2 class="text-xl font-bold text-gray-800 mb-6 text-center">注册账号</h2>
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">用户名 <span class="text-red-500">*</span></label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><i class="fa fa-user text-gray-400"></i></div>
            <input v-model="form.username" type="text" placeholder="请输入用户名" class="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" required />
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">密码 <span class="text-red-500">*</span></label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><i class="fa fa-lock text-gray-400"></i></div>
            <input v-model="form.password" type="password" placeholder="请输入密码" class="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" required />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">手机号</label>
            <input v-model="form.phone" type="text" placeholder="手机号" class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
            <input v-model="form.email" type="email" placeholder="邮箱" class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">身份 <span class="text-red-500">*</span></label>
          <div class="flex gap-3">
            <label class="flex-1 flex items-center justify-center p-3 border rounded-lg cursor-pointer transition-all" :class="form.user_type === 1 ? 'border-primary bg-light text-primary' : 'border-gray-300 text-gray-500'">
              <input type="radio" :value="1" v-model.number="form.user_type" class="sr-only" />
              <i class="fa fa-user mr-2"></i> 我是家长
            </label>
            <label class="flex-1 flex items-center justify-center p-3 border rounded-lg cursor-pointer transition-all" :class="form.user_type === 2 ? 'border-primary bg-light text-primary' : 'border-gray-300 text-gray-500'">
              <input type="radio" :value="2" v-model.number="form.user_type" class="sr-only" />
              <i class="fa fa-graduation-cap mr-2"></i> 我是家教
            </label>
          </div>
        </div>
        <button type="submit" :disabled="loading" class="w-full bg-primary hover:bg-secondary text-white font-medium py-3 rounded-lg transition-colors shadow-md hover:shadow-lg disabled:opacity-60">
          <i class="fa fa-user-plus mr-2"></i>{{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      <p v-if="error" class="text-red-500 text-sm mt-4 text-center">{{ error }}</p>
      <p v-if="success" class="text-green-600 text-sm mt-4 text-center">{{ success }}</p>
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">已有账号？ <router-link to="/login" class="text-primary hover:text-secondary font-medium">去登录</router-link></p>
      </div>
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
  loading.value = true; error.value = ''; success.value = ''
  try { await auth.register({ ...form }); success.value = '注册成功，请登录'; setTimeout(() => router.push('/login'), 1500) }
  catch (e) { error.value = e.response?.data?.msg || '注册失败' }
  finally { loading.value = false }
}
</script>
