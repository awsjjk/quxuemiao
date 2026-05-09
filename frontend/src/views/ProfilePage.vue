<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white nav-shadow px-6 py-3 flex justify-between items-center">
      <span class="text-xl font-bold text-primary flex items-center"><i class="fa fa-paw mr-2"></i>趣学喵</span>
      <button @click="$router.push('/dashboard')" class="text-sm border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50 transition-colors"><i class="fa fa-arrow-left mr-1"></i>返回工作台</button>
    </nav>
    <div class="max-w-lg mx-auto py-8 px-4">
      <h2 class="text-xl font-bold text-gray-800 mb-6 flex items-center"><i class="fa fa-user-circle text-primary mr-2"></i>个人信息</h2>
      <form @submit.prevent="save" class="bg-white rounded-xl card-shadow p-6 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">手机号</label>
          <input v-model="form.phone" placeholder="手机号" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
          <input v-model="form.email" placeholder="邮箱" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
        </div>

        <div v-if="auth.user?.user_type === 1" class="pt-2 border-t border-gray-100">
          <h3 class="font-semibold text-gray-800 mb-3"><i class="fa fa-user mr-2 text-primary"></i>家长信息</h3>
          <div class="grid grid-cols-2 gap-3">
            <input v-model="form.real_name" placeholder="真实姓名" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
            <input v-model="form.location" placeholder="所在区域" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
          </div>
          <input v-model="form.address" placeholder="家庭地址" class="w-full mt-3 px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
        </div>

        <div v-if="auth.user?.user_type === 2" class="pt-2 border-t border-gray-100">
          <h3 class="font-semibold text-gray-800 mb-3"><i class="fa fa-graduation-cap mr-2 text-primary"></i>家教信息</h3>
          <div class="grid grid-cols-2 gap-3">
            <input v-model="form.real_name" placeholder="真实姓名" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
            <input v-model="form.school" placeholder="学校" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
            <input v-model="form.major" placeholder="专业" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
            <input v-model="form.grade" placeholder="年级" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
            <input v-model="form.education" placeholder="学历" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
            <input v-model.number="form.teaching_exp" type="number" placeholder="教学经验(年)" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
            <input v-model.number="form.hourly_rate" type="number" placeholder="时薪(元/小时)" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
            <input v-model="form.location" placeholder="所在区域" class="px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
          </div>
          <textarea v-model="form.introduction" placeholder="个人简介" rows="3" class="w-full mt-3 px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none resize-none transition-all"></textarea>
        </div>

        <button :disabled="saving" class="w-full bg-primary hover:bg-secondary text-white font-medium py-3 rounded-lg transition-colors shadow-md disabled:opacity-60">
          <i class="fa fa-save mr-2"></i>{{ saving ? '保存中...' : '保存' }}
        </button>
        <p v-if="msg" :class="msgType === 'success' ? 'text-green-600' : 'text-red-500'" class="text-sm text-center">{{ msg }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { authAPI } from '../api'
const auth = useAuthStore()
const form = reactive({})
const saving = ref(false); const msg = ref(''); const msgType = ref('')
onMounted(async () => { await auth.fetchUser(); Object.assign(form, auth.user || {}) })
async function save() {
  saving.value = true
  try { await authAPI.updateProfile({ ...form }); msg.value = '保存成功'; msgType.value = 'success' }
  catch (e) { msg.value = e.response?.data?.msg || '保存失败'; msgType.value = 'error' }
  finally { saving.value = false }
}
</script>
