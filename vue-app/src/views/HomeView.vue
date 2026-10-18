<template>
  <div class="home-page">
    <section class="hero">
      <div class="hero-orbit orbit-one"></div>
      <div class="hero-orbit orbit-two"></div>
      <div class="container hero-inner">
        <div class="hero-copy">
          <div class="hero-eyebrow animate-up"><span></span>HANDCRAFTED WITH LOVE · SHANGHAI</div>
          <h1 class="animate-up delay-1">你是我今生<br /><em>最美的相遇</em></h1>
          <p class="hero-desc animate-up delay-2">
            我们相信，甜点不只是味觉的犒赏。<br />
            它是纪念日的仪式，也是平凡日常里，认真生活的小证据。
          </p>
          <div class="hero-actions animate-up delay-3">
            <router-link to="/catalog" class="btn btn-primary">挑选今日蛋糕 <el-icon><ArrowRight /></el-icon></router-link>
            <a href="#our-story" class="btn btn-outline">了解兔南故事</a>
          </div>
          <div class="hero-numbers animate-up delay-3">
            <div><strong>12<small>年</small></strong><span>手作经验</span></div>
            <div><strong>36<small>+</small></strong><span>季节配方</span></div>
            <div><strong>4.9<small>★</small></strong><span>口碑评分</span></div>
          </div>
        </div>
        <div class="hero-visual animate-up delay-2">
          <HeroMediaCarousel />
          <div class="float-card fresh-card">
            <span class="fresh-icon"><el-icon><Sunrise /></el-icon></span>
            <div><strong>每日鲜作</strong><span>下单后新鲜制作</span></div>
          </div>
          <div class="float-card rating-card">
            <span class="rating-stars">★★★★★</span>
            <div><strong>2,800+ 位</strong><span>甜品爱好者的选择</span></div>
          </div>
          <div class="hero-side-note">EST. 2014 · SHANGHAI</div>
        </div>
      </div>
    </section>

    <section class="service-strip">
      <div class="container service-grid">
        <div class="service-item">
          <el-icon><Drizzling /></el-icon>
          <div><strong>当日新鲜手作</strong><span>不使用预制品，每一只蛋糕都从零开始</span></div>
        </div>
        <div class="service-item">
          <el-icon><Van /></el-icon>
          <div><strong>专业冷链配送</strong><span>上海市内全程控温，完好送达</span></div>
        </div>
        <div class="service-item">
          <el-icon><Present /></el-icon>
          <div><strong>心意包装</strong><span>附赠餐具、生日蜡烛与手写贺卡</span></div>
        </div>
      </div>
    </section>

    <section class="notice-ribbon" v-if="notices.length">
      <div class="container notice-inner">
        <span class="notice-label"><el-icon><BellFilled /></el-icon> 兔南播报</span>
        <div class="notice-track"><span>{{ notices[0].name }}</span><em>{{ notices[0].content }}</em></div>
        <span class="notice-date">{{ notices[0].time }}</span>
      </div>
    </section>

    <section class="section category-section">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">FIND YOUR FAVORITE</span>
          <h2>今天，想吃哪一种甜？</h2>
          <p>从轻盈的戚风到醇厚的巧克力，每一种心情，都有刚刚好的答案。</p>
        </div>
        <div class="category-grid" v-loading="loading">
          <router-link v-for="(category, index) in categories" :key="category.id" :to="{ path: '/catalog', query: { category: category.id } }" class="category-card" :class="`category-${index + 1}`">
            <img :src="categoryImages[index % categoryImages.length]" :alt="category.name" />
            <div class="category-shade"></div>
            <div class="category-content">
              <span class="category-index">0{{ index + 1 }}</span>
              <div><h3>{{ category.name }}</h3><p>{{ category.description }}</p></div>
              <span class="category-arrow"><el-icon><ArrowRight /></el-icon></span>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <section class="section featured-section">
      <div class="container">
        <div class="featured-head">
          <div class="section-heading left">
            <span class="eyebrow">MOST LOVED</span>
            <h2>本季人气之选</h2>
            <p>被反复点名的温柔味道，也是第一次认识兔南的好选择。</p>
          </div>
          <router-link to="/catalog" class="text-link">查看全部蛋糕 <el-icon><Right /></el-icon></router-link>
        </div>
        <div class="product-grid" v-loading="loading">
          <ProductCard v-for="product in featured" :key="product.id" :product="product" @order="openOrder" />
        </div>
      </div>
    </section>

    <section id="our-story" class="story-section">
      <div class="container story-grid">
        <div class="story-visual">
          <div class="story-image-main"><img src="/images/cake-berry.jpg" alt="法式蛋糕" loading="lazy" /></div>
          <div class="story-image-small"><img src="/images/cake-matcha.jpg" alt="甜品细节" loading="lazy" /></div>
          <div class="story-seal"><span>EST.</span><strong>2014</strong><em>SHANGHAI</em></div>
          <div class="story-note">“好的甜点，应该让人想起<br />某个被认真爱着的瞬间。”</div>
        </div>
        <div class="story-copy">
          <span class="eyebrow">OUR STORY</span>
          <h2 class="display-title">以甜为名，<br /><em>收藏每一束光。</em></h2>
          <p class="story-lead">兔南，是我们对‘认真做甜、温柔待人’的朴素愿望。我们想把生活中那些微小却明亮的时刻，用一只蛋糕认真收藏。</p>
          <p class="story-text">从 2014 年安福路的一间小小工作室开始，我们坚持使用动物奶油、当季鲜果与手工熬制的果酱。拒绝工业预拌粉，也拒绝千篇一律的甜。每一份配方，都经过数十次调整，只为在入口那一瞬，恰好温柔。</p>
          <div class="story-values">
            <div><span>01</span><strong>当季食材</strong><p>跟随四时变化，选择风味最好的原料</p></div>
            <div><span>02</span><strong>小批次手作</strong><p>每日限量，只为保证每一只蛋糕的状态</p></div>
            <div><span>03</span><strong>刚刚好的甜</strong><p>不掩盖食材本味，甜得有层次</p></div>
          </div>
          <router-link to="/catalog" class="btn btn-primary">认识我们的蛋糕 <el-icon><ArrowRight /></el-icon></router-link>
        </div>
      </div>
    </section>

    <section class="section testimonial-section">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">SWEET MOMENTS</span>
          <h2>被记住的甜，<span class="italic">都有故事</span></h2>
        </div>
        <div class="testimonial-grid">
          <div class="testimonial-card">
            <div class="quote-mark">“</div>
            <p>妈妈生日那天订了香槟玫瑰，打开盒子的瞬间她眼睛都亮了。奶油很轻，玫瑰香一点都不做作。</p>
            <div class="testimonial-person"><span class="person-avatar">Y</span><div><strong>余小姐</strong><span>香槟玫瑰 · 8寸</span></div><span class="stars">★★★★★</span></div>
          </div>
          <div class="testimonial-card featured-quote">
            <div class="quote-mark">“</div>
            <p>是我在上海吃过最舒服的草莓蛋糕。不是那种齁甜，草莓的酸和奶油的香刚刚好，连不爱吃甜的朋友都吃了两块。</p>
            <div class="testimonial-person"><span class="person-avatar">C</span><div><strong>陈先生</strong><span>云朵草莓蛋糕 · 6寸</span></div><span class="stars">★★★★★</span></div>
          </div>
          <div class="testimonial-card">
            <div class="quote-mark">“</div>
            <p>包装太美了，舍不得拆。每周三会员日都会订一只小蛋糕，已经变成我给自己的固定奖励。</p>
            <div class="testimonial-person"><span class="person-avatar">L</span><div><strong>林小姐</strong><span>柠檬轻芝士 · 4寸</span></div><span class="stars">★★★★★</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="closing-banner">
      <div class="closing-overlay"></div>
      <div class="container closing-inner">
        <span class="eyebrow">A LITTLE SWEETNESS</span>
        <h2>下一个值得纪念的日子，<br /><em>让兔南陪你一起。</em></h2>
        <p>提前 24 小时预订，我们会在约定好的那天，把新鲜与心意一起送达。</p>
        <router-link to="/catalog" class="btn btn-light">开始挑选 <el-icon><ArrowRight /></el-icon></router-link>
      </div>
    </section>

    <ProductOrderDialog ref="orderDialogRef" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import ProductCard from '../components/ProductCard.vue'
import ProductOrderDialog from '../components/ProductOrderDialog.vue'
import HeroMediaCarousel from '../components/HeroMediaCarousel.vue'
import request from '../utils/request'
import { authState } from '../utils/auth'

const router = useRouter()
const loading = ref(true)
const categories = ref([])
const featured = ref([])
const notices = ref([])
const orderDialogRef = ref(null)

const categoryImages = [
  '/images/cake-strawberry.jpg',
  '/images/cake-berry.jpg',
  '/images/cake-chocolate.jpg',
  '/images/cake-vanilla.jpg',
  '/images/cake-celebration.jpg',
  '/images/cake-cupcake.jpg'
]

const loadData = async () => {
  loading.value = true
  try {
    const [categoryRes, goodsRes, noticeRes] = await Promise.all([
      request.get('/category/selectAll'),
      request.get('/goods/selectPage', { params: { featured: true, pageSize: 6 } }),
      request.get('/notice/selectAll')
    ])
    categories.value = categoryRes.data || []
    featured.value = goodsRes.data?.list || []
    notices.value = noticeRes.data || []
  } finally {
    loading.value = false
  }
}

const openOrder = (product) => {
  if (!authState.user) {
    ElMessage.info('登录后即可预订蛋糕')
    router.push({ name: 'login', query: { redirect: '/catalog' } })
    return
  }
  if (authState.user.role === '管理员') {
    ElMessage.info('管理员账号请前往后台管理')
    return
  }
  orderDialogRef.value?.open(product)
}

onMounted(loadData)
</script>

<style scoped>
.hero { position: relative; min-height: 740px; display: flex; align-items: center; margin-top: -84px; padding: 125px 0 85px; background: radial-gradient(circle at 78% 36%, #f0dfd0 0, transparent 34%), linear-gradient(135deg, #faf6ee 0%, #f7eee2 58%, #f4eade 100%); overflow: hidden; }
.hero::after { content: ''; position: absolute; width: 100%; height: 45%; bottom: 0; left: 0; background: linear-gradient(transparent, rgba(255,250,244,.35)); pointer-events: none; }
.hero-inner { display: grid; grid-template-columns: 1fr .95fr; gap: 70px; align-items: center; position: relative; z-index: 2; }
.hero-orbit { position: absolute; border: 1px solid rgba(147,90,96,.13); border-radius: 50%; }
.orbit-one { width: 610px; height: 610px; right: -70px; top: -35px; }
.orbit-two { width: 760px; height: 760px; right: -145px; top: -110px; border-style: dashed; opacity: .6; }
.hero-copy { padding-top: 24px; }
.hero-eyebrow { display: flex; align-items: center; gap: 12px; color: var(--rose-deep); font-size: 9px; font-weight: 700; letter-spacing: .24em; }
.hero-eyebrow span { display: block; width: 36px; height: 1px; background: var(--rose); }
.hero h1 { font-family: var(--font-display); font-size: clamp(43px, 4.8vw, 69px); line-height: 1.02; letter-spacing: -.025em; font-weight: 500; margin: 30px 0 27px; }
.hero h1 em { display: inline-block; color: var(--rose-deep); font-family: "STKaiti", "华文楷体", "KaiTi", "楷体", "Songti SC", serif; font-size: 1em; font-style: normal; font-weight: 400; line-height: 1.12; letter-spacing: .07em; margin-top: .04em; white-space: nowrap; }
.hero-desc { color: var(--ink-soft); font-size: 14px; line-height: 2; letter-spacing: .05em; margin: 0; }
.hero-actions { display: flex; gap: 13px; margin-top: 37px; }
.hero-numbers { display: flex; gap: 38px; margin-top: 47px; padding-top: 28px; border-top: 1px solid rgba(67,47,41,.14); max-width: 430px; }
.hero-numbers div { display: flex; flex-direction: column; gap: 6px; }
.hero-numbers strong { font-family: var(--font-display); font-size: 30px; font-weight: 500; line-height: 1; }
.hero-numbers small { font-size: 14px; color: var(--rose-deep); margin-left: 2px; }
.hero-numbers span { color: var(--ink-muted); font-size: 9px; letter-spacing: .12em; }
.hero-visual { position: relative; height: 650px; display: flex; align-items: center; justify-content: center; }
.float-card { position: absolute; z-index: 3; background: rgba(255,250,244,.92); backdrop-filter: blur(14px); border: 1px solid rgba(255,255,255,.65); box-shadow: 0 18px 45px rgba(57,35,27,.14); border-radius: 16px; padding: 14px 17px; display: flex; align-items: center; gap: 11px; animation: floatY 5s ease-in-out infinite; }
.float-card strong { display: block; font-size: 10px; margin-bottom: 3px; }
.float-card span { color: var(--ink-muted); font-size: 8px; letter-spacing: .04em; }
.fresh-card { left: -6px; top: 120px; }
.rating-card { right: -22px; bottom: 85px; animation-delay: 1.3s; }
.fresh-icon { width: 34px; height: 34px; border-radius: 50%; background: var(--sage-pale); color: var(--sage); display: grid; place-items: center; font-size: 17px; }
.rating-stars { color: var(--gold); font-size: 10px; letter-spacing: 2px; }
.rating-card .rating-stars { display: block; margin-bottom: 3px; }
.rating-card div { order: -1; }
.rating-card { flex-wrap: wrap; width: 172px; }
.rating-card span:last-child { display: block; }
.hero-side-note { position: absolute; right: -94px; top: 50%; transform: rotate(90deg); font-size: 8px; letter-spacing: .35em; color: var(--ink-muted); }
.service-strip { position: relative; z-index: 5; margin-top: -36px; }
.service-grid { background: rgba(255,250,244,.94); border: 1px solid var(--line); border-radius: 20px; box-shadow: 0 18px 50px rgba(65,43,35,.08); display: grid; grid-template-columns: repeat(3,1fr); padding: 24px 16px; backdrop-filter: blur(12px); }
.service-item { display: flex; align-items: center; gap: 15px; padding: 4px 30px; border-right: 1px solid var(--line); }
.service-item:last-child { border-right: 0; }
.service-item > .el-icon { font-size: 25px; color: var(--gold); }
.service-item strong { display: block; font-size: 11px; margin-bottom: 5px; letter-spacing: .04em; }
.service-item span { display: block; color: var(--ink-muted); font-size: 9px; line-height: 1.5; }
.notice-ribbon { margin-top: 35px; }
.notice-inner { border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); min-height: 51px; display: flex; align-items: center; gap: 22px; }
.notice-label { display: flex; gap: 6px; align-items: center; color: var(--rose-deep); font-size: 10px; letter-spacing: .1em; white-space: nowrap; }
.notice-track { flex: 1; min-width: 0; display: flex; gap: 12px; align-items: center; white-space: nowrap; overflow: hidden; }
.notice-track span { font-family: var(--font-display); font-size: 16px; font-weight: 600; }
.notice-track em { color: var(--ink-soft); font-size: 10px; font-style: normal; overflow: hidden; text-overflow: ellipsis; }
.notice-date { color: var(--ink-muted); font-size: 8px; letter-spacing: .08em; white-space: nowrap; }
.category-section { padding-top: 110px; }
.category-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.category-card { position: relative; height: 245px; border-radius: 20px; overflow: hidden; text-decoration: none; color: white; }
.category-card:nth-child(4) { grid-column: span 1; }
.category-card img { width: 100%; height: 100%; object-fit: cover; transition: transform .8s cubic-bezier(.2,.7,.2,1); }
.category-card:hover img { transform: scale(1.07); }
.category-shade { position: absolute; inset: 0; background: linear-gradient(to top, rgba(36,23,20,.76), rgba(36,23,20,.02) 75%); }
.category-content { position: absolute; inset: 0; padding: 22px 24px; display: flex; flex-direction: column; justify-content: space-between; }
.category-index { font-size: 8px; letter-spacing: .2em; opacity: .7; align-self: flex-end; }
.category-content h3 { font-family: var(--font-display); font-size: 30px; font-weight: 500; margin: 0 0 5px; }
.category-content p { margin: 0; font-size: 9px; opacity: .7; letter-spacing: .04em; }
.category-arrow { position: absolute; right: 22px; bottom: 23px; width: 35px; height: 35px; display: grid; place-items: center; border-radius: 50%; background: rgba(255,255,255,.16); backdrop-filter: blur(8px); transition: .3s; }
.category-card:hover .category-arrow { background: white; color: var(--ink); }
.featured-section { background: var(--paper-deep); }
.featured-head { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 38px; }
.featured-head .section-heading { margin-bottom: 0; }
.featured-head .section-heading p { max-width: 470px; }
.featured-head .text-link { margin-bottom: 8px; }
.product-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.story-section { padding: 125px 0; background: var(--paper); }
.story-grid { display: grid; grid-template-columns: 1.03fr .97fr; gap: 100px; align-items: center; }
.story-visual { position: relative; height: 620px; }
.story-image-main { width: 73%; height: 88%; border-radius: 240px 240px 24px 24px; overflow: hidden; }
.story-image-main img { width: 100%; height: 100%; object-fit: cover; }
.story-image-small { position: absolute; right: 0; bottom: 0; width: 43%; height: 47%; border-radius: 140px 140px 20px 20px; overflow: hidden; border: 10px solid var(--paper); box-shadow: var(--shadow-md); }
.story-image-small img { width: 100%; height: 100%; object-fit: cover; }
.story-seal { position: absolute; top: 30px; right: 20px; width: 112px; height: 112px; border-radius: 50%; border: 1px solid rgba(163,100,109,.35); display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--rose-deep); transform: rotate(8deg); background: rgba(255,250,244,.72); backdrop-filter: blur(6px); }
.story-seal span, .story-seal em { font-size: 7px; letter-spacing: .2em; font-style: normal; }
.story-seal strong { font-family: var(--font-display); font-size: 30px; font-weight: 500; line-height: 1.05; }
.story-note { position: absolute; left: -22px; bottom: 65px; background: var(--ink); color: #f3e7d6; padding: 22px 25px; font-family: var(--font-display); font-size: 16px; line-height: 1.7; letter-spacing: .05em; border-radius: 4px 20px 20px 20px; box-shadow: var(--shadow-md); }
.story-copy .display-title { margin-top: 16px; margin-bottom: 24px; }
.story-copy .display-title em { color: var(--rose-deep); }
.story-lead { font-family: var(--font-display); font-size: 20px; line-height: 1.9; color: var(--ink); margin: 0 0 17px; }
.story-text { color: var(--ink-soft); font-size: 12px; line-height: 2.05; margin: 0; }
.story-values { border-top: 1px solid var(--line); margin: 33px 0 35px; }
.story-values > div { position: relative; padding: 16px 0 16px 48px; border-bottom: 1px solid var(--line); }
.story-values span { position: absolute; left: 0; top: 18px; color: var(--rose); font-family: var(--font-display); font-size: 16px; }
.story-values strong { display: block; font-size: 11px; margin-bottom: 5px; }
.story-values p { margin: 0; color: var(--ink-muted); font-size: 9px; }
.testimonial-section { background: var(--cream); }
.testimonial-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 18px; }
.testimonial-card { background: rgba(255,250,244,.72); border: 1px solid var(--line); border-radius: 22px; padding: 32px 28px 25px; position: relative; display: flex; flex-direction: column; }
.testimonial-card.featured-quote { background: var(--ink); color: #f7ece0; transform: translateY(-14px); box-shadow: var(--shadow-md); }
.quote-mark { font-family: var(--font-display); font-size: 62px; line-height: .6; color: var(--rose); height: 33px; }
.featured-quote .quote-mark { color: var(--gold-light); }
.testimonial-card > p { font-family: var(--font-display); font-size: 17px; line-height: 1.8; flex: 1; margin: 12px 0 25px; }
.featured-quote > p { color: #f4e5d5; }
.testimonial-person { display: flex; align-items: center; gap: 10px; padding-top: 18px; border-top: 1px solid var(--line); }
.featured-quote .testimonial-person { border-color: rgba(255,255,255,.13); }
.person-avatar { width: 32px; height: 32px; border-radius: 50%; background: var(--rose-pale); color: var(--rose-deep); display: grid; place-items: center; font-family: var(--font-display); font-size: 15px; }
.testimonial-person strong { display: block; font-size: 10px; margin-bottom: 3px; }
.testimonial-person div span { color: var(--ink-muted); font-size: 8px; }
.featured-quote .testimonial-person div span { color: rgba(255,255,255,.45); }
.stars { margin-left: auto; color: var(--gold); font-size: 8px; letter-spacing: 1px; }
.closing-banner { min-height: 500px; position: relative; display: flex; align-items: center; text-align: center; background-image: url('/images/cake-celebration.jpg'); background-size: cover; background-position: center 45%; }
.closing-overlay { position: absolute; inset: 0; background: linear-gradient(rgba(38,24,20,.66), rgba(38,24,20,.72)); }
.closing-inner { position: relative; z-index: 2; color: white; display: flex; flex-direction: column; align-items: center; }
.closing-inner .eyebrow { color: var(--gold-light); }
.closing-inner h2 { font-family: var(--font-display); font-size: clamp(43px,5.4vw,70px); font-weight: 400; line-height: 1.08; margin: 19px 0 20px; }
.closing-inner h2 em { color: var(--gold-light); }
.closing-inner p { color: rgba(255,255,255,.7); font-size: 12px; letter-spacing: .06em; margin: 0 0 30px; }
.closing-inner .btn { min-height: 50px; padding: 0 32px; }
@media (max-width: 1050px) {
  .hero-inner { gap: 30px; }
  .hero-visual { height: 630px; }
  .hero-side-note { display: none; }
  .story-grid { gap: 55px; }
  .story-visual { height: 540px; }
}
@media (max-width: 800px) {
  .hero { min-height: auto; margin-top: -70px; padding: 125px 0 90px; }
  .hero-inner { grid-template-columns: 1fr; }
  .hero-copy { text-align: center; }
  .hero-eyebrow { justify-content: center; }
  .hero h1 { font-size: 46px; }
  .hero-desc br { display: none; }
  .hero-actions, .hero-numbers { justify-content: center; }
  .hero-visual { height: 590px; margin-top: 10px; }
  .fresh-card { left: 2px; top: 75px; }
  .rating-card { right: 0; bottom: 30px; }
  .service-grid { grid-template-columns: 1fr; padding: 10px 20px; }
  .service-item { border-right: 0; border-bottom: 1px solid var(--line); padding: 15px 2px; }
  .service-item:last-child { border-bottom: 0; }
  .notice-date { display: none; }
  .category-grid { grid-template-columns: repeat(2,1fr); }
  .product-grid { grid-template-columns: repeat(2,1fr); }
  .featured-head { flex-direction: column; align-items: flex-start; gap: 18px; }
  .story-grid { grid-template-columns: 1fr; }
  .story-visual { height: 520px; max-width: 520px; }
  .testimonial-grid { grid-template-columns: 1fr; max-width: 560px; margin: 0 auto; }
  .testimonial-card.featured-quote { transform: none; }
}
@media (max-width: 560px) {
  .hero h1 { font-size: 40px; }
  .hero-actions { flex-direction: column; align-items: stretch; }
  .hero-numbers { gap: 20px; justify-content: space-between; }
  .hero-visual { height: 510px; }
  .fresh-card { top: 30px; left: -4px; padding: 10px 12px; }
  .rating-card { bottom: -5px; right: -3px; }
  .category-grid, .product-grid { grid-template-columns: 1fr; }
  .category-card { height: 210px; }
  .story-visual { height: 420px; }
  .story-note { left: -5px; bottom: 20px; font-size: 13px; padding: 16px; }
  .story-seal { right: 2px; width: 90px; height: 90px; }
  .closing-banner { min-height: 420px; }
}
</style>
