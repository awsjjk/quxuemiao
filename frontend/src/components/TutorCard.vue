<template>
  <div class="tutor-card">
    <div class="top">
      <span class="rank">#{{ rank }}</span>
      <span class="name">{{ tutor.real_name || '未填写姓名' }}</span>
      <span class="score">{{ tutor.total_score }}分</span>
    </div>
    <div class="meta">
      <span>{{ tutor.school }}</span>
      <span>{{ tutor.major }}</span>
      <span>{{ tutor.education }}</span>
      <span>{{ tutor.teaching_exp }}年经验</span>
    </div>
    <div class="scores">
      <span>学科匹配 {{ tutor.subject_match }}/40</span>
      <span>经验匹配 {{ tutor.experience_match }}/30</span>
      <span>区位匹配 {{ tutor.location_time_match }}/15</span>
      <span>性价比 {{ tutor.value_match }}/15</span>
    </div>
    <p class="reason">&bull; {{ tutor.reason }}</p>
    <button v-if="!selected" @click="$emit('select', tutor.tutor_id)">选择此家教</button>
  </div>
</template>

<script setup>
defineProps({ tutor: Object, rank: Number, selected: Boolean })
defineEmits(['select'])
</script>

<style scoped>
.tutor-card { background:#fff; padding:20px; border-radius:10px; box-shadow:0 1px 6px rgba(0,0,0,0.06); margin-bottom:12px; }
.top { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.rank { background:#2563eb; color:#fff; width:28px; height:28px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0; }
.name { font-weight:600; font-size:16px; color:#1f2937; }
.score { margin-left:auto; font-weight:700; color:#2563eb; font-size:18px; }
.meta { display:flex; gap:12px; font-size:13px; color:#6b7280; margin-bottom:8px; flex-wrap:wrap; }
.scores { display:flex; gap:10px; font-size:12px; color:#9ca3af; margin-bottom:8px; flex-wrap:wrap; }
.reason { font-size:13px; color:#374151; margin-bottom:12px; }
button { padding:8px 20px; background:#059669; color:#fff; border:none; border-radius:6px; font-size:13px; cursor:pointer; }
</style>
