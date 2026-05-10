<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white nav-shadow px-6 py-3 flex justify-between items-center">
      <span class="text-xl font-bold text-primary flex items-center"><i class="fa fa-paw mr-2"></i>趣学喵</span>
      <button @click="$router.push('/dashboard')" class="text-sm border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50 transition-colors"><i class="fa fa-arrow-left mr-1"></i>返回工作台</button>
    </nav>
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h2 class="text-xl font-bold text-gray-800 mb-6 flex items-center"><i class="fa fa-user-circle text-primary mr-2"></i>个人信息</h2>

      <form @submit.prevent="save" class="bg-white rounded-xl card-shadow p-6 space-y-6">
        <ProfileBase :form="form" :user-type="auth.user?.user_type" />

        <ParentProfile v-if="auth.user?.user_type === 1" ref="parentRef" :form="form" />
        <TutorProfile v-if="auth.user?.user_type === 2" ref="tutorRef" :form="form" />

        <button :disabled="saving" class="w-full bg-primary hover:bg-secondary text-white font-medium py-3 rounded-lg transition-colors shadow-md disabled:opacity-60">
          <i class="fa fa-save mr-2"></i>{{ saving ? '保存中...' : '保存修改' }}
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
import ProfileBase from '../components/ProfileBase.vue'
import ParentProfile from '../components/ParentProfile.vue'
import TutorProfile from '../components/TutorProfile.vue'

const auth = useAuthStore()
const form = reactive({})
const saving = ref(false); const msg = ref(''); const msgType = ref('')
const parentRef = ref(null); const tutorRef = ref(null)

onMounted(async () => {
  await auth.fetchUser()
  const u = auth.user || {}
  Object.assign(form, u)
  if (u.birthday) form.birthday = u.birthday.slice(0, 10)
})

async function save() {
  saving.value = true; msg.value = ''
  const data = { ...form }

  if (auth.user?.user_type === 1 && parentRef.value) {
    const extra = parentRef.value.getData()
    data.children_info = extra.children_info
    data.preference = extra.preference
  }
  if (auth.user?.user_type === 2 && tutorRef.value) {
    const extra = tutorRef.value.getData()
    data.skills = extra.skills
    data.certificates = extra.certificates
    data.available_time = extra.available_time
  }

  try { await authAPI.updateProfile(data); msg.value = '保存成功'; msgType.value = 'success'; await auth.fetchUser() }
  catch (e) { msg.value = e.response?.data?.msg || '保存失败'; msgType.value = 'error' }
  finally { saving.value = false }
}
</script>
