<template>
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <BrandMark />
        <p>把每一个值得纪念的日子，<br />做成一口温柔的甜。</p>
      </div>
      <div class="footer-links">
        <div>
          <h4>探索</h4>
          <router-link to="/catalog">全部蛋糕</router-link>
          <a href="/#our-story">品牌故事</a>
          <router-link to="/orders">我的订单</router-link>
        </div>
        <div>
          <h4>服务</h4>
          <a href="#">预订须知</a>
          <a href="#">配送范围</a>
          <a href="#">企业定制</a>
        </div>
        <div>
          <h4>联系我们</h4>
          <p>021-6888 1024</p>
          <p>hello@tunan-cake.cn</p>
          <p>上海 · 徐汇区安福路</p>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 兔南蛋糕零售店</span>
      <span>FRESHLY BAKED WITH LOVE</span>
      <span>沪ICP备2026001024号</span>
    </div>
  </footer>
</template>

<script setup>
import BrandMark from './BrandMark.vue'
</script>

<style scoped>
.site-footer { background: var(--ink); color: #d9cbbd; padding: 70px 0 0; margin-top: 0; }
.footer-inner { max-width: 1200px; margin: 0 auto; padding: 0 32px 64px; display: grid; grid-template-columns: 1.1fr 1.7fr; gap: 90px; }
.footer-brand :deep(.brand-mark) { color: #f3e7d6; }
.footer-brand :deep(.brand-cn) { color: rgba(243,231,214,.55); }
.footer-brand p { margin: 25px 0 0; color: rgba(243,231,214,.55); font-family: var(--font-display); font-size: 18px; line-height: 1.9; letter-spacing: .06em; }
.footer-links { display: grid; grid-template-columns: repeat(3, 1fr); gap: 35px; }
.footer-links h4 { margin: 0 0 20px; color: #f4e7d2; font-size: 11px; letter-spacing: .22em; font-weight: 500; }
.footer-links a, .footer-links p { display: block; color: rgba(243,231,214,.58); text-decoration: none; font-size: 12px; line-height: 2.2; margin: 0; transition: color .2s; }
.footer-links a:hover { color: var(--gold-light); }
.footer-bottom { max-width: 1200px; margin: 0 auto; padding: 22px 32px; display: flex; justify-content: space-between; border-top: 1px solid rgba(243,231,214,.12); font-size: 9px; letter-spacing: .16em; color: rgba(243,231,214,.35); }
@media (max-width: 800px) {
  .footer-inner { grid-template-columns: 1fr; gap: 45px; padding-bottom: 40px; }
  .footer-links { gap: 20px; }
  .footer-bottom { flex-wrap: wrap; gap: 12px; }
}
</style>