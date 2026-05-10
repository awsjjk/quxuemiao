<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white nav-shadow px-6 py-3 flex justify-between items-center">
      <span class="text-xl font-bold text-primary flex items-center"><i class="fa fa-paw mr-2"></i>趣学喵</span>
      <button @click="$router.push('/dashboard')" class="text-sm border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50 transition-colors"><i class="fa fa-arrow-left mr-1"></i>返回</button>
    </nav>
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h2 class="text-xl font-bold text-gray-800 mb-6 flex items-center"><i class="fa fa-magic text-primary mr-2"></i>AI 匹配结果</h2>
      <MatchLoading v-if="status === 'pending' || status === 'processing'" />
      <div v-else-if="status === 'done' && results.length">
        <TutorCard v-for="(t, i) in results" :key="t.tutor_id" :tutor="t" :rank="i+1" :selected="selectedTutor === t.tutor_id" @select="handleSelect" />
        <button v-if="selectedTutor" @click="createOrder" class="w-full bg-primary hover:bg-secondary text-white font-medium py-3 rounded-lg mt-3 transition-colors shadow-md">
          <i class="fa fa-check-circle mr-2"></i>创建订单
        </button>
      </div>
      <div v-else-if="status === 'done' && !results.length" class="text-center py-12">
        <i class="fa fa-inbox text-4xl text-gray-300 mb-4 block"></i>
        <p class="text-gray-500 mb-6">暂无匹配到符合条件的结果</p>
        <button @click="$router.push('/dashboard?search=open')" class="bg-primary hover:bg-secondary text-white text-sm px-6 py-2.5 rounded-lg transition-colors shadow-md">
          <i class="fa fa-search mr-2"></i>前往手动筛选
        </button>
      </div>
      <div v-else-if="status === 'failed'" class="text-center py-12">
        <i class="fa fa-exclamation-triangle text-4xl text-amber-400 mb-4 block"></i>
        <p class="text-gray-500 mb-6">AI 匹配失败，您可以尝试手动筛选</p>
        <button @click="$router.push('/dashboard?search=open')" class="bg-primary hover:bg-secondary text-white text-sm px-6 py-2.5 rounded-lg transition-colors shadow-md">
          <i class="fa fa-search mr-2"></i>前往手动筛选
        </button>
      </div>
      <div v-else-if="status === 'timeout'" class="text-center py-12">
        <i class="fa fa-clock-o text-4xl text-gray-300 mb-4 block"></i>
        <p class="text-gray-500 mb-2">匹配耗时较长</p>
        <p class="text-gray-400 text-xs mb-6">您可以稍后在需求详情中查看结果，或直接手动筛选</p>
        <div class="flex gap-3 justify-center">
          <button @click="$router.push('/dashboard')" class="border border-gray-300 text-gray-600 text-sm px-6 py-2 rounded-lg hover:bg-gray-50 transition-colors">返回首页</button>
          <button @click="$router.push('/dashboard?search=open')" class="bg-primary hover:bg-secondary text-white text-sm px-6 py-2.5 rounded-lg transition-colors shadow-md">
            <i class="fa fa-search mr-2"></i>手动筛选
          </button>
        </div>
      </div>
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
const route = useRoute(); const router = useRouter(); const store = useDemandStore()
const demandId = Number(route.params.demand_id)
const status = ref('pending'); const results = ref([]); const selectedTutor = ref(null)
let timer = null
let count = 0
const MAX_POLLS = 15

onMounted(() => {
  poll()
  timer = setInterval(() => {
    count++
    if (count >= MAX_POLLS) {
      clearInterval(timer)
      if (status.value === 'pending' || status.value === 'processing') {
        status.value = 'timeout'
      }
      return
    }
    poll()
  }, 3000)
})
onUnmounted(() => clearInterval(timer))

async function poll() {
  const data = await store.pollResult(demandId)
  status.value = data.status
  if (data.status === 'done') {
    results.value = data.result || []
    clearInterval(timer)
  } else if (data.status === 'failed') {
    clearInterval(timer)
  }
}
function handleSelect(tutorId) { selectedTutor.value = tutorId }
async function createOrder() {
  try { const res = await orderAPI.create({ demand_id: demandId, tutor_id: selectedTutor.value }); router.push(`/order/${res.data.id}`) }
  catch (e) { alert(e.response?.data?.msg || '创建订单失败') }
}
</script>
