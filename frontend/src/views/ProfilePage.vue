<template>
  <div class="page">
    <nav><span class="logo">趣学喵</span><button @click="$router.push('/dashboard')">返回工作台</button></nav>
    <div class="container">
      <h2>个人信息</h2>
      <form @submit.prevent="save">
        <input v-model="form.phone" placeholder="手机号" />
        <input v-model="form.email" placeholder="邮箱" />

        <div v-if="auth.user?.user_type === 1">
          <h3>家长信息</h3>
          <input v-model="form.real_name" placeholder="真实姓名" />
          <input v-model="form.address" placeholder="家庭地址" />
          <input v-model="form.location" placeholder="所在区域" />
        </div>

        <div v-if="auth.user?.user_type === 2">
          <h3>家教信息</h3>
          <input v-model="form.real_name" placeholder="真实姓名" />
          <input v-model="form.school" placeholder="学校" />
          <input v-model="form.major" placeholder="专业" />
          <input v-model="form.grade" placeholder="年级" />
          <input v-model="form.education" placeholder="学历" />
          <input v-model.number="form.teaching_exp" type="number" placeholder="教学经验(年)" />
          <input v-model.number="form.hourly_rate" type="number" placeholder="时薪(元/小时)" />
          <input v-model="form.location" placeholder="所在区域" />
          <textarea v-model="form.introduction" placeholder="个人简介" rows="3"></textarea>
        </div>

        <button :disabled="saving">{{ saving ? '保存中...' : '保存' }}</button>
      </form>
      <p v-if="msg" :class="msgType">{{ msg }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authAPI } from '../api'

const router = useRouter()
const auth = useAuthStore()
const form = reactive({})
const saving = ref(false)
const msg = ref('')
const msgType = ref('')

onMounted(async () => {
  await auth.fetchUser()
  Object.assign(form, auth.user || {})
})

async function save() {
  saving.value = true
  try {
    await authAPI.updateProfile({ ...form })
    msg.value = '保存成功'
    msgType.value = 'success'
  } catch (e) {
    msg.value = e.response?.data?.msg || '保存失败'
    msgType.value = 'error'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.page { min-height:100vh; background:#f5f5f5; }
nav { display:flex; justify-content:space-between; align-items:center; padding:12px 24px; background:#fff; }
.logo { font-size:20px; font-weight:700; color:#2563eb; }
nav button { padding:6px 14px; border:1px solid #d1d5db; border-radius:6px; background:#fff; font-size:13px; cursor:pointer; }
.container { max-width:500px; margin:24px auto; padding:0 16px; }
h2 { color:#1f2937; margin-bottom:16px; }
h3 { color:#374151; margin:16px 0 8px; font-size:15px; }
input, textarea { width:100%; padding:10px; margin-bottom:12px; border:1px solid #d1d5db; border-radius:8px; font-size:14px; box-sizing:border-box; }
button { width:100%; padding:10px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
button:disabled { opacity:0.6; }
.success { color:#16a34a; font-size:13px; }
.error { color:#dc2626; font-size:13px; }
</style>
