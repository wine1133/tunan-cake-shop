<template>
  <div class="hero-media-carousel">
    <div class="carousel-stage">
      <div class="carousel-slides">
        <div v-for="(slide, index) in slides" :key="slide.key" class="carousel-slide" :class="{ active: index === active }" :aria-hidden="index !== active">
          <video
            v-if="slide.type === 'video'"
            :ref="setVideoElement"
            :poster="slide.poster"
            :muted="muted"
            autoplay
            playsinline
            preload="auto"
            disablepictureinpicture
            @loadeddata="playActiveVideo"
            @canplay="playActiveVideo"
            @ended="next"
          >
            <source :src="slide.src" type="video/mp4" />
          </video>
          <img v-else :src="slide.src" :alt="slide.title" loading="lazy" />
          <div class="slide-shade"></div>
          <div class="film-grain"></div>
          <div class="slide-caption">
            <span>{{ slide.kicker }}</span>
            <strong>{{ slide.title }}</strong>
          </div>
        </div>
      </div>

      <div class="film-badge"><i></i> FILM</div>
      <button v-if="active === 0" class="sound-toggle" :class="{ muted }" :aria-pressed="!muted" @click="toggleSound">
        <svg v-if="muted" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4Zm12.6 1.1a3.5 3.5 0 0 1 0 3.8M19.4 7a7 7 0 0 1 0 10" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/><path d="m4 4 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
        <svg v-else viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4Z" fill="currentColor"/><path d="M16.6 8.4a5 5 0 0 1 0 7.2M19.4 5.6a9 9 0 0 1 0 12.8" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
        <span>{{ muted ? '开启声音' : '关闭声音' }}</span>
      </button>
      <button class="carousel-arrow arrow-prev" aria-label="上一张" @click="prev"><el-icon><ArrowLeft /></el-icon></button>
      <button class="carousel-arrow arrow-next" aria-label="下一张" @click="next"><el-icon><ArrowRight /></el-icon></button>
    </div>
    <div class="carousel-footer">
      <div class="carousel-dots">
        <button v-for="(slide, index) in slides" :key="slide.key" :class="{ active: index === active }" :aria-label="`查看第 ${index + 1} 张`" @click="goTo(index)"></button>
      </div>
      <span class="carousel-count">0{{ active + 1 }} <em>/</em> 0{{ slides.length }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'

const slides = [
  { key: 'film', type: 'video', src: '/media/tunan-cake-film-web.mp4', poster: '/media/tunan-cake-poster.jpg', kicker: 'TU NAN FILM', title: '兔南映像 · 手作日常' },
  { key: 'scene-1', type: 'image', src: '/media/tunan-cake-scene-1.jpg', kicker: 'FRESHLY MADE', title: '每一口，都是当天的新鲜' },
  { key: 'scene-2', type: 'image', src: '/media/tunan-cake-scene-2.jpg', kicker: 'SEASONAL MOMENT', title: '把秋天，藏进一块蛋糕里' },
  { key: 'scene-3', type: 'image', src: '/media/tunan-cake-scene-3.jpg', kicker: 'WITH LOVE', title: '认真做甜，也认真生活' }
]
const durations = [39000, 6000, 6000, 6000]
const active = ref(0)
const videoEl = ref(null)
const muted = ref(false)
let timer = null

const clearTimer = () => {
  if (timer) window.clearTimeout(timer)
  timer = null
}
const schedule = () => {
  clearTimer()
  timer = window.setTimeout(next, durations[active.value] || 6000)
}
const setVideoElement = (element) => {
  if (element) videoEl.value = element
}
const getVideoElement = () => {
  if (videoEl.value?.tagName === 'VIDEO') return videoEl.value
  return document.querySelector('.hero-media-carousel video')
}
const playActiveVideo = async () => {
  const video = getVideoElement()
  if (!video || active.value !== 0) return
  video.muted = muted.value
  video.volume = 0.82
  try {
    await video.play()
  } catch (error) {
    if (!muted.value) {
      muted.value = true
      video.muted = true
      try { await video.play() } catch (fallbackError) {}
    }
  }
}
const toggleSound = async () => {
  const video = getVideoElement()
  muted.value = !muted.value
  if (!video) return
  video.muted = muted.value
  video.volume = 0.82
  if (!muted.value) {
    try { await video.play() } catch (error) {}
  }
}
const syncMedia = () => {
  nextTick(() => {
    if (active.value === 0) {
      const video = getVideoElement()
      if (video) video.currentTime = 0
      playActiveVideo()
    } else {
      getVideoElement()?.pause()
    }
  })
  schedule()
}
const next = () => {
  active.value = (active.value + 1) % slides.length
}
const prev = () => {
  active.value = (active.value - 1 + slides.length) % slides.length
}
const goTo = (index) => { active.value = index }

watch(active, syncMedia)
onMounted(() => {
  syncMedia()
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) clearTimer()
})
onBeforeUnmount(clearTimer)
</script>

<style scoped>
.hero-media-carousel { width: clamp(400px, 34vw, 490px); position: relative; }
.carousel-stage { position: relative; width: 100%; aspect-ratio: 4 / 5; border-radius: 145px 145px 24px 24px; overflow: hidden; box-shadow: 0 35px 80px rgba(58,35,28,.2); background: #3b2923; }
.carousel-slides, .carousel-slide { position: absolute; inset: 0; }
.carousel-slide { opacity: 0; visibility: hidden; transform: scale(1.035); transition: opacity .9s ease, transform 1s cubic-bezier(.2,.7,.2,1); }
.carousel-slide.active { opacity: 1; visibility: visible; transform: scale(1); z-index: 1; }
.carousel-slide video, .carousel-slide img { width: 100%; height: 100%; object-fit: cover; display: block; }
.carousel-slide video { background: #2c1d19; }
.slide-shade { position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(35,22,18,.04) 38%, rgba(35,22,18,.12) 55%, rgba(35,22,18,.78) 100%); }
.film-grain { position: absolute; inset: 0; opacity: .09; pointer-events: none; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.95' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }
.slide-caption { position: absolute; left: 24px; right: 24px; bottom: 27px; color: #fff8ef; z-index: 2; }
.slide-caption span { display: block; font-size: 7px; font-weight: 600; letter-spacing: .24em; color: rgba(255,248,239,.64); margin-bottom: 8px; }
.slide-caption strong { display: block; font-family: var(--font-display); font-size: 23px; line-height: 1.35; font-weight: 400; letter-spacing: .04em; text-shadow: 0 2px 12px rgba(30,17,14,.28); }
.film-badge { position: absolute; z-index: 3; left: 22px; top: 28px; display: flex; align-items: center; gap: 7px; padding: 7px 10px; border-radius: 999px; color: rgba(255,250,244,.8); background: rgba(42,27,23,.28); border: 1px solid rgba(255,255,255,.14); backdrop-filter: blur(9px); font-size: 7px; letter-spacing: .14em; }
.film-badge i { display: block; width: 5px; height: 5px; border-radius: 50%; background: #e5bd7a; box-shadow: 0 0 0 3px rgba(229,189,122,.15); }
.sound-toggle { position: absolute; z-index: 4; right: 20px; top: 24px; height: 32px; padding: 0 11px 0 9px; border-radius: 999px; border: 1px solid rgba(255,255,255,.18); background: rgba(42,27,23,.34); color: rgba(255,250,244,.88); display: flex; align-items: center; gap: 6px; backdrop-filter: blur(10px); cursor: pointer; font-size: 8px; letter-spacing: .05em; transition: .25s; }
.sound-toggle svg { width: 15px; height: 15px; }
.sound-toggle:hover { background: rgba(42,27,23,.58); }
.sound-toggle.muted { color: #fff4df; border-color: rgba(229,189,122,.5); box-shadow: 0 0 0 4px rgba(229,189,122,.08); }
.carousel-arrow { position: absolute; z-index: 4; top: 50%; transform: translateY(-50%); width: 34px; height: 34px; border: 1px solid rgba(255,255,255,.25); border-radius: 50%; background: rgba(255,250,244,.83); color: var(--ink); display: grid; place-items: center; cursor: pointer; backdrop-filter: blur(9px); transition: .25s; opacity: 0; }
.carousel-stage:hover .carousel-arrow { opacity: 1; }
.carousel-arrow:hover { background: white; transform: translateY(-50%) scale(1.06); }
.arrow-prev { left: 14px; }
.arrow-next { right: 14px; }
.carousel-footer { width: 100%; margin-top: 16px; padding: 0 5px; display: flex; align-items: center; justify-content: space-between; }
.carousel-dots { display: flex; align-items: center; gap: 6px; }
.carousel-dots button { width: 5px; height: 5px; padding: 0; border: 0; border-radius: 99px; background: rgba(67,47,41,.22); cursor: pointer; transition: .35s; }
.carousel-dots button.active { width: 28px; background: var(--rose-deep); }
.carousel-count { color: var(--ink-muted); font-family: var(--font-display); font-size: 12px; letter-spacing: .06em; }
.carousel-count em { color: var(--rose); font-style: normal; margin: 0 2px; }
@media (max-width: 1050px) {
  .hero-media-carousel { width: clamp(360px, 42vw, 430px); }
}
@media (max-width: 800px) {
  .hero-media-carousel { width: 370px; }
  .slide-caption { left: 20px; right: 20px; bottom: 23px; }
  .slide-caption strong { font-size: 21px; }
  .carousel-arrow { opacity: 1; width: 31px; height: 31px; }
}
@media (max-width: 560px) {
  .hero-media-carousel { width: min(315px, 86vw); }
  .slide-caption strong { font-size: 19px; }
  .carousel-footer { margin-top: 12px; }
}
@media (prefers-reduced-motion: reduce) {
  .carousel-slide { transition: none; }
  .carousel-dots button { transition: none; }
}
</style>