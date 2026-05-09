<template>
  <div class="page">
    <nav><span class="logo">趣学喵</span><button @click="$router.push('/dashboard')">返回</button></nav>
    <div class="container">
      <h2 v-if="demand">{{ demand.title }}</h2>
      <div v-if="demand" class="detail">
        <div class="row"><span class="label">学科</span><span>{{ demand.subject }} · {{ demand.grade }}</span></div>
        <div class="row"><span class="label">区域</span><span>{{ demand.location || '--' }}</span></div>
        <div class="row"><span class="label">预算</span><span>{{ demand.budget }}元/时</span></div>
        <div class="row"><span class="label">状态</span><span>{{ statusText }}</span></div>
        <div class="row"><span class="label">描述</span><span>{{ demand.description || '--' }}</span></div>
        <div class="row"><span class="label">要求</span><span>{{ demand.requirements || '--' }}</span></div>
      </div>
      <div v-if="demand && demand.status === 1" class="actions">
        <button @click="goMatch">AI 智能匹配</button>
      </div>
      <div v-if="demand && demand.match_status === 'done' && demand.match_result?.length" class="actions">
        <button class="secondary" @click="goMatch">查看匹配结果</button>
      </div>
      <p v-if="!demand" class="empty">需求不存在</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDemandStore } from '../stores/demand'

const route = useRoute()
const router = useRouter()
const store = useDemandStore()
const demand = ref(null)

const statusText = computed(() => {
  const m = { 1: '招募中', 2: '已匹配', 3: '已完成', 4: '已取消' }
  return m[demand.value?.status] || '--'
})

onMounted(async () => {
  await store.fetchDetail(Number(route.params.id))
  demand.value = store.currentDemand
})

function goMatch() { router.push(`/match/${demand.value.id}`) }
</script>

<style scoped>
.page { min-height:100vh; background:#f5f5f5; }
nav { display:flex; justify-content:space-between; align-items:center; padding:12px 24px; background:#fff; }
.logo { font-size:20px; font-weight:700; color:#2563eb; }
nav button { padding:6px 14px; border:1px solid #d1d5db; border-radius:6px; background:#fff; font-size:13px; cursor:pointer; }
.container { max-width:600px; margin:24px auto; padding:0 16px; }
.detail { background:#fff; padding:20px; border-radius:10px; }
.row { display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #f3f4f6; font-size:14px; }
.row:last-child { border:none; }
.label { color:#6b7280; }
.actions { margin:16px 0; }
.actions button { padding:10px 24px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; margin-right:8px; }
.actions button.secondary { background:#059669; }
.empty { text-align:center; color:#9ca3af; padding:48px 0; }
h2 { margin-bottom:16px; }
</style>
