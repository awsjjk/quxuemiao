<template>
  <div class="mt-4 border-t border-gray-100 pt-4">
    <div class="flex gap-4">
      <div class="w-56 flex-shrink-0 bg-white rounded-xl card-shadow p-4 border border-gray-100 self-start sticky top-24">
        <h4 class="font-semibold text-sm text-gray-800 mb-3">筛选条件</h4>

        <div class="mb-3">
          <label class="text-xs text-gray-500 mb-1 block">学科/技能</label>
          <div class="flex flex-wrap gap-1">
            <button v-for="s in subjects" :key="s" @click="toggleFilter('subject', s)"
              :class="filters.subject === s ? 'bg-primary/10 text-primary border-primary/30' : 'bg-gray-50 text-gray-600 border-gray-200'"
              class="text-xs px-2 py-1 rounded-full border transition-colors">{{ s }}</button>
          </div>
        </div>

        <div class="mb-3">
          <label class="text-xs text-gray-500 mb-1 block">学校</label>
          <input v-model="filters.school" placeholder="输入学校名称" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none" />
        </div>

        <div class="mb-3">
          <label class="text-xs text-gray-500 mb-1 block">学历</label>
          <select v-model="filters.education" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none bg-white">
            <option value="">不限</option><option>本科</option><option>硕士</option><option>博士</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="text-xs text-gray-500 mb-1 block">所在区域</label>
          <select v-model="filters.location" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none bg-white">
            <option value="">不限</option><option v-for="r in regions" :key="r" :value="r">{{ r }}</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="text-xs text-gray-500 mb-1 block">时薪范围</label>
          <div class="flex gap-1 items-center">
            <input v-model.number="filters.min_rate" type="number" placeholder="最低" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none" />
            <span class="text-gray-400 text-xs">—</span>
            <input v-model.number="filters.max_rate" type="number" placeholder="最高" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none" />
          </div>
        </div>

        <div class="mb-3">
          <label class="text-xs text-gray-500 mb-1 block">教学经验</label>
          <select v-model.number="filters.min_exp" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none bg-white">
            <option :value="0">不限</option><option :value="1">1年以上</option><option :value="2">2年以上</option><option :value="3">3年以上</option><option :value="5">5年以上</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="flex items-center gap-2 text-xs text-gray-600 cursor-pointer">
            <input v-model="filters.verified_only" type="checkbox" class="w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary" /> 仅显示已认证
          </label>
        </div>

        <button @click="search" class="w-full bg-primary hover:bg-secondary text-white text-xs font-medium py-2 rounded-lg transition-colors">🔍 搜索</button>
      </div>

      <div class="flex-1 space-y-3">
        <p v-if="!results.length && !loading" class="text-gray-400 text-center py-12">点击「搜索」查看符合条件的家教</p>
        <p v-if="loading" class="text-gray-400 text-center py-12">搜索中...</p>
        <TutorCard v-for="t in results" :key="t.tutor_id" :tutor="t" @chat="handleChat" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { tutorSearchAPI } from '../api'
import TutorCard from './TutorCard.vue'

const router = useRouter()
const subjects = ['数学', '语文', '英语', '物理', '化学', '生物', '政治', '历史', '地理', '其他外语']
const regions = ['和平区', '南开区', '河西区', '河东区', '河北区', '红桥区', '东丽区', '西青区', '津南区', '北辰区']

const filters = reactive({
  subject: '', school: '', education: '', location: '',
  min_rate: null, max_rate: null, min_exp: 0, verified_only: false
})
const results = ref([])
const loading = ref(false)

function toggleFilter(type, val) {
  filters[type] = filters[type] === val ? '' : val
}

async function search() {
  loading.value = true
  try {
    const params = {}
    if (filters.subject) params.subject = filters.subject
    if (filters.school) params.school = filters.school
    if (filters.education) params.education = filters.education
    if (filters.location) params.location = filters.location
    if (filters.min_rate) params.min_rate = filters.min_rate
    if (filters.max_rate) params.max_rate = filters.max_rate
    if (filters.min_exp) params.min_exp = filters.min_exp
    if (filters.verified_only) params.verified_only = '1'
    const res = await tutorSearchAPI.search(params)
    results.value = res.data
  } catch (e) {
    results.value = []
  } finally {
    loading.value = false
  }
}

function handleChat(tutor) {
  router.push({ path: '/messages', query: { username: tutor.username } })
}
</script>
