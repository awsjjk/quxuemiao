<template>
  <div class="card" @click="$emit('click')">
    <div class="header">
      <span class="title">{{ demand.title }}</span>
      <span class="tag" :class="statusClass">{{ statusText }}</span>
    </div>
    <div class="info">
      <span>{{ demand.subject }} · {{ demand.grade }}</span>
      <span v-if="demand.location">{{ demand.location }}</span>
      <span v-if="demand.budget">{{ demand.budget }}元/时</span>
    </div>
    <div class="actions" v-if="demand.status === 1" @click.stop>
      <button @click="$emit('match')" :disabled="matching">AI 智能匹配</button>
    </div>
    <div class="actions" v-if="demand.match_status === 'done' && demand.match_result" @click.stop>
      <button class="secondary" @click="$emit('viewMatch')">查看匹配结果</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ demand: Object, matching: Boolean })
defineEmits(['click', 'match', 'viewMatch'])

const statuses = { 1: '招募中', 2: '已匹配', 3: '已完成', 4: '已取消' }
const statusText = computed(() => statuses[props.demand.status] || '未知')
const statusClass = computed(() => props.demand.status === 1 ? 'active' : '')
</script>

<style scoped>
.card { background:#fff; padding:16px 20px; border-radius:10px; box-shadow:0 1px 4px rgba(0,0,0,0.06); cursor:pointer; margin-bottom:10px; transition:box-shadow 0.15s; }
.card:hover { box-shadow:0 2px 10px rgba(0,0,0,0.1); }
.header { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
.title { font-weight:600; color:#1f2937; }
.tag { font-size:12px; padding:2px 8px; border-radius:12px; background:#f3f4f6; color:#6b7280; }
.tag.active { background:#dbeafe; color:#2563eb; }
.info { display:flex; gap:12px; font-size:13px; color:#6b7280; flex-wrap:wrap; }
.actions { margin-top:12px; display:flex; gap:8px; }
button { padding:6px 16px; background:#2563eb; color:#fff; border:none; border-radius:6px; font-size:13px; cursor:pointer; }
button:disabled { opacity:0.6; }
button.secondary { background:#059669; }
</style>
