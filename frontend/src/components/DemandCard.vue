<template>
  <div class="bg-white rounded-lg p-4 border border-gray-100 hover:shadow-md transition-shadow cursor-pointer" @click="$emit('click')">
    <div class="flex justify-between items-start mb-2">
      <span class="font-semibold text-gray-800">{{ demand.title }}</span>
      <span class="text-xs px-2 py-0.5 rounded-full" :class="demand.status === 1 ? 'bg-light text-primary' : 'bg-gray-100 text-gray-500'">{{ statusText }}</span>
    </div>
    <div class="flex gap-4 text-xs text-gray-500 flex-wrap">
      <span><i class="fa fa-book mr-1"></i>{{ demand.subject }} · {{ demand.grade }}</span>
      <span v-if="demand.location"><i class="fa fa-map-marker mr-1"></i>{{ demand.location }}</span>
      <span v-if="demand.budget"><i class="fa fa-cny mr-1"></i>{{ demand.budget }}元/时</span>
    </div>
    <div class="flex gap-2 mt-3" @click.stop>
      <button v-if="demand.status === 1" @click="$emit('match')" :disabled="matching" class="text-xs bg-primary hover:bg-secondary text-white px-3 py-1.5 rounded transition-colors disabled:opacity-50">
        <i class="fa fa-magic mr-1"></i>AI 匹配
      </button>
      <button v-if="demand.match_status === 'done' && demand.match_result" @click="$emit('viewMatch')" class="text-xs bg-green-600 hover:bg-green-700 text-white px-3 py-1.5 rounded transition-colors">
        <i class="fa fa-list mr-1"></i>查看匹配结果
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ demand: Object, matching: Boolean })
defineEmits(['click', 'match', 'viewMatch'])
const statuses = { 1: '招募中', 2: '已匹配', 3: '已完成', 4: '已取消' }
const statusText = computed(() => statuses[props.demand.status] || '未知')
</script>
