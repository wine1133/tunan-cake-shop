<template>
  <div class="admin-page-head">
    <div>
      <span class="eyebrow">{{ eyebrow }}</span>
      <h1>{{ title }}</h1>
      <p>{{ subtitle }}</p>
    </div>
    <div class="admin-page-actions"><slot /></div>
  </div>
</template>

<script setup>
defineProps({
  eyebrow: { type: String, default: 'MANAGEMENT' },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' }
})
</script>

<style scoped>
.admin-page-head { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 24px; }
.admin-page-head h1 { font-family: var(--font-display); font-size: 40px; font-weight: 500; line-height: 1; margin: 9px 0 7px; letter-spacing: -.02em; }
.admin-page-head p { color: var(--ink-muted); font-size: 10px; margin: 0; }
.admin-page-actions { display: flex; gap: 8px; }
@media (max-width: 650px) {
  .admin-page-head { align-items: flex-start; flex-direction: column; gap: 16px; }
  .admin-page-head h1 { font-size: 34px; }
  .admin-page-actions { width: 100%; }
  .admin-page-actions :deep(.btn) { flex: 1; }
}
</style>