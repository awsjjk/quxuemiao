<template>
  <div class="bg-white rounded-lg p-4 border border-gray-100 hover:shadow-md transition-shadow cursor-pointer mb-3" @click="$emit('click')">
    <div class="flex justify-between mb-2">
      <span class="font-semibold text-gray-800">订单 #{{ order.id }}</span>
      <span class="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-500">{{ statusText }}</span>
    </div>
    <div class="flex gap-4 text-sm text-gray-500 flex-wrap">
      <span v-if="order.demand_title"><i class="fa fa-file-text-o mr-1"></i>{{ order.demand_title }}</span>
      <span><i class="fa fa-user mr-1"></i>{{ order.tutor_name || '--' }}</span>
      <span><i class="fa fa-cny mr-1"></i>{{ order.total_amount }}元</span>
      <span>{{ order.create_time?.slice(0, 10) }}</span>
    </div>
  </div>
</template>
<script setup>
import { computed } from 'vue'
const props = defineProps({ order: Object })
defineEmits(['click'])
const statusText = computed(() => ({ 1: '待支付', 2: '进行中', 3: '已完成', 4: '已取消' }[props.order.status] || '未知'))
</script>
