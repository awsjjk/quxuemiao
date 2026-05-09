<template>
  <div class="page">
    <nav><span class="logo">趣学喵</span><button @click="$router.push('/dashboard')">返回</button></nav>
    <div class="container">
      <h2>AI 匹配结果</h2>
      <MatchLoading v-if="status === 'pending' || status === 'processing'" />
      <div v-else-if="status === 'done' && results.length">
        <TutorCard v-for="(t, i) in results" :key="t.tutor_id" :tutor="t" :rank="i+1"
          :selected="selectedTutor === t.tutor_id" @select="handleSelect" />
        <button v-if="selectedTutor" class="create-btn" @click="createOrder">创建订单</button>
      </div>
      <p v-else-if="status === 'done' && !results.length" class="empty">暂无匹配结果</p>
      <p v-else-if="status === 'failed'" class="empty">匹配失败，请重试</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDemandStore } from '../stores/demand'
import { orderAPI } from '../api'
import MatchLoading from '../components/MatchLoading.vue'
import TutorCard from '../components/TutorCard.vue'

const route = useRoute()
const router = useRouter()
const store = useDemandStore()

const demandId = Number(route.params.demand_id)
const status = ref('pending')
const results = ref([])
const selectedTutor = ref(null)
let timer = null

onMounted(() => {
  poll()
  timer = setInterval(poll, 2000)
})

onUnmounted(() => clearInterval(timer))

async function poll() {
  const data = await store.pollResult(demandId)
  status.value = data.status
  if (data.status === 'done') {
    results.value = data.result || []
    clearInterval(timer)
  }
}

function handleSelect(tutorId) { selectedTutor.value = tutorId }

async function createOrder() {
  try {
    const res = await orderAPI.create({ demand_id: demandId, tutor_id: selectedTutor.value })
    router.push(`/order/${res.data.id}`)
  } catch (e) {
    alert(e.response?.data?.msg || '创建订单失败')
  }
}
</script>

<style scoped>
.page { min-height:100vh; background:#f5f5f5; }
nav { display:flex; justify-content:space-between; align-items:center; padding:12px 24px; background:#fff; }
.logo { font-size:20px; font-weight:700; color:#2563eb; }
nav button { padding:6px 14px; border:1px solid #d1d5db; border-radius:6px; background:#fff; font-size:13px; cursor:pointer; }
.container { max-width:600px; margin:24px auto; padding:0 16px; }
h2 { color:#1f2937; margin-bottom:16px; }
.create-btn { width:100%; padding:12px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:15px; cursor:pointer; margin-top:12px; }
.empty { text-align:center; color:#9ca3af; padding:48px 0; }
</style>
