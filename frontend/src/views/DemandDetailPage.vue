<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white nav-shadow px-6 py-3 flex justify-between items-center">
      <span class="text-xl font-bold text-primary flex items-center"><i class="fa fa-paw mr-2"></i>趣学喵</span>
      <button @click="$router.push('/dashboard')" class="text-sm border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50 transition-colors"><i class="fa fa-arrow-left mr-1"></i>返回</button>
    </nav>
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h2 v-if="demand" class="text-xl font-bold text-gray-800 mb-4">{{ demand.title }}</h2>
      <div v-if="demand" class="bg-white rounded-xl card-shadow p-6">
        <div class="flex justify-between py-3 border-b border-gray-100 text-sm"><span class="text-gray-500">学科</span><span class="text-gray-700">{{ demand.subject }} · {{ demand.grade }}</span></div>
        <div class="flex justify-between py-3 border-b border-gray-100 text-sm"><span class="text-gray-500">区域</span><span class="text-gray-700">{{ demand.location || '--' }}</span></div>
        <div class="flex justify-between py-3 border-b border-gray-100 text-sm"><span class="text-gray-500">预算</span><span class="text-gray-700">{{ demand.budget }}元/时</span></div>
        <div class="flex justify-between py-3 border-b border-gray-100 text-sm"><span class="text-gray-500">状态</span><span :class="demand.status === 1 ? 'text-primary font-medium' : 'text-gray-700'">{{ statusText }}</span></div>
        <div class="flex justify-between py-3 border-b border-gray-100 text-sm"><span class="text-gray-500">描述</span><span class="text-gray-700 text-right max-w-xs">{{ demand.description || '--' }}</span></div>
        <div class="flex justify-between py-3 text-sm"><span class="text-gray-500">要求</span><span class="text-gray-700">{{ demand.requirements || '--' }}</span></div>
      </div>
      <div v-if="demand && demand.status === 1" class="mt-4">
        <button @click="goMatch" class="bg-primary hover:bg-secondary text-white font-medium px-6 py-3 rounded-lg transition-colors shadow-md">
          <i class="fa fa-magic mr-2"></i>AI 智能匹配
        </button>
      </div>
      <div v-if="demand && demand.match_status === 'done' && demand.match_result?.length" class="mt-4">
        <button @click="goMatch" class="bg-green-600 hover:bg-green-700 text-white font-medium px-6 py-3 rounded-lg transition-colors shadow-md">
          <i class="fa fa-list mr-2"></i>查看匹配结果
        </button>
      </div>
      <p v-if="!demand" class="text-center py-20 text-gray-400"><i class="fa fa-inbox text-5xl mb-3 block"></i>需求不存在</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDemandStore } from '../stores/demand'
const route = useRoute(); const router = useRouter(); const store = useDemandStore()
const demand = ref(null)
const statusText = computed(() => ({ 1: '招募中', 2: '已匹配', 3: '已完成', 4: '已取消' }[demand.value?.status] || '--'))
onMounted(async () => { await store.fetchDetail(Number(route.params.id)); demand.value = store.currentDemand })
function goMatch() { router.push(`/match/${demand.value.id}`) }
</script>
