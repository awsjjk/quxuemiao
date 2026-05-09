<template>
  <div class="bg-white rounded-xl card-shadow p-6 fade-in">
    <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
      <i class="fa fa-edit text-primary mr-2"></i>发布家教需求
    </h3>
    <form @submit.prevent="submit" class="space-y-3">
      <div class="grid grid-cols-2 gap-3">
        <input v-model="form.title" placeholder="标题（如：高一数学辅导）" required class="col-span-2 px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
        <select v-model="form.subject" required class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all">
          <option value="">选择学科</option>
          <option value="数学">数学</option><option value="语文">语文</option>
          <option value="英语">英语</option><option value="物理">物理</option>
          <option value="化学">化学</option>
        </select>
        <select v-model="form.grade" required class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all">
          <option value="">选择年级</option>
          <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>
      <div class="grid grid-cols-2 gap-3">
        <input v-model="form.location" placeholder="所在区域（如：南开区）" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
        <input v-model.number="form.budget" type="number" placeholder="预算（元/小时）" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <textarea v-model="form.description" placeholder="详细描述孩子的学习情况、薄弱环节..." rows="3" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all resize-none"></textarea>
      <input v-model="form.requirements" placeholder="额外要求（如：有耐心、女老师优先）" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      <div class="grid grid-cols-2 gap-3">
        <input v-model.number="form.duration" type="number" placeholder="每次课时长(小时)" min="1" max="4" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
        <select v-model="form.frequency" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all">
          <option value="">上课频率</option>
          <option value="每周1次">每周1次</option><option value="每周2次">每周2次</option>
          <option value="每周3次">每周3次</option><option value="每天">每天</option>
        </select>
      </div>
      <label class="flex items-center gap-2 text-sm text-gray-500"><input type="checkbox" v-model="form.is_urgent" class="w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary" /> 紧急需求</label>
      <button :disabled="loading" class="w-full bg-primary hover:bg-secondary text-white font-medium py-3 rounded-lg transition-colors shadow-md hover:shadow-lg disabled:opacity-60">
        <i class="fa fa-paper-plane mr-2"></i>{{ loading ? '发布中...' : '发布需求' }}
      </button>
    </form>
    <p v-if="msg" :class="msgType === 'success' ? 'text-green-600' : 'text-red-500'" class="text-sm mt-3 text-center">{{ msg }}</p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useDemandStore } from '../stores/demand'
const emit = defineEmits(['created'])
const store = useDemandStore()
const grades = ['小学一年级','小学二年级','小学三年级','小学四年级','小学五年级','小学六年级','初一','初二','初三','高一','高二','高三']
const form = reactive({ title: '', subject: '', grade: '', location: '', budget: null, description: '', requirements: '', duration: null, frequency: '', is_urgent: false })
const loading = ref(false)
const msg = ref('')
const msgType = ref('')
async function submit() {
  loading.value = true; msg.value = ''
  try { await store.create({ ...form, time_slots: [], tags: [] }); msg.value = '发布成功'; msgType.value = 'success'; emit('created') }
  catch (e) { msg.value = e.response?.data?.msg || '发布失败'; msgType.value = 'error' }
  finally { loading.value = false }
}
</script>
