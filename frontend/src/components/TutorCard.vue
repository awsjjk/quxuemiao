<template>
  <div class="bg-white rounded-lg card-shadow p-5 mb-3 fade-in">
    <div class="flex items-center gap-3 mb-3">
      <span class="bg-primary text-white w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">#{{ rank }}</span>
      <span class="font-semibold text-gray-800">{{ tutor.real_name || '未填写姓名' }}</span>
      <span class="ml-auto font-bold text-primary text-lg">{{ tutor.total_score }}分</span>
    </div>
    <div class="flex gap-3 text-sm text-gray-500 mb-2 flex-wrap">
      <span>{{ tutor.school }}</span><span>{{ tutor.major }}</span><span>{{ tutor.education }}</span><span>{{ tutor.teaching_exp }}年经验</span>
    </div>
    <div class="flex gap-3 text-xs text-gray-400 mb-3 flex-wrap">
      <span>学科 {{ tutor.subject_match }}/40</span><span>经验 {{ tutor.experience_match }}/30</span><span>区位 {{ tutor.location_time_match }}/15</span><span>性价比 {{ tutor.value_match }}/15</span>
    </div>
    <p class="text-sm text-gray-600 mb-3">{{ tutor.reason }}</p>
    <button v-if="!selected" @click="$emit('select', tutor.tutor_id)" class="bg-green-600 hover:bg-green-700 text-white text-sm px-4 py-2 rounded-lg transition-colors">
      <i class="fa fa-check mr-1"></i>选择此家教
    </button>
    <span v-else class="text-green-600 text-sm font-medium"><i class="fa fa-check-circle mr-1"></i>已选择</span>
  </div>
</template>
<script setup>
defineProps({ tutor: Object, rank: Number, selected: Boolean })
defineEmits(['select'])
</script>
