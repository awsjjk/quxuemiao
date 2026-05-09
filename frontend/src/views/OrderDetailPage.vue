<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white nav-shadow px-6 py-3 flex justify-between items-center">
      <span class="text-xl font-bold text-primary flex items-center"><i class="fa fa-paw mr-2"></i>趣学喵</span>
      <button @click="$router.push('/dashboard')" class="text-sm border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50 transition-colors"><i class="fa fa-arrow-left mr-1"></i>返回</button>
    </nav>
    <div class="max-w-2xl mx-auto py-8 px-4">
      <div v-if="route.params.id === '0'">
        <h2 class="text-xl font-bold text-gray-800 mb-4"><i class="fa fa-list-alt text-primary mr-2"></i>我的订单</h2>
        <p v-if="!orders.length" class="text-center py-20 text-gray-400"><i class="fa fa-inbox text-5xl mb-3 block"></i>暂无订单</p>
        <OrderCard v-for="o in orders" :key="o.id" :order="o" @click="$router.push(`/order/${o.id}`)" />
      </div>
      <div v-else-if="order">
        <h2 class="text-xl font-bold text-gray-800 mb-4"><i class="fa fa-file-text text-primary mr-2"></i>订单详情</h2>
        <div class="bg-white rounded-xl card-shadow p-6 mb-4">
          <div class="flex justify-between py-3 border-b border-gray-100 text-sm"><span class="text-gray-500">订单状态</span><span :class="order.status === 2 ? 'text-green-600 font-medium' : 'text-gray-700'">{{ statusText }}</span></div>
          <div class="flex justify-between py-3 border-b border-gray-100 text-sm"><span class="text-gray-500">需求标题</span><span class="text-gray-700">{{ order.demand_title }}</span></div>
          <div class="flex justify-between py-3 border-b border-gray-100 text-sm"><span class="text-gray-500">家教</span><span class="text-gray-700">{{ order.tutor_name }} &middot; {{ order.tutor_school }}</span></div>
          <div class="flex justify-between py-3 border-b border-gray-100 text-sm"><span class="text-gray-500">联系电话</span><span class="text-gray-700">{{ order.tutor_phone || '--' }}</span></div>
          <div class="flex justify-between py-3 border-b border-gray-100 text-sm"><span class="text-gray-500">金额</span><span class="text-gray-700">{{ order.total_amount }}元</span></div>
          <div class="flex justify-between py-3 text-sm"><span class="text-gray-500">创建时间</span><span class="text-gray-700">{{ order.create_time?.slice(0, 10) }}</span></div>
        </div>
        <div v-if="order.status === 2" class="mb-4">
          <button @click="finishOrder" :disabled="loading" class="bg-green-600 hover:bg-green-700 text-white font-medium px-6 py-3 rounded-lg transition-colors disabled:opacity-60">
            <i class="fa fa-check-circle mr-2"></i>{{ loading ? '处理中...' : '确认完成' }}
          </button>
        </div>
        <RatingForm v-if="order.status === 3 && !rated" :order-id="order.id" @submitted="rated = true" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { orderAPI } from '../api'
import OrderCard from '../components/OrderCard.vue'
import RatingForm from '../components/RatingForm.vue'
const route = useRoute()
const orders = ref([]); const order = ref(null); const loading = ref(false); const rated = ref(false)
const statusText = computed(() => ({ 1: '待支付', 2: '进行中', 3: '已完成', 4: '已取消' }[order.value?.status] || '--'))
onMounted(async () => {
  const id = route.params.id
  if (id === '0') { const res = await orderAPI.list(); orders.value = res.data }
  else { const res = await orderAPI.detail(Number(id)); order.value = res.data }
})
async function finishOrder() { loading.value = true; try { await orderAPI.updateStatus(order.value.id, 3); order.value.status = 3 } catch (e) { alert(e.response?.data?.msg || '操作失败') } finally { loading.value = false } }
</script>
