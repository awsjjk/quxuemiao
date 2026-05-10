<template>
  <div class="space-y-3 mt-4 border-t border-gray-100 pt-4">
    <p class="text-sm text-gray-500">选择匹配方式：</p>
    <div
      @click="$emit('select', 'ai')"
      :class="['border-2 rounded-xl p-4 cursor-pointer transition-all', selected === 'ai' ? 'border-primary bg-primary/5' : 'border-gray-200 hover:border-primary/50']">
      <div class="flex items-center gap-3">
        <span class="text-2xl">🤖</span>
        <div>
          <span class="font-semibold text-sm text-gray-800">AI 智能匹配</span>
          <p class="text-xs text-gray-500 mt-0.5">系统根据需求自动分析，从家教库中匹配最合适的候选人，30秒内返回结果</p>
        </div>
      </div>
    </div>
    <div
      @click="$emit('select', 'manual')"
      :class="['border-2 rounded-xl p-4 cursor-pointer transition-all', selected === 'manual' ? 'border-primary bg-primary/5' : 'border-gray-200 hover:border-primary/50']">
      <div class="flex items-center gap-3">
        <span class="text-2xl">🔍</span>
        <div>
          <span class="font-semibold text-sm text-gray-800">手动筛选搜索</span>
          <p class="text-xs text-gray-500 mt-0.5">按条件精确筛选家教，查看详细资料后自行选择</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ selected: { type: String, default: '' } })
defineEmits(['select'])
</script>
