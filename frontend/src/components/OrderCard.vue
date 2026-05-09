<template>
  <div class="order-card" @click="$emit('click')">
    <div class="header">
      <span class="title">订单 #{{ order.id }}</span>
      <span class="status">{{ statusText }}</span>
    </div>
    <div class="info">
      <span v-if="order.demand_title">需求: {{ order.demand_title }}</span>
      <span>家教: {{ order.tutor_name || '--' }}</span>
      <span>金额: {{ order.total_amount }}元</span>
      <span>{{ order.create_time?.slice(0, 10) }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ order: Object })
defineEmits(['click'])
const statusText = computed(() => {
  const m = { 1: '待支付', 2: '进行中', 3: '已完成', 4: '已取消' }
  return m[props.order.status] || '未知'
})
</script>

<style scoped>
.order-card { background:#fff; padding:16px 20px; border-radius:10px; box-shadow:0 1px 4px rgba(0,0,0,0.06); cursor:pointer; margin-bottom:10px; }
.header { display:flex; justify-content:space-between; margin-bottom:6px; }
.title { font-weight:600; color:#1f2937; }
.status { font-size:12px; padding:2px 8px; border-radius:12px; background:#f3f4f6; color:#6b7280; }
.info { display:flex; gap:12px; font-size:13px; color:#6b7280; flex-wrap:wrap; }
</style>
