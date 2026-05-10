<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white nav-shadow px-6 py-3 flex justify-between items-center">
      <span class="text-xl font-bold text-primary flex items-center"><i class="fa fa-paw mr-2"></i>趣学喵</span>
      <button @click="$router.push('/dashboard')" class="text-sm border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50 transition-colors"><i class="fa fa-arrow-left mr-1"></i>返回</button>
    </nav>
    <div class="max-w-4xl mx-auto py-8 px-4">
      <!-- 会话列表 -->
      <div v-if="!activePartner">
        <h2 class="text-xl font-bold text-gray-800 mb-4"><i class="fa fa-envelope text-primary mr-2"></i>消息</h2>
        <div v-if="convs.length" class="space-y-2">
          <div v-for="c in convs" :key="c.partner_id" @click="openChat(c.partner_id, c.partner_name)" class="bg-white rounded-lg p-4 border border-gray-100 hover:shadow-md cursor-pointer transition-shadow flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-light flex items-center justify-center flex-shrink-0"><i class="fa fa-user text-primary"></i></div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between">
                <span class="font-medium text-gray-800">
                  {{ c.partner_name }}
                  <span v-if="c.partner_role" :class="c.partner_role === '家长' ? 'text-xs bg-orange-50 text-orange-600 px-1 py-0.5 rounded ml-1' : 'text-xs bg-blue-50 text-blue-600 px-1 py-0.5 rounded ml-1'">{{ c.partner_role }}</span>
                </span>
                <span class="text-xs text-gray-400">{{ c.last_time?.slice(0, 16) }}</span>
              </div>
              <p class="text-sm text-gray-500 truncate">{{ c.last_message || '暂无消息' }}</p>
            </div>
            <span v-if="c.unread" class="bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">{{ c.unread }}</span>
          </div>
        </div>
        <div v-else class="text-center py-20 text-gray-400"><i class="fa fa-inbox text-5xl mb-3 block"></i><p>暂无会话</p></div>

        <!-- 新会话 -->
        <div class="mt-6 bg-white rounded-xl card-shadow p-4">
          <h3 class="font-semibold text-gray-800 mb-3"><i class="fa fa-plus-circle text-primary mr-2"></i>发起新会话</h3>
          <form @submit.prevent="startChat" class="flex gap-3">
            <input v-model="newPartnerName" type="text" placeholder="输入对方用户名" required class="flex-1 px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
            <button type="submit" class="bg-primary hover:bg-secondary text-white text-sm px-4 py-2 rounded-lg transition-colors">开始聊天</button>
          </form>
          <p v-if="searchError" class="text-red-500 text-xs mt-2">{{ searchError }}</p>
        </div>
      </div>

      <!-- 聊天界面 -->
      <div v-else>
        <div class="flex items-center gap-3 mb-4">
          <button @click="activePartner = null" class="text-gray-500 hover:text-gray-700"><i class="fa fa-arrow-left"></i></button>
          <h2 class="text-lg font-bold text-gray-800">{{ activePartnerName }}</h2>
        </div>
        <div class="bg-white rounded-xl card-shadow p-4 h-96 overflow-y-auto mb-4 space-y-3" ref="chatBox">
          <div v-for="m in messages" :key="m.id" :class="m.sender_id === myId ? 'flex justify-end' : 'flex justify-start'">
            <div :class="m.sender_id === myId ? 'bg-primary text-white' : 'bg-gray-100 text-gray-800'" class="max-w-xs px-4 py-2 rounded-xl text-sm">{{ m.content }}</div>
          </div>
          <div v-if="!messages.length" class="text-center py-12 text-gray-400">暂无消息</div>
        </div>
        <form @submit.prevent="sendMsg" class="flex gap-3">
          <input v-model="newMsg" placeholder="输入消息..." required class="flex-1 px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
          <button type="submit" class="bg-primary hover:bg-secondary text-white text-sm px-6 py-2 rounded-lg transition-colors"><i class="fa fa-send"></i></button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { messageAPI } from '../api'
const route = useRoute(); const auth = useAuthStore()
const convs = ref([])
const activePartner = ref(null); const activePartnerName = ref('')
const messages = ref([]); const newMsg = ref(''); const newPartnerName = ref('')
const chatBox = ref(null); const searchError = ref('')
const myId = ref(0)

onMounted(async () => {
  if (!auth.user) await auth.fetchUser()
  myId.value = auth.user?.id || 0
  const res = await messageAPI.conversations(); convs.value = res.data
  if (route.params.partner_id) {
    activePartner.value = Number(route.params.partner_id)
  } else if (route.query.username) {
    const name = route.query.username
    try {
      const userRes = await messageAPI.searchUser(name)
      openChat(userRes.data.id, userRes.data.username)
    } catch (e) {
      searchError.value = '用户不存在'
    }
  }
})

async function startChat() {
  searchError.value = ''
  const name = newPartnerName.value.trim()
  if (!name) return
  if (name === auth.user?.username) {
    searchError.value = '不能给自己发消息'
    return
  }
  try {
    const res = await messageAPI.searchUser(name)
    openChat(res.data.id, res.data.username)
    newPartnerName.value = ''
  } catch (e) {
    searchError.value = e.response?.data?.msg || '用户不存在'
  }
}

function openChat(id, name) { activePartner.value = id; activePartnerName.value = name; loadMessages() }
async function loadMessages() { const res = await messageAPI.chat(activePartner.value); messages.value = res.data; await nextTick(); chatBox.value?.scrollTo(0, chatBox.value.scrollHeight) }
async function sendMsg() {
  const content = newMsg.value.trim(); if (!content) return
  const partner = convs.value.find(c => c.partner_id === activePartner.value)
  const receiverUsername = partner?.partner_name || activePartnerName.value
  await messageAPI.send({ receiver_username: receiverUsername, content, msg_type: 1 })
  newMsg.value = ''; loadMessages()
}
let pollTimer = null
watch(activePartner, () => {
  if (activePartner.value) { loadMessages(); pollTimer = setInterval(loadMessages, 5000) }
  else { clearInterval(pollTimer) }
})
onUnmounted(() => clearInterval(pollTimer))
</script>
