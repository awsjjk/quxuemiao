<template>
  <router-view />
  <AIAssistantFAB v-if="isLoggedIn" />
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from './stores/auth'
import AIAssistantFAB from './components/AIAssistantFAB.vue'

const auth = useAuthStore()
const isLoggedIn = computed(() => auth.isLoggedIn)
</script>
