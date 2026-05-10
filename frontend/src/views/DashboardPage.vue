<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航栏 -->
    <header class="bg-white nav-shadow fixed w-full top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-3">
          <div class="flex items-center space-x-2">
            <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center">
              <i class="fa fa-paw text-white text-xl"></i>
            </div>
            <span class="text-xl font-bold text-primary">趣学喵</span>
          </div>
          <nav class="hidden md:flex items-center space-x-6 text-sm">
            <a class="text-secondary font-medium cursor-pointer">首页</a>
            <a @click="$router.push('/order/0')" class="text-gray-600 hover:text-primary cursor-pointer">我的订单</a>
            <a @click="$router.push('/profile')" class="text-gray-600 hover:text-primary cursor-pointer">个人信息</a>
          </nav>
          <div class="flex items-center space-x-3">
            <span class="text-sm text-gray-600 hidden sm:inline">{{ auth.user?.username }} ({{ roleText }})</span>
            <button @click="handleLogout" class="text-sm bg-red-50 text-red-500 hover:bg-red-100 px-3 py-1.5 rounded-lg transition-colors">
              <i class="fa fa-sign-out mr-1"></i>退出
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-16">
      <div class="flex flex-col lg:flex-row gap-6">

        <!-- 左侧边栏 -->
        <aside class="lg:w-1/5 w-full">
          <div class="bg-white rounded-lg card-shadow p-4 sticky top-24">
            <h3 class="text-sm font-semibold text-primary mb-3 flex items-center"><i class="fa fa-th-large mr-2"></i>快捷功能</h3>
            <ul class="space-y-1 text-sm">
              <li><a @click="showForm = !showForm" class="flex items-center px-3 py-2 rounded-md hover:bg-light text-gray-700 cursor-pointer transition-colors"><i class="fa fa-plus-circle w-5 text-center mr-3 text-gray-500"></i>发布需求</a></li>
              <li><a @click="$router.push('/order/0')" class="flex items-center px-3 py-2 rounded-md hover:bg-light text-gray-700 cursor-pointer transition-colors"><i class="fa fa-list-alt w-5 text-center mr-3 text-gray-500"></i>我的订单</a></li>
              <li><a @click="$router.push('/profile')" class="flex items-center px-3 py-2 rounded-md hover:bg-light text-gray-700 cursor-pointer transition-colors"><i class="fa fa-user-circle w-5 text-center mr-3 text-gray-500"></i>个人信息</a></li>
              <li><a @click="$router.push('/messages')" class="flex items-center px-3 py-2 rounded-md hover:bg-light text-gray-700 cursor-pointer transition-colors"><i class="fa fa-envelope w-5 text-center mr-3 text-gray-500"></i>消息</a></li>
              <li><a @click="$router.push('/resources')" class="flex items-center px-3 py-2 rounded-md hover:bg-light text-gray-700 cursor-pointer transition-colors"><i class="fa fa-book w-5 text-center mr-3 text-gray-500"></i>教学资源</a></li>
              <li><a @click="$router.push('/payments')" class="flex items-center px-3 py-2 rounded-md hover:bg-light text-gray-700 cursor-pointer transition-colors"><i class="fa fa-credit-card w-5 text-center mr-3 text-gray-500"></i>支付记录</a></li>
            </ul>
          </div>
        </aside>

        <!-- 中间内容区域 -->
        <section class="lg:w-3/5 w-full">
          <!-- 欢迎卡片 -->
          <div class="bg-white rounded-lg card-shadow p-6 mb-6 fade-in text-center">
            <div class="w-16 h-16 rounded-full bg-light flex items-center justify-center mx-auto mb-3">
              <i class="fa fa-paw text-primary text-3xl"></i>
            </div>
            <h2 class="text-lg font-semibold text-gray-800 mb-1">欢迎回来，{{ auth.user?.username || '用户' }}！</h2>
            <p class="text-gray-500 text-sm">
              <span v-if="auth.user?.user_type === 1">发布家教需求，AI 帮您精准匹配</span>
              <span v-else-if="auth.user?.user_type === 2">完善资料，接收家长匹配推荐</span>
            </p>
          </div>

          <!-- 家长视图 -->
          <div v-if="auth.user?.user_type === 1">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-800 flex items-center"><i class="fa fa-tasks text-primary mr-2"></i>我的家教需求</h3>
              <button @click="showForm = !showForm" class="bg-primary hover:bg-secondary text-white text-sm font-medium py-2 px-4 rounded-lg transition-colors shadow-md">
                <i :class="showForm ? 'fa fa-minus' : 'fa fa-plus'" class="mr-1"></i>{{ showForm ? '收起' : '发布需求' }}
              </button>
            </div>

            <div v-if="showForm" class="mb-6 fade-in">
              <DemandForm @created="onCreated" @mode-select="onModeSelect" />
            </div>

            <TutorSearch v-if="showTutorSearch" />

            <div v-if="store.demands.length" class="space-y-3">
              <DemandCard v-for="d in store.demands" :key="d.id" :demand="d"
                :matching="matchingId === d.id"
                @click="$router.push(`/demand/${d.id}`)"
                @match="handleMatch(d.id)"
                @viewMatch="$router.push(`/match/${d.id}`)" />
            </div>
            <div v-else-if="!showForm" class="bg-white rounded-lg card-shadow p-8 text-center text-gray-400">
              <i class="fa fa-inbox text-4xl mb-3"></i>
              <p>还没有发布需求，点击上方按钮发布第一条</p>
            </div>
          </div>

          <!-- 家教视图 -->
          <div v-if="auth.user?.user_type === 2" class="bg-white rounded-lg card-shadow p-8 fade-in">
            <div class="text-center">
              <div class="w-20 h-20 rounded-full bg-light flex items-center justify-center mx-auto mb-4">
                <i class="fa fa-graduation-cap text-primary text-3xl"></i>
              </div>
              <h3 class="text-lg font-semibold text-gray-800 mb-2">家教工作台</h3>
              <p class="text-gray-500 mb-6">完善个人资料以接收家长匹配推荐</p>
              <button @click="$router.push('/profile')" class="bg-primary hover:bg-secondary text-white font-medium py-2 px-6 rounded-lg transition-colors shadow-md">
                <i class="fa fa-edit mr-2"></i>完善资料
              </button>
            </div>
          </div>
        </section>

        <!-- 右侧边栏 -->
        <aside class="lg:w-1/5 w-full">
          <div class="bg-white rounded-lg card-shadow p-4 mb-4 sticky top-24">
            <div class="flex flex-col items-center text-center">
              <div class="w-16 h-16 rounded-full bg-light flex items-center justify-center mb-2">
                <i class="fa fa-user text-primary text-2xl"></i>
              </div>
              <h3 class="font-semibold text-gray-800">{{ auth.user?.username }}</h3>
              <p class="text-xs text-gray-500">{{ roleText }}</p>
            </div>
            <div class="mt-4 grid grid-cols-2 gap-2">
              <a @click="$router.push('/profile')" class="flex flex-col items-center p-2 bg-light rounded-lg hover:bg-primary/10 transition-colors cursor-pointer">
                <i class="fa fa-cog text-primary"></i>
                <span class="text-xs text-gray-700 mt-1">个人设置</span>
              </a>
              <a @click="$router.push('/order/0')" class="flex flex-col items-center p-2 bg-light rounded-lg hover:bg-primary/10 transition-colors cursor-pointer">
                <i class="fa fa-file-text text-primary"></i>
                <span class="text-xs text-gray-700 mt-1">我的订单</span>
              </a>
            </div>
          </div>
        </aside>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useDemandStore } from '../stores/demand'
import DemandForm from '../components/DemandForm.vue'
import DemandCard from '../components/DemandCard.vue'
import TutorSearch from '../components/TutorSearch.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const store = useDemandStore()

const showForm = ref(false)
const matchingId = ref(null)
const showTutorSearch = ref(false)
const lastCreatedDemandId = ref(null)

const roleText = computed(() => ({ 1: '家长', 2: '家教', 3: '管理员' }[auth.user?.user_type] || ''))

onMounted(async () => {
  if (!auth.user) await auth.fetchUser()
  if (auth.user?.user_type === 1) {
    await store.fetchList()
    if (route.query.search === 'open') showTutorSearch.value = true
  }
})

function onCreated({ id, mode }) {
  showForm.value = false
  lastCreatedDemandId.value = id
  if (!mode) store.fetchList()
}

function onModeSelect({ mode }) {
  if (mode === 'ai') {
    showForm.value = false
    const demandId = lastCreatedDemandId.value
    store.runMatch(demandId)
    router.push(`/match/${demandId}`)
  } else if (mode === 'manual') {
    showForm.value = false
    showTutorSearch.value = true
  }
}
async function handleMatch(demandId) { matchingId.value = demandId; await store.runMatch(demandId); matchingId.value = null; router.push(`/match/${demandId}`) }
function handleLogout() { auth.logout(); router.push('/login') }
</script>
