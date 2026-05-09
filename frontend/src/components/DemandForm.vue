<template>
  <div class="demand-form">
    <h3>发布家教需求</h3>
    <form @submit.prevent="submit">
      <div class="row">
        <input v-model="form.title" placeholder="标题（如：高一数学辅导）" required />
        <select v-model="form.subject" required>
          <option value="">选择学科</option>
          <option value="数学">数学</option><option value="语文">语文</option>
          <option value="英语">英语</option><option value="物理">物理</option>
          <option value="化学">化学</option>
        </select>
      </div>
      <div class="row">
        <select v-model="form.grade" required>
          <option value="">选择年级</option>
          <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
        </select>
        <input v-model="form.location" placeholder="所在区域（如：南开区）" />
      </div>
      <input v-model.number="form.budget" type="number" placeholder="预算（元/小时）" />
      <textarea v-model="form.description" placeholder="详细描述孩子的学习情况、薄弱环节..." rows="3"></textarea>
      <input v-model="form.requirements" placeholder="额外要求（如：有耐心、女老师优先）" />
      <div class="row">
        <input v-model.number="form.duration" type="number" placeholder="每次课时长(小时)" min="1" max="4" />
        <select v-model="form.frequency">
          <option value="">上课频率</option>
          <option value="每周1次">每周1次</option><option value="每周2次">每周2次</option>
          <option value="每周3次">每周3次</option><option value="每天">每天</option>
        </select>
      </div>
      <label class="urgent"><input type="checkbox" v-model="form.is_urgent" /> 紧急需求</label>
      <button :disabled="loading">{{ loading ? '发布中...' : '发布需求' }}</button>
    </form>
    <p v-if="msg" :class="msgType">{{ msg }}</p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useDemandStore } from '../stores/demand'

const emit = defineEmits(['created'])
const store = useDemandStore()
const grades = ['小学一年级','小学二年级','小学三年级','小学四年级','小学五年级','小学六年级',
  '初一','初二','初三','高一','高二','高三']
const form = reactive({
  title: '', subject: '', grade: '', location: '', budget: null, description: '',
  requirements: '', duration: null, frequency: '', is_urgent: false
})
const loading = ref(false)
const msg = ref('')
const msgType = ref('')

async function submit() {
  loading.value = true
  msg.value = ''
  try {
    await store.create({ ...form, time_slots: [], tags: [] })
    msg.value = '发布成功'
    msgType.value = 'success'
    emit('created')
  } catch (e) {
    msg.value = e.response?.data?.msg || '发布失败'
    msgType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.demand-form { background:#fff; padding:24px; border-radius:12px; box-shadow:0 1px 6px rgba(0,0,0,0.06); max-width:600px; margin:0 auto; }
h3 { margin:0 0 16px; color:#1f2937; }
.row { display:flex; gap:12px; }
.row > * { flex:1; }
input, select, textarea { width:100%; padding:10px; margin-bottom:12px; border:1px solid #d1d5db; border-radius:8px; font-size:14px; box-sizing:border-box; }
.urgent { display:flex; align-items:center; gap:6px; font-size:13px; color:#6b7280; margin-bottom:12px; }
.urgent input { width:auto; margin:0; }
button { width:100%; padding:10px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
button:disabled { opacity:0.6; }
.success { color:#16a34a; font-size:13px; margin-top:8px; }
.error { color:#dc2626; font-size:13px; margin-top:8px; }
</style>
