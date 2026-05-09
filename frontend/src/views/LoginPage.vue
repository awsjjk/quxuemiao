<template>
  <div class="min-h-screen flex flex-col md:flex-row">
    <div class="login-bg md:w-1/2 p-8 flex flex-col justify-center text-white hidden md:flex">
      <div class="max-w-md mx-auto">
        <div class="flex items-center space-x-3 mb-8">
          <div class="w-12 h-12 rounded-full bg-white flex items-center justify-center">
            <i class="fa fa-paw text-primary text-2xl"></i>
          </div>
          <span class="text-2xl font-bold">趣学喵</span>
        </div>
        <h1 class="text-4xl font-bold mb-4 leading-tight">让孩子的学习<br>更有趣、更高效</h1>
        <p class="text-blue-100 mb-8 text-lg">专业家教供需匹配平台，AI 智能推荐最合适的家教</p>
        <div class="space-y-4">
          <div class="flex items-start">
            <div class="bg-white/20 p-2 rounded-full mt-1 mr-4"><i class="fa fa-search"></i></div>
            <div><h3 class="font-semibold text-xl mb-1">AI 智能匹配</h3><p class="text-blue-100">基于需求自动推荐最合适的家教老师</p></div>
          </div>
          <div class="flex items-start">
            <div class="bg-white/20 p-2 rounded-full mt-1 mr-4"><i class="fa fa-check-circle"></i></div>
            <div><h3 class="font-semibold text-xl mb-1">品质保障</h3><p class="text-blue-100">实名认证大学生家教，教学质量有保证</p></div>
          </div>
        </div>
      </div>
    </div>
    <div class="md:w-1/2 p-8 flex flex-col justify-center">
      <div class="max-w-md mx-auto w-full fade-in">
        <div class="md:hidden flex items-center space-x-3 mb-8">
          <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center">
            <i class="fa fa-paw text-white text-xl"></i>
          </div>
          <span class="text-xl font-bold text-primary">趣学喵</span>
        </div>
        <h2 class="text-2xl font-bold text-gray-800 mb-6">欢迎登录</h2>
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">用户名 <span class="text-red-500">*</span></label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><i class="fa fa-user text-gray-400"></i></div>
              <input v-model="username" type="text" placeholder="请输入用户名" class="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" required />
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">密码 <span class="text-red-500">*</span></label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><i class="fa fa-lock text-gray-400"></i></div>
              <input v-model="password" :type="showPwd ? 'text' : 'password'" placeholder="请输入密码" class="w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" required />
              <button type="button" class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600" @click="showPwd = !showPwd">
                <i :class="showPwd ? 'fa fa-eye' : 'fa fa-eye-slash'"></i>
              </button>
            </div>
          </div>
          <div class="pt-2">
            <button type="submit" :disabled="loading" class="w-full bg-primary hover:bg-secondary text-white font-medium py-3 rounded-lg transition-colors shadow-md hover:shadow-lg disabled:opacity-60">
              <i class="fa fa-sign-in mr-2"></i>{{ loading ? '登录中...' : '登录' }}
            </button>
          </div>
        </form>
        <p v-if="error" class="text-red-500 text-sm mt-4 text-center">{{ error }}</p>
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">还没有账号？ <router-link to="/register" class="text-primary hover:text-secondary font-medium">立即注册</router-link></p>
        </div>
      </div>
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
const showPwd = ref(false)
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true; error.value = ''
  try { await auth.login(username.value, password.value); router.push('/dashboard') }
  catch (e) { error.value = e.response?.data?.msg || '登录失败' }
  finally { loading.value = false }
}
</script>
