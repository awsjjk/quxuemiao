<template>
  <div class="bg-white rounded-lg card-shadow p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center"><i class="fa fa-star text-yellow-500 mr-2"></i>服务评价</h3>
    <div v-for="dim in dimensions" :key="dim.key" class="flex justify-between items-center mb-3">
      <label class="text-sm text-gray-700">{{ dim.label }}</label>
      <div class="flex gap-1">
        <span v-for="s in 5" :key="s" class="text-2xl cursor-pointer transition-colors" :class="s <= scores[dim.key] ? 'text-yellow-500' : 'text-gray-300'" @click="scores[dim.key] = s">&#9733;</span>
      </div>
    </div>
    <div class="flex justify-between items-center mb-3">
      <label class="text-sm text-gray-700 font-medium">综合评价</label>
      <div class="flex gap-1">
        <span v-for="s in 5" :key="s" class="text-2xl cursor-pointer transition-colors" :class="s <= overall ? 'text-yellow-500' : 'text-gray-300'" @click="overall = s">&#9733;</span>
      </div>
    </div>
    <textarea v-model="comment" placeholder="写下你的评价..." rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none resize-none mb-3"></textarea>
    <button @click="submit" :disabled="loading" class="bg-primary hover:bg-secondary text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors disabled:opacity-60">
      <i class="fa fa-send mr-1"></i>{{ loading ? '提交中...' : '提交评价' }}
    </button>
    <p v-if="msg" :class="msg === '评价成功' ? 'text-green-600' : 'text-red-500'" class="text-sm mt-2">{{ msg }}</p>
  </div>
</template>
<script setup>
import { reactive, ref } from 'vue'
import { ratingAPI } from '../api'
const props = defineProps({ orderId: [Number, String] })
const emit = defineEmits(['submitted'])
const dimensions = [{ key: 'teaching_score', label: '教学能力' }, { key: 'attitude_score', label: '教学态度' }, { key: 'punctuality_score', label: '守时情况' }]
const scores = reactive({ teaching_score: 5, attitude_score: 5, punctuality_score: 5 })
const overall = ref(5)
const comment = ref('')
const loading = ref(false)
const msg = ref('')
async function submit() {
  loading.value = true
  try { await ratingAPI.submit({ order_id: Number(props.orderId), ...scores, overall_score: overall.value, comment: comment.value }); msg.value = '评价成功'; emit('submitted') }
  catch (e) { msg.value = e.response?.data?.msg || '提交失败' }
  finally { loading.value = false }
}
</script>
