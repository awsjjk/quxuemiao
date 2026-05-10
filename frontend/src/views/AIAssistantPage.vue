<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white nav-shadow px-6 py-3 flex justify-between items-center">
      <span class="text-xl font-bold text-primary flex items-center"><i class="fa fa-paw mr-2"></i>趣学喵</span>
      <button @click="$router.push('/dashboard')" class="text-sm border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50 transition-colors"><i class="fa fa-arrow-left mr-1"></i>返回</button>
    </nav>

    <div class="max-w-2xl mx-auto py-8 px-4">
      <div class="text-center mb-6">
        <div class="w-16 h-16 rounded-full bg-purple-50 flex items-center justify-center mx-auto mb-3">
          <span class="text-3xl">🤖</span>
        </div>
        <h2 class="text-lg font-bold text-gray-800">趣学喵AI助手</h2>
        <p class="text-sm text-gray-500 mt-1">我是您的专属助手，可以帮您了解平台、解答疑问</p>
      </div>

      <div class="bg-white rounded-xl card-shadow p-4 mb-4 h-96 overflow-y-auto space-y-3" ref="chatBox">
        <div v-if="!messages.length" class="text-center py-8">
          <p class="text-gray-400 text-sm mb-4">👇 您可以点击以下常见问题，或直接输入您的问题</p>
          <div class="flex flex-wrap justify-center gap-2">
            <button v-for="faq in faqList" :key="faq.id" @click="askFaq(faq)"
              class="text-xs px-3 py-1.5 rounded-full bg-gray-100 text-gray-600 hover:bg-primary/10 hover:text-primary border border-gray-200 hover:border-primary/30 transition-colors">
              {{ faq.question }}
            </button>
          </div>
        </div>

        <div v-for="(m, idx) in messages" :key="idx" :class="m.role === 'user' ? 'flex justify-end' : 'flex justify-start'">
          <div :class="m.role === 'user' ? 'bg-primary text-white' : 'bg-gray-100 text-gray-800'" class="max-w-sm px-4 py-2 rounded-xl text-sm">
            {{ m.content }}
          </div>
        </div>

        <div v-if="loading" class="flex justify-start">
          <div class="bg-gray-100 text-gray-400 px-4 py-2 rounded-xl text-sm">正在思考...</div>
        </div>
      </div>

      <form @submit.prevent="sendMsg" class="flex gap-3">
        <input v-model="inputText" placeholder="输入您的问题..." class="flex-1 px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
        <button type="submit" :disabled="!inputText.trim() || loading" class="bg-primary hover:bg-secondary text-white text-sm px-5 py-2 rounded-lg transition-colors disabled:opacity-50">
          <i class="fa fa-send"></i>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { aiAssistantAPI } from '../api'

const messages = ref([])
const inputText = ref('')
const loading = ref(false)
const chatBox = ref(null)
const faqList = ref([])

onMounted(async () => {
  try {
    const res = await aiAssistantAPI.faqList()
    faqList.value = res.data
  } catch (e) {
    // FAQ加载失败不影响使用
  }
})

async function askFaq(faq) {
  messages.value.push({ role: 'user', content: faq.question })
  loading.value = true
  await scrollDown()
  try {
    const res = await aiAssistantAPI.chat({ message: faq.question, faq_id: faq.id })
    messages.value.push({ role: 'assistant', content: res.data.reply })
  } catch (e) {
    messages.value.push({ role: 'assistant', content: '抱歉，出现了一些问题，请稍后再试。' })
  } finally {
    loading.value = false
    await scrollDown()
  }
}

async function sendMsg() {
  const text = inputText.value.trim()
  if (!text || loading.value) return
  messages.value.push({ role: 'user', content: text })
  inputText.value = ''
  loading.value = true
  await scrollDown()
  try {
    const res = await aiAssistantAPI.chat({ message: text })
    messages.value.push({ role: 'assistant', content: res.data.reply })
  } catch (e) {
    messages.value.push({ role: 'assistant', content: '抱歉，出现了一些问题，请稍后再试。' })
  } finally {
    loading.value = false
    await scrollDown()
  }
}

async function scrollDown() {
  await nextTick()
  if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight
}
</script>
