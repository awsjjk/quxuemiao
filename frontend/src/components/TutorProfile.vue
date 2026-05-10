<template>
  <div class="border-b border-gray-100 pb-4">
    <h3 class="font-semibold text-gray-800 mb-4"><i class="fa fa-graduation-cap text-primary mr-2"></i>家教信息</h3>
    <div class="grid grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">真实姓名</label>
        <input v-model="form.real_name" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">身份证号</label>
        <input v-model="form.id_card" type="password" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">学校</label>
        <input v-model="form.school" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">专业</label>
        <input v-model="form.major" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">年级</label>
        <input v-model="form.grade" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">学历</label>
        <select v-model="form.education" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all bg-white">
          <option value="">请选择</option><option value="本科">本科</option><option value="硕士">硕士</option><option value="博士">博士</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">教学经验(年)</label>
        <input v-model.number="form.teaching_exp" type="number" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">时薪(元/h)</label>
        <input v-model.number="form.hourly_rate" type="number" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">所在区域</label>
        <select v-model="form.location" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all bg-white">
          <option value="">请选择</option>
          <option v-for="r in regions" :key="r" :value="r">{{ r }}</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">认证状态</label>
        <div v-if="form.verification_status === 2" class="w-full px-3 py-2.5 bg-green-50 border border-green-200 rounded-lg text-sm text-green-600 flex items-center gap-2">
          🟢 已认证
        </div>
        <div v-else-if="form.verification_status === 1" class="w-full px-3 py-2.5 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-600">
          📝 审核中...
        </div>
        <div v-else class="w-full px-3 py-1.5 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-700 flex items-center justify-between">
          <span>📝 未认证</span>
          <button type="button" @click="applyVerify" class="text-red-500 underline text-xs hover:text-red-600">申请认证</button>
        </div>
      </div>

      <div class="col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-2">技能标签（点击选择/取消）</label>
        <div class="flex flex-wrap gap-2">
          <button type="button" v-for="s in skillPresets" :key="s" @click="toggleSkill(s)"
            :class="skills.includes(s) ? 'bg-primary/10 text-primary border-primary/30' : 'bg-gray-100 text-gray-600 border-gray-200'"
            class="text-xs px-3 py-1.5 rounded-full border transition-colors">{{ s }}</button>
          <span v-if="showCustomSkill" class="flex items-center gap-1">
            <input v-model="customSkillInput" placeholder="自定义技能" class="text-xs px-2 py-1.5 border border-gray-300 rounded-full w-24 focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none" @keyup.enter="addCustomSkill" />
          </span>
          <button v-else type="button" @click="showCustomSkill = true" class="text-xs px-3 py-1.5 rounded-full border border-dashed border-gray-300 text-gray-400 hover:text-primary hover:border-primary/50 transition-colors">+ 自定义</button>
        </div>
      </div>

      <div class="col-span-2">
        <div class="flex justify-between items-center mb-2">
          <label class="text-sm font-medium text-gray-700">证书/资质</label>
          <button type="button" @click="addCert" class="text-xs text-primary hover:underline">+ 添加证书</button>
        </div>
        <div v-for="(cert, idx) in certs" :key="idx" class="flex items-center justify-between bg-gray-50 rounded-lg px-3 py-2 mb-1 border border-gray-200 text-sm text-gray-700">
          <span>📜 {{ cert }}</span>
          <button type="button" @click="removeCert(idx)" class="text-red-400 hover:text-red-600">✕</button>
        </div>
        <div v-if="showCertInput" class="flex gap-2 mt-2">
          <input v-model="newCertName" placeholder="证书名称" class="flex-1 px-2 py-1.5 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none" @keyup.enter="addCert" />
          <button type="button" @click="addCert" class="text-xs bg-primary text-white px-3 py-1.5 rounded">确认</button>
        </div>
        <p v-if="!certs.length && !showCertInput" class="text-xs text-gray-400">暂无证书</p>
      </div>

      <div class="col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-2">可用时间（点击勾选）</label>
        <div class="inline-grid grid-cols-[auto_repeat(7,1fr)] gap-1 text-center text-xs">
          <div></div>
          <div v-for="d in days" :key="d" class="text-gray-600 py-1">{{ d }}</div>
          <template v-for="slot in timeSlots" :key="slot">
            <div class="text-gray-400 text-right pr-2 py-1">{{ slot }}</div>
            <div v-for="d in days" :key="d + slot"
              @click="toggleTime(d, slot)"
              :class="isTimeSelected(d, slot) ? 'bg-primary/20 border-primary/40' : 'bg-gray-100 border-gray-200 hover:bg-gray-200'"
              class="w-8 h-6 rounded cursor-pointer border transition-colors"></div>
          </template>
        </div>
      </div>

      <div class="col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-1">个人简介</label>
        <textarea v-model="form.introduction" rows="3" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none resize-none transition-all"></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'

const props = defineProps({ form: { type: Object, required: true } })

const regions = ['和平区', '南开区', '河西区', '河东区', '河北区', '红桥区', '东丽区', '西青区', '津南区', '北辰区']
const skillPresets = ['数学', '语文', '英语', '物理', '化学', '生物', '政治', '历史', '地理', '其他外语']
const days = ['一', '二', '三', '四', '五', '六', '日']
const timeSlots = ['上午', '下午', '晚上']

function initData() {
  skills.splice(0, skills.length, ...(props.form.skills?.length ? [...props.form.skills] : []))
  certs.splice(0, certs.length, ...(props.form.certificates?.length ? [...props.form.certificates] : []))
  avail.splice(0, avail.length, ...(props.form.available_time?.length ? [...props.form.available_time] : []))
}

const skills = reactive([])
const certs = reactive([])
const avail = reactive([])

watch(() => props.form.skills, initData, { immediate: true })
watch(() => props.form.certificates, initData, { immediate: true })
watch(() => props.form.available_time, initData, { immediate: true })

const showCustomSkill = ref(false)
const customSkillInput = ref('')
const showCertInput = ref(false)
const newCertName = ref('')

function toggleSkill(s) {
  const idx = skills.indexOf(s)
  idx >= 0 ? skills.splice(idx, 1) : skills.push(s)
}
function addCustomSkill() {
  const v = customSkillInput.value.trim()
  if (v && !skills.includes(v)) { skills.push(v) }
  customSkillInput.value = ''
  showCustomSkill.value = false
}
function addCert() {
  if (showCertInput.value && newCertName.value.trim()) {
    certs.push(newCertName.value.trim())
    newCertName.value = ''
    showCertInput.value = false
  } else {
    showCertInput.value = true
  }
}
function removeCert(idx) { certs.splice(idx, 1) }

function makeTimeKey(d, s) { return d + '_' + s }
function isTimeSelected(d, s) { return avail.includes(makeTimeKey(d, s)) }
function toggleTime(d, s) {
  const key = makeTimeKey(d, s)
  const idx = avail.indexOf(key)
  idx >= 0 ? avail.splice(idx, 1) : avail.push(key)
}

function applyVerify() {
  alert('认证功能即将上线，敬请期待')
}

defineExpose({
  getData: () => ({
    skills: [...skills],
    certificates: [...certs],
    available_time: [...avail],
  })
})
</script>
