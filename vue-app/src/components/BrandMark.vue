<template>
  <div class="brand-mark" :class="{ compact }">
    <span class="brand-emblem" aria-hidden="true">
      <svg viewBox="0 0 54 54" fill="none">
        <circle cx="27" cy="27" r="25.5" stroke="currentColor" stroke-opacity=".35"/>
        <path d="M14 33.5c0-3 2.4-5.5 5.5-5.5h15c3 0 5.5 2.5 5.5 5.5v3H14v-3Z" fill="currentColor" opacity=".95"/>
        <path d="M19 28c0-5.3 3.6-9.5 8-9.5s8 4.2 8 9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <path d="M27 14.5v-3M24 12.7h6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
        <path d="M12 39h30" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" opacity=".8"/>
      </svg>
    </span>
    <span class="brand-copy">
      <span class="brand-en">TU NAN</span>
      <span class="brand-cn">兔南蛋糕零售店</span>
    </span>
  </div>
</template>

<script setup>
defineProps({ compact: Boolean })
</script>

<style scoped>
.brand-mark { display: inline-flex; align-items: center; gap: 11px; color: var(--ink); text-decoration: none; }
.brand-emblem { width: 44px; height: 44px; display: grid; place-items: center; }
.brand-emblem svg { width: 100%; height: 100%; }
.brand-copy { display: flex; flex-direction: column; line-height: 1; }
.brand-en { font-family: var(--font-display); font-size: 18px; letter-spacing: .22em; font-weight: 600; }
.brand-cn { margin-top: 6px; font-size: 11px; font-weight: 500; letter-spacing: .16em; color: var(--ink-soft); padding-left: 2px; white-space: nowrap; }
.compact .brand-emblem { width: 38px; height: 38px; }
</style>