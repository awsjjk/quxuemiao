<template>
  <div class="dashboard">
    <nav>
      <span class="logo">趣学喵</span>
      <div class="nav-right">
        <span class="user">{{ auth.user?.username }} ({{ roleText }})</span>
        <button @click="goProfile">个人信息</button>
        <button @click="$router.push('/order/0')">我的订单</button>
        <button class="logout" @click="handleLogout">退出</button>
      </div>
    </nav>

    <div class="container" v-if="auth.user?.user_type === 1">
      <h2>我的家教需求</h2>
      <button class="btn-create" @click="showForm = !showForm">
        {{ showForm ? '收起' : '+ 发布新需求' }}
      </button>
      <DemandForm v-if="showForm" @created="onCreated" />
      <div class="list" v-if="store.demands.length">
        <DemandCard v-for="d in store.demands" :key="d.id" :demand="d"
          :matching="matchingId === d.id"
          @click="$router.push(`/demand/${d.id}`)"
          @match="handleMatch(d.id)"
          @viewMatch="$router.push(`/match/${d.id}`)" />
      </div>
      <p v-else class="empty">还没有发布需求，点击上方按钮发布第一条</p>
    </div>

    <div class="container" v-else-if="auth.user?.user_type === 2">
      <h2>家教工作台</h2>
      <p class="empty">完善个人资料以接收匹配推荐</p>
      <button @click="goProfile">完善资料</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useDemandStore } from '../stores/demand'
import DemandForm from '../components/DemandForm.vue'
import DemandCard from '../components/DemandCard.vue'

const router = useRouter()
const auth = useAuthStore()
const store = useDemandStore()

const showForm = ref(false)
const matchingId = ref(null)

const roleText = computed(() => {
  const roles = { 1: '家长', 2: '家教', 3: '管理员' }
  return roles[auth.user?.user_type] || ''
})

onMounted(async () => {
  if (!auth.user) await auth.fetchUser()
  if (auth.user?.user_type === 1) await store.fetchList()
})

function onCreated() {
  showForm.value = false
  store.fetchList()
}

async function handleMatch(demandId) {
  matchingId.value = demandId
  await store.runMatch(demandId)
  matchingId.value = null
  router.push(`/match/${demandId}`)
}

function handleLogout() { auth.logout(); router.push('/login') }
function goProfile() { router.push('/profile') }
</script>

<style scoped>
.dashboard { min-height:100vh; background:#f5f5f5; }
nav { display:flex; justify-content:space-between; align-items:center; padding:12px 24px; background:#fff; box-shadow:0 1px 4px rgba(0,0,0,0.06); }
.logo { font-size:20px; font-weight:700; color:#2563eb; }
.nav-right { display:flex; align-items:center; gap:12px; }
.nav-right .user { font-size:14px; color:#374151; }
nav button { padding:6px 14px; border:1px solid #d1d5db; border-radius:6px; background:#fff; font-size:13px; cursor:pointer; }
nav button.logout { background:#fee2e2; color:#dc2626; border-color:#fecaca; }
.container { max-width:700px; margin:24px auto; padding:0 16px; }
h2 { color:#1f2937; }
.btn-create { margin:12px 0; padding:8px 20px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
.empty { color:#9ca3af; font-size:14px; margin-top:48px; text-align:center; }
.list { margin-top:16px; }
</style>
