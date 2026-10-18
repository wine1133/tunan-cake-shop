<template>
  <article class="product-card" @click="$emit('order', product)">
    <div class="product-image">
      <img :src="product.img" :alt="product.name" loading="lazy" />
      <span v-if="product.tag" class="product-tag">{{ product.tag }}</span>
      <button class="favorite" :class="{ active: liked }" @click.stop="liked = !liked" aria-label="收藏">
        <el-icon><StarFilled /></el-icon>
      </button>
      <div class="quick-view"><span>查看并预订</span><el-icon><Right /></el-icon></div>
    </div>
    <div class="product-body">
      <div class="product-meta">
        <span>{{ product.categoryName }}</span>
        <span class="rating"><el-icon><StarFilled /></el-icon>{{ product.rating || 4.9 }}</span>
      </div>
      <h3>{{ product.name }}</h3>
      <p>{{ product.description }}</p>
      <div class="product-foot">
        <div class="price"><small>¥</small>{{ money(product.price) }}<em>/{{ product.unit }}</em></div>
        <button class="order-button" :disabled="product.num <= 0" @click.stop="$emit('order', product)">
          {{ product.num > 0 ? '预订' : '售罄' }}
          <el-icon><ArrowRight /></el-icon>
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { ref } from 'vue'
import { money } from '../utils/format'

defineProps({ product: { type: Object, required: true } })
defineEmits(['order'])
const liked = ref(false)
</script>

<style scoped>
.product-card { background: rgba(255,250,244,.82); border: 1px solid var(--line); border-radius: 22px; overflow: hidden; cursor: pointer; transition: transform .45s cubic-bezier(.2,.7,.2,1), box-shadow .45s; }
.product-card:hover { transform: translateY(-7px); box-shadow: 0 26px 60px rgba(65,43,35,.13); }
.product-image { position: relative; height: 345px; overflow: hidden; background: #eadfd2; }
.product-image img { width: 100%; height: 100%; object-fit: cover; transition: transform .8s cubic-bezier(.2,.7,.2,1); }
.product-card:hover .product-image img { transform: scale(1.055); }
.product-image::after { content: ''; position: absolute; inset: 0; background: linear-gradient(to top, rgba(43,28,24,.24), transparent 35%); opacity: 0; transition: .4s; }
.product-card:hover .product-image::after { opacity: 1; }
.product-tag { position: absolute; z-index: 2; left: 14px; top: 14px; padding: 7px 11px; border-radius: 999px; background: rgba(255,250,244,.9); backdrop-filter: blur(8px); color: var(--rose-deep); font-size: 9px; font-weight: 700; letter-spacing: .08em; }
.favorite { position: absolute; z-index: 3; right: 13px; top: 13px; width: 33px; height: 33px; border-radius: 50%; border: 0; background: rgba(255,250,244,.82); color: #9c8980; display: grid; place-items: center; cursor: pointer; backdrop-filter: blur(8px); transition: .2s; }
.favorite.active { color: var(--rose); }
.favorite:hover { transform: scale(1.08); }
.quick-view { position: absolute; z-index: 2; bottom: 16px; left: 18px; right: 18px; display: flex; justify-content: space-between; align-items: center; color: white; font-size: 11px; letter-spacing: .08em; opacity: 0; transform: translateY(8px); transition: .4s; }
.product-card:hover .quick-view { opacity: 1; transform: translateY(0); }
.product-body { padding: 20px 21px 21px; }
.product-meta { display: flex; justify-content: space-between; color: var(--ink-muted); font-size: 9px; letter-spacing: .1em; text-transform: uppercase; }
.rating { display: flex; align-items: center; gap: 4px; color: var(--gold); }
.rating .el-icon { font-size: 10px; }
h3 { font-family: var(--font-display); font-size: 24px; font-weight: 600; margin: 9px 0 7px; letter-spacing: .01em; }
p { margin: 0; color: var(--ink-soft); font-size: 11px; line-height: 1.7; height: 37px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
.product-foot { margin-top: 18px; padding-top: 15px; border-top: 1px solid var(--line); display: flex; align-items: center; justify-content: space-between; }
.price { font-family: var(--font-display); font-size: 25px; font-weight: 600; color: var(--ink); }
.price small { font-size: 13px; margin-right: 2px; }
.price em { font-family: var(--font-body); font-size: 9px; color: var(--ink-muted); font-style: normal; font-weight: 400; margin-left: 3px; }
.order-button { border: 0; background: var(--rose-pale); color: var(--rose-deep); border-radius: 999px; height: 36px; padding: 0 15px; cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 10px; font-weight: 700; letter-spacing: .07em; transition: .25s; }
.order-button:hover { background: var(--rose-deep); color: white; }
.order-button:disabled { background: #eee7df; color: #9d8e85; cursor: not-allowed; }
@media (max-width: 700px) { .product-image { height: 300px; } }
</style>