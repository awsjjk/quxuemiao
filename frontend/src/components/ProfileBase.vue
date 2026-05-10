<template>
  <div class="border-b border-gray-100 pb-4">
    <h3 class="font-semibold text-gray-800 mb-4"><i class="fa fa-id-card text-primary mr-2"></i>账号信息</h3>
    <div class="grid grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
        <input :value="form.username" disabled class="w-full px-3 py-2.5 border border-gray-200 rounded-lg text-sm bg-gray-50 text-gray-400" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">身份</label>
        <input :value="roleText" disabled class="w-full px-3 py-2.5 border border-gray-200 rounded-lg text-sm bg-gray-50 text-gray-400" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">手机号</label>
        <input v-model="form.phone" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
        <input v-model="form.email" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">头像URL</label>
        <input v-model="form.avatar" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">性别</label>
        <select v-model.number="form.sex" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all bg-white">
          <option :value="0">未设置</option><option :value="1">男</option><option :value="2">女</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">生日</label>
        <input v-model="form.birthday" type="date" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
      </div>
      <div></div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">QQ绑定</label>
        <button type="button" @click="showUnavailable" class="w-full px-3 py-2 border border-dashed border-gray-300 rounded-lg text-sm text-gray-400 bg-gray-50 hover:bg-gray-100 transition-colors">🔗 绑定QQ</button>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">微信绑定</label>
        <button type="button" @click="showUnavailable" class="w-full px-3 py-2 border border-dashed border-gray-300 rounded-lg text-sm text-gray-400 bg-gray-50 hover:bg-gray-100 transition-colors">🔗 绑定微信</button>
      </div>
    </div>
    <p v-if="unavailableMsg" class="text-amber-600 text-xs mt-2">{{ unavailableMsg }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({ form: { type: Object, required: true }, userType: { type: Number, default: 1 } })
const unavailableMsg = ref('')

const roleText = computed(() => ({ 1: '家长', 2: '家教', 3: '管理员' }[props.userType] || ''))

function showUnavailable() {
  unavailableMsg.value = '该功能暂不可用'
  setTimeout(() => unavailableMsg.value = '', 3000)
}
</script>
