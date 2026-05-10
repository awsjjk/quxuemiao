<template>
  <div class="fixed bottom-6 right-6 z-50 flex items-center gap-3">
    <span class="hidden sm:block bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-xs text-gray-600 shadow-sm">💬 需要帮助吗？</span>
    <button
      @click="$router.push('/ai-assistant')"
      class="w-13 h-13 rounded-full bg-gradient-to-br from-primary to-purple-500 flex items-center justify-center shadow-lg shadow-primary/30 hover:shadow-xl hover:shadow-primary/40 hover:scale-105 transition-all">
      <span class="text-2xl">🤖</span>
    </button>
  </div>
</template>
