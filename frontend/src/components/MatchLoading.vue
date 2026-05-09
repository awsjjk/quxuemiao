<template>
  <div class="text-center py-16">
    <div class="w-10 h-10 border-3 border-gray-200 border-t-primary rounded-full animate-spin mx-auto mb-4"></div>
    <p class="text-gray-700 text-base">AI 正在为您智能匹配家教...</p>
    <p class="text-gray-400 text-sm mt-1">正在分析需求、检索知识库、评估候选家教</p>
  </div>
</template>
<style scoped>
.animate-spin { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
