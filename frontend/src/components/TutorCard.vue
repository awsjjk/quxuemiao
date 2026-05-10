<template>
  <div class="bg-white rounded-xl card-shadow p-4 border border-gray-100">
    <div class="flex items-center gap-3 mb-3">
      <div class="w-11 h-11 rounded-full bg-blue-50 flex items-center justify-center text-xl flex-shrink-0">
        <i class="fa fa-user-graduate text-primary"></i>
      </div>
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2">
          <span class="font-semibold text-sm text-gray-800">{{ tutor.real_name || tutor.username }}</span>
          <span v-if="tutor.verification_status === 2" class="text-xs bg-green-50 text-green-600 px-1.5 py-0.5 rounded">已认证</span>
        </div>
        <div class="text-xs text-gray-500">{{ tutor.school }}{{ tutor.major ? ' · ' + tutor.major : '' }}{{ tutor.teaching_exp ? ' · ' + tutor.teaching_exp + '年教龄' : '' }}</div>
      </div>
      <div class="text-right flex-shrink-0">
        <span class="text-base font-bold text-red-500">¥{{ tutor.hourly_rate }}</span>
        <span class="text-xs text-gray-400">/h</span>
      </div>
    </div>
    <p class="text-xs text-gray-600 mb-3 leading-relaxed line-clamp-2">{{ tutor.introduction || '暂无简介' }}</p>
    <div class="flex flex-wrap gap-1.5 mb-3">
      <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">{{ tutor.school }}</span>
      <span v-if="tutor.location" class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">{{ tutor.location }}</span>
      <span v-if="tutor.available_time && tutor.available_time.length" class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">{{ tutor.available_time.slice(0, 2).join(' ') }}</span>
    </div>
    <div class="flex gap-2">
      <button @click="$emit('chat', tutor)" class="flex-1 bg-primary hover:bg-secondary text-white text-xs py-2 rounded-lg transition-colors">
        <i class="fa fa-comment mr-1"></i>发起沟通
      </button>
      <button @click="$emit('detail', tutor)" class="px-3 border border-gray-300 rounded-lg text-xs text-gray-600 hover:bg-gray-50 transition-colors">
        详情
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({ tutor: { type: Object, required: true } })
defineEmits(['chat', 'detail'])
</script>
