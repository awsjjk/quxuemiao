<template>
  <div class="rating-form">
    <h3>服务评价</h3>
    <div class="stars">
      <div v-for="dim in dimensions" :key="dim.key" class="dim">
        <label>{{ dim.label }}</label>
        <div class="star-row">
          <span v-for="s in 5" :key="s" :class="starClass(dim.key, s)" @click="scores[dim.key] = s">&#9733;</span>
        </div>
      </div>
    </div>
    <div class="dim">
      <label>综合评价</label>
      <div class="star-row">
        <span v-for="s in 5" :key="s" :class="s <= overall ? 'star on' : 'star'" @click="overall = s">&#9733;</span>
      </div>
    </div>
    <textarea v-model="comment" placeholder="写下你的评价..." rows="3"></textarea>
    <button @click="submit" :disabled="loading">{{ loading ? '提交中...' : '提交评价' }}</button>
    <p v-if="msg">{{ msg }}</p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ratingAPI } from '../api'

const props = defineProps({ orderId: [Number, String] })
const emit = defineEmits(['submitted'])

const dimensions = [
  { key: 'teaching_score', label: '教学能力' },
  { key: 'attitude_score', label: '教学态度' },
  { key: 'punctuality_score', label: '守时情况' }
]
const scores = reactive({ teaching_score: 5, attitude_score: 5, punctuality_score: 5 })
const overall = ref(5)
const comment = ref('')
const loading = ref(false)
const msg = ref('')

function starClass(dim, s) {
  return s <= scores[dim] ? 'star on' : 'star'
}

async function submit() {
  loading.value = true
  try {
    await ratingAPI.submit({
      order_id: Number(props.orderId),
      ...scores,
      overall_score: overall.value,
      comment: comment.value
    })
    msg.value = '评价成功'
    emit('submitted')
  } catch (e) {
    msg.value = e.response?.data?.msg || '提交失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.rating-form { background:#fff; padding:20px; border-radius:10px; }
h3 { margin:0 0 16px; color:#1f2937; }
.dim { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.dim label { font-size:13px; color:#374151; }
.star-row { display:flex; gap:4px; }
.star { font-size:24px; color:#d1d5db; cursor:pointer; transition:color 0.1s; }
.star.on { color:#f59e0b; }
textarea { width:100%; margin:12px 0; padding:10px; border:1px solid #d1d5db; border-radius:8px; font-size:14px; box-sizing:border-box; }
button { padding:8px 20px; background:#2563eb; color:#fff; border:none; border-radius:6px; font-size:14px; cursor:pointer; }
button:disabled { opacity:0.6; }
</style>
