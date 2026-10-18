<template>
  <div class="account-header">
    <div>
      <span class="eyebrow">{{ eyebrow }}</span>
      <h1>{{ title }}</h1>
      <p>{{ subtitle }}</p>
    </div>
    <nav class="account-tabs">
      <router-link to="/orders">我的订单</router-link>
      <router-link to="/addresses">收货地址</router-link>
      <router-link to="/profile">个人中心</router-link>
    </nav>
  </div>
</template>

<script setup>
defineProps({
  eyebrow: { type: String, default: 'MY TU NAN' },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' }
})
</script>