<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white nav-shadow px-6 py-3 flex justify-between items-center">
      <span class="text-xl font-bold text-primary flex items-center"><i class="fa fa-paw mr-2"></i>趣学喵</span>
      <button @click="$router.back()" class="text-sm border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50 transition-colors"><i class="fa fa-arrow-left mr-1"></i>返回</button>
    </nav>
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h2 class="text-xl font-bold text-gray-800 mb-2">选择需求创建订单</h2>
      <p class="text-sm text-gray-500 mb-6">家教：{{ tutorName }}</p>

      <div v-if="demands.length" class="space-y-3">
        <div v-for="d in demands" :key="d.id" @click="createOrder(d)"
          class="bg-white rounded-xl card-shadow p-4 border border-gray-100 hover:border-primary/50 cursor-pointer transition-all">
          <div class="flex justify-between items-center">
            <div>
              <h3 class="font-semibold text-sm text-gray-800">{{ d.title }}</h3>
              <p class="text-xs text-gray-500 mt-1">{{ d.subject }} · {{ d.grade }} · {{ d.location || '--' }} · ¥{{ d.budget }}/h</p>
            </div>
            <div class="text-primary text-xs font-medium flex items-center gap-1">
              选择 <i class="fa fa-chevron-right"></i>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-12 text-gray-400">
        <i class="fa fa-inbox text-4xl mb-3 block"></i>
        <p>没有可用的招募中需求</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDemandStore } from '../stores/demand'
import { orderAPI } from '../api'

const route = useRoute(); const router = useRouter(); const store = useDemandStore()
const tutorId = ref(Number(route.query.tutor_id))
const tutorName = ref(route.query.tutor_name || '')
const demands = ref([])

onMounted(async () => {
  await store.fetchList()
  demands.value = store.demands.filter(d => d.status === 1)
})

async function createOrder(demand) {
  try {
    const res = await orderAPI.create({
      demand_id: demand.id,
      tutor_id: tutorId.value,
      total_amount: demand.budget * (demand.duration || 2),
    })
    router.push(`/order/${res.data.id}`)
  } catch (e) {
    alert(e.response?.data?.msg || '创建订单失败')
  }
}
</script>
