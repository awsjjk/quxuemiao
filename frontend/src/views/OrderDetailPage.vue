<template>
  <div class="page">
    <nav><span class="logo">趣学喵</span><button @click="$router.back()">返回</button></nav>
    <div class="container">
      <div v-if="route.params.id === '0'">
        <h2>我的订单</h2>
        <p v-if="!orders.length" class="empty">暂无订单</p>
        <OrderCard v-for="o in orders" :key="o.id" :order="o" @click="$router.push(`/order/${o.id}`)" />
      </div>
      <div v-else-if="order">
        <h2>订单详情</h2>
        <div class="detail">
          <div class="row"><span class="label">订单状态</span><span>{{ statusText }}</span></div>
          <div class="row"><span class="label">需求标题</span><span>{{ order.demand_title }}</span></div>
          <div class="row"><span class="label">家教</span><span>{{ order.tutor_name }} &middot; {{ order.tutor_school }}</span></div>
          <div class="row"><span class="label">联系电话</span><span>{{ order.tutor_phone || '--' }}</span></div>
          <div class="row"><span class="label">金额</span><span>{{ order.total_amount }}元</span></div>
          <div class="row"><span class="label">创建时间</span><span>{{ order.create_time?.slice(0, 10) }}</span></div>
        </div>
        <div class="actions" v-if="order.status === 2">
          <button @click="finishOrder" :disabled="loading">确认完成</button>
        </div>
        <RatingForm v-if="order.status === 3 && !rated" :order-id="order.id" @submitted="rated = true" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { orderAPI } from '../api'
import OrderCard from '../components/OrderCard.vue'
import RatingForm from '../components/RatingForm.vue'

const route = useRoute()
const router = useRouter()
const orders = ref([])
const order = ref(null)
const loading = ref(false)
const rated = ref(false)

const statusText = computed(() => {
  const m = { 1: '待支付', 2: '进行中', 3: '已完成', 4: '已取消' }
  return m[order.value?.status] || '--'
})

onMounted(async () => {
  const id = route.params.id
  if (id === '0') {
    const res = await orderAPI.list()
    orders.value = res.data
  } else {
    const res = await orderAPI.detail(Number(id))
    order.value = res.data
  }
})

async function finishOrder() {
  loading.value = true
  try {
    await orderAPI.updateStatus(order.value.id, 3)
    order.value.status = 3
  } catch (e) {
    alert(e.response?.data?.msg || '操作失败')
  } finally {
    loading.value = false
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
.empty { color:#9ca3af; text-align:center; padding:48px 0; }
.detail { background:#fff; padding:20px; border-radius:10px; margin-bottom:16px; }
.row { display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #f3f4f6; font-size:14px; }
.row:last-child { border:none; }
.label { color:#6b7280; }
.actions { margin:16px 0; }
.actions button { padding:10px 24px; background:#059669; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
.actions button:disabled { opacity:0.6; }
</style>
