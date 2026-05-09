<template>
  <div class="loading">
    <div class="spinner"></div>
    <p>AI 正在为您智能匹配家教...</p>
    <p class="hint">正在分析需求、检索知识库、评估候选家教</p>
  </div>
</template>
<style scoped>
.loading { text-align:center; padding:60px 0; }
.spinner { width:40px; height:40px; border:3px solid #e5e7eb; border-top-color:#2563eb; border-radius:50%; animation:spin 0.8s linear infinite; margin:0 auto 16px; }
@keyframes spin { to { transform:rotate(360deg); } }
p { color:#374151; font-size:15px; }
.hint { color:#9ca3af; font-size:13px; margin-top:4px; }
</style>
