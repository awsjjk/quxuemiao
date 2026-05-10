<template>
  <div class="border-b border-gray-100 pb-4">
    <h3 class="font-semibold text-gray-800 mb-4"><i class="fa fa-home text-primary mr-2"></i>家长信息</h3>
    <div class="grid grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">真实姓名</label>
        <input v-model="form.real_name" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">所在区域</label>
        <select v-model="form.location" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all bg-white">
          <option value="">请选择</option>
          <option v-for="r in regions" :key="r" :value="r">{{ r }}</option>
        </select>
      </div>
      <div class="col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-1">家庭地址</label>
        <input v-model="form.address" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>

      <div class="col-span-2">
        <div class="flex justify-between items-center mb-2">
          <label class="text-sm font-medium text-gray-700">孩子信息</label>
          <button type="button" @click="addChild" class="text-xs text-primary hover:underline">+ 添加孩子</button>
        </div>
        <div v-for="(child, idx) in children" :key="idx" class="flex gap-2 items-center mb-2 bg-gray-50 rounded-lg p-2 border border-gray-200">
          <input v-model="child.name" placeholder="姓名" class="flex-1 px-2 py-1.5 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none" />
          <input v-model="child.grade" placeholder="年级" class="flex-1 px-2 py-1.5 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none" />
          <input v-model.number="child.age" type="number" placeholder="年龄" class="w-16 px-2 py-1.5 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none" />
          <button type="button" @click="removeChild(idx)" class="text-red-400 hover:text-red-600">✕</button>
        </div>
        <p v-if="!children.length" class="text-xs text-gray-400">暂无孩子信息，点击上方按钮添加</p>
      </div>

      <div class="col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-2">学科偏好</label>
        <div class="flex flex-wrap gap-2">
          <button type="button" v-for="s in subjects" :key="s" @click="toggleTag('subjects', s)"
            :class="pref.subjects.includes(s) ? 'bg-primary/10 text-primary border-primary/30' : 'bg-gray-100 text-gray-600 border-gray-200'"
            class="text-xs px-3 py-1.5 rounded-full border transition-colors">{{ s }}</button>
        </div>
      </div>
      <div class="col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-2">时间偏好</label>
        <div class="flex flex-wrap gap-2">
          <button type="button" v-for="t in timeOptions" :key="t" @click="toggleTag('times', t)"
            :class="pref.times.includes(t) ? 'bg-primary/10 text-primary border-primary/30' : 'bg-gray-100 text-gray-600 border-gray-200'"
            class="text-xs px-3 py-1.5 rounded-full border transition-colors">{{ t }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({ form: { type: Object, required: true } })

const regions = ['和平区', '南开区', '河西区', '河东区', '河北区', '红桥区', '东丽区', '西青区', '津南区', '北辰区']
const subjects = ['数学', '语文', '英语', '物理', '化学', '生物', '政治', '历史', '地理', '其他外语']
const timeOptions = ['工作日晚上', '周末上午', '周末下午', '周末晚上', '每天']

const children = reactive(props.form.children_info?.length ? [...props.form.children_info] : [])
const pref = reactive({
  subjects: props.form.preference?.subjects || [],
  times: props.form.preference?.times || []
})

function addChild() { children.push({ name: '', grade: '', age: null }) }
function removeChild(idx) { children.splice(idx, 1) }
function toggleTag(type, val) {
  const arr = pref[type]
  const idx = arr.indexOf(val)
  idx >= 0 ? arr.splice(idx, 1) : arr.push(val)
}

defineExpose({
  getData: () => ({
    children_info: children.filter(c => c.name),
    preference: { subjects: [...pref.subjects], times: [...pref.times] }
  })
})
</script>
