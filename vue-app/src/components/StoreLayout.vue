<template>
  <div class="store-shell">
    <AppHeader />
    <main class="store-main"><router-view /></main>
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'
</script>