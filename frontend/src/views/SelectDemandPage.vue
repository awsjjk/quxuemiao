<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white nav-shadow px-6 py-3 flex justify-between items-center">
      <span class="text-xl font-bold text-primary flex items-center"><i class="fa fa-paw mr-2"></i>趣学喵</span>
      <button @click="$router.back()" class="text-sm border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50 transition-colors"><i class="fa fa-arrow-left mr-1"></i>返回</button>
    </nav>
    <div class="max-w-2xl mx-auto py-8 px-4">

      <!-- Step 1: 选择需求 -->
      <div v-if="!selectedDemand">
        <h2 class="text-xl font-bold text-gray-800 mb-2">选择需求</h2>
        <p class="text-sm text-gray-500 mb-6">家教：{{ tutorName }}</p>
        <div v-if="demands.length" class="space-y-3">
          <div v-for="d in demands" :key="d.id" @click="selectedDemand = d"
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

      <!-- Step 2: 确认订单 -->
      <div v-else>
        <button @click="selectedDemand = null" class="text-gray-500 hover:text-gray-700 text-sm mb-4"><i class="fa fa-arrow-left mr-1"></i>返回选择</button>
        <h2 class="text-xl font-bold text-gray-800 mb-4">确认订单</h2>

        <div class="bg-white rounded-xl card-shadow p-4 mb-4">
          <div class="flex justify-between py-2 text-sm"><span class="text-gray-500">家教</span><span class="text-gray-700">{{ tutorName }}</span></div>
          <div class="flex justify-between py-2 text-sm"><span class="text-gray-500">需求</span><span class="text-gray-700">{{ selectedDemand.title }}</span></div>
          <div class="flex justify-between py-2 text-sm"><span class="text-gray-500">学科</span><span class="text-gray-700">{{ selectedDemand.subject }} · {{ selectedDemand.grade }}</span></div>
          <div class="flex justify-between py-2 text-sm border-t border-gray-100 mt-2 pt-2">
            <span class="text-gray-500">课时费（元/小时）</span>
            <span class="text-gray-700">¥{{ selectedDemand.budget }}</span>
          </div>
          <div class="flex justify-between py-2 text-sm">
            <span class="text-gray-500">时长（小时）</span>
            <input v-model.number="hours" type="number" min="0.5" step="0.5" class="w-20 text-right px-2 py-1 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none" />
          </div>
          <div class="flex justify-between py-2 text-sm font-semibold border-t border-gray-100 mt-2 pt-2">
            <span class="text-gray-700">合计金额</span>
            <span class="text-red-500 text-base">¥{{ totalAmount }}</span>
          </div>
          <input v-model="remark" placeholder="备注（可选）" class="w-full mt-3 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none" />
        </div>

        <button @click="confirmOrder" :disabled="saving" class="w-full bg-primary hover:bg-secondary text-white font-medium py-3 rounded-lg transition-colors shadow-md disabled:opacity-60">
          <i class="fa fa-check-circle mr-2"></i>{{ saving ? '创建中...' : `确认创建订单 (¥${totalAmount})` }}
        </button>
        <p class="text-xs text-gray-400 text-center mt-2">订单创建后可在订单详情页点击「确认完成」标记需求为已完成</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDemandStore } from '../stores/demand'
import { orderAPI } from '../api'

const route = useRoute(); const router = useRouter(); const store = useDemandStore()
const tutorId = ref(Number(route.query.tutor_id))
const tutorName = ref(route.query.tutor_name || '')
const demands = ref([])
const selectedDemand = ref(null)
const hours = ref(2)
const remark = ref('')
const saving = ref(false)

const totalAmount = computed(() => {
  if (!selectedDemand.value) return 0
  return (selectedDemand.value.budget || 0) * (hours.value || 1)
})

onMounted(async () => {
  await store.fetchList()
  demands.value = store.demands.filter(d => d.status === 1)
})

async function confirmOrder() {
  saving.value = true
  try {
    const res = await orderAPI.create({
      demand_id: selectedDemand.value.id,
      tutor_id: tutorId.value,
      total_amount: totalAmount.value,
      remark: remark.value,
    })
    router.push(`/order/${res.data.id}`)
  } catch (e) {
    alert(e.response?.data?.msg || '创建订单失败')
  } finally {
    saving.value = false
  }
}
</script>
