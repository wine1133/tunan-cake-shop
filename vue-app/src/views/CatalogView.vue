<template>
  <div class="catalog-page">
    <section class="page-banner catalog-banner">
      <div class="container banner-grid">
        <div>
          <span class="eyebrow">THE CAKE COLLECTION</span>
          <h1>把喜欢的甜，<br /><em>带回家。</em></h1>
          <p>每一只都在接单后新鲜制作。挑一份合心意的味道，为今天加一点柔软。</p>
        </div>
        <div class="banner-note">
          <span>今日可预订</span>
          <strong>{{ total || 10 }}</strong>
          <p>款手作蛋糕</p>
          <div class="note-line"></div>
          <small>每日限量 · 售完即止</small>
        </div>
      </div>
    </section>

    <section class="catalog-content container">
      <div class="catalog-toolbar">
        <div class="category-tabs">
          <button :class="{ active: categoryId === 0 }" @click="selectCategory(0)">全部</button>
          <button v-for="category in categories" :key="category.id" :class="{ active: categoryId === category.id }" @click="selectCategory(category.id)">{{ category.name }}</button>
        </div>
        <div class="catalog-search">
          <el-icon><Search /></el-icon>
          <input v-model="search" placeholder="搜索蛋糕名称" @keyup.enter="applySearch" />
          <button v-if="search" @click="resetSearch"><el-icon><Close /></el-icon></button>
        </div>
      </div>

      <div class="catalog-meta">
        <span><em>{{ total }}</em> 款蛋糕</span>
        <div class="sort-tabs">
          <button :class="{ active: sort === 'default' }" @click="sort = 'default'">默认排序</button>
          <button :class="{ active: sort === 'sales' }" @click="sort = 'sales'">人气优先</button>
          <button :class="{ active: sort === 'price' }" @click="sort = 'price'">价格从低到高</button>
        </div>
      </div>

      <div v-if="displayProducts.length" class="catalog-grid">
        <ProductCard v-for="product in displayProducts" :key="product.id" :product="product" @order="openOrder" />
      </div>
      <div v-else-if="!loading" class="catalog-empty">
        <div class="empty-icon"><el-icon><Dish /></el-icon></div>
        <h3>暂时没有找到这份甜</h3>
        <p>换一个关键词，或者看看其他分类吧。</p>
        <button class="btn btn-outline btn-small" @click="resetAll">查看全部蛋糕</button>
      </div>
      <div v-else class="catalog-grid">
        <div v-for="n in 8" :key="n" class="skeleton-card"><div></div><span></span><span></span></div>
      </div>

      <div class="catalog-pagination" v-if="total > pageSize">
        <el-pagination background layout="prev, pager, next" :page-size="pageSize" :current-page="pageNum" :total="total" @current-change="changePage" />
      </div>
    </section>

    <ProductOrderDialog ref="orderDialogRef" @ordered="loadProducts" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import ProductCard from '../components/ProductCard.vue'
import ProductOrderDialog from '../components/ProductOrderDialog.vue'
import request from '../utils/request'
import { authState } from '../utils/auth'

const route = useRoute()
const router = useRouter()
const categories = ref([])
const products = ref([])
const search = ref('')
const appliedSearch = ref('')
const categoryId = ref(Number(route.query.category) || 0)
const sort = ref('default')
const pageNum = ref(1)
const pageSize = ref(9)
const total = ref(0)
const loading = ref(true)
const orderDialogRef = ref(null)

const displayProducts = computed(() => {
  const list = [...products.value]
  if (sort.value === 'sales') list.sort((a, b) => (b.sales || 0) - (a.sales || 0))
  if (sort.value === 'price') list.sort((a, b) => (a.price || 0) - (b.price || 0))
  return list
})

const loadProducts = async () => {
  loading.value = true
  try {
    const res = await request.get('/goods/selectPage', {
      params: { pageNum: pageNum.value, pageSize: pageSize.value, name: appliedSearch.value, categoryId: categoryId.value }
    })
    products.value = res.data?.list || []
    total.value = res.data?.total || 0
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  const res = await request.get('/category/selectAll')
  categories.value = res.data || []
}

const selectCategory = (id) => {
  categoryId.value = id
  pageNum.value = 1
  router.replace({ query: id ? { category: id } : {} })
  loadProducts()
}

const applySearch = () => {
  appliedSearch.value = search.value.trim()
  pageNum.value = 1
  loadProducts()
}

const resetSearch = () => {
  search.value = ''
  appliedSearch.value = ''
  pageNum.value = 1
  loadProducts()
}

const resetAll = () => {
  search.value = ''
  appliedSearch.value = ''
  categoryId.value = 0
  pageNum.value = 1
  router.replace({ query: {} })
  loadProducts()
}

const changePage = (page) => {
  pageNum.value = page
  loadProducts()
  window.scrollTo({ top: 400, behavior: 'smooth' })
}

const openOrder = (product) => {
  if (!authState.user) {
    ElMessage.info('登录后即可预订蛋糕')
    router.push({ name: 'login', query: { redirect: route.fullPath } })
    return
  }
  if (authState.user.role === '管理员') {
    ElMessage.info('管理员账号请前往后台管理')
    return
  }
  orderDialogRef.value?.open(product)
}

watch(() => route.query.category, (value) => {
  categoryId.value = Number(value) || 0
  pageNum.value = 1
  loadProducts()
})

onMounted(() => {
  loadCategories()
  loadProducts()
})
</script>

<style scoped>
.page-banner { background: linear-gradient(135deg, #f3e9dc, #f7f0e7 66%, #f0e2d4); }
.banner-grid { display: flex; justify-content: space-between; align-items: flex-end; }
.page-banner h1 { font-size: clamp(50px, 6vw, 80px); margin-bottom: 22px; }
.page-banner h1 em { color: var(--rose-deep); }
.banner-note { width: 180px; padding: 24px; border-radius: 18px; border: 1px solid rgba(140,84,93,.18); background: rgba(255,250,244,.46); backdrop-filter: blur(10px); margin-bottom: 5px; }
.banner-note > span { display: block; color: var(--ink-muted); font-size: 9px; letter-spacing: .14em; }
.banner-note strong { display: inline-block; font-family: var(--font-display); font-size: 58px; font-weight: 500; line-height: 1; margin-top: 9px; }
.banner-note p { display: inline; color: var(--ink-soft); font-size: 10px; margin-left: 5px; }
.note-line { height: 1px; background: var(--line); margin: 13px 0; }
.banner-note small { font-size: 8px; color: var(--ink-muted); letter-spacing: .07em; }
.catalog-content { padding-top: 52px; padding-bottom: 110px; }
.catalog-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 24px; padding-bottom: 22px; border-bottom: 1px solid var(--line); }
.category-tabs { display: flex; flex-wrap: wrap; gap: 4px; }
.category-tabs button, .sort-tabs button { background: none; border: 0; cursor: pointer; color: var(--ink-soft); font-size: 11px; letter-spacing: .04em; padding: 9px 13px; border-radius: 999px; transition: .2s; }
.category-tabs button:hover, .sort-tabs button:hover { color: var(--ink); }
.category-tabs button.active { background: var(--ink); color: white; }
.catalog-search { min-width: 260px; display: flex; align-items: center; gap: 9px; border: 1px solid var(--line); background: rgba(255,250,244,.7); border-radius: 999px; padding: 10px 15px; }
.catalog-search > .el-icon { color: var(--ink-muted); }
.catalog-search input { border: 0; outline: 0; background: transparent; flex: 1; font-size: 11px; color: var(--ink); min-width: 0; }
.catalog-search button { border: 0; background: none; padding: 0; color: var(--ink-muted); cursor: pointer; }
.catalog-meta { display: flex; justify-content: space-between; align-items: center; margin: 23px 0 26px; }
.catalog-meta > span { color: var(--ink-muted); font-size: 10px; letter-spacing: .08em; }
.catalog-meta em { color: var(--ink); font-family: var(--font-display); font-size: 16px; font-style: normal; }
.sort-tabs { display: flex; gap: 2px; }
.sort-tabs button.active { color: var(--rose-deep); font-weight: 600; }
.catalog-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.skeleton-card { border-radius: 22px; background: rgba(255,250,244,.68); padding-bottom: 22px; overflow: hidden; }
.skeleton-card div { height: 340px; background: linear-gradient(90deg, #ede3d8, #f7f0e8, #ede3d8); background-size: 200% 100%; animation: shimmer 1.4s infinite linear; }
.skeleton-card span { display: block; height: 13px; margin: 20px 22px 0; border-radius: 8px; background: #eee4d9; }
.skeleton-card span:last-child { width: 55%; margin-top: 12px; }
@keyframes shimmer { to { background-position: -200% 0; } }
.catalog-empty { text-align: center; padding: 90px 20px 100px; }
.empty-icon { width: 76px; height: 76px; border-radius: 50%; background: var(--paper-deep); display: grid; place-items: center; margin: 0 auto 20px; color: var(--rose); font-size: 30px; }
.catalog-empty h3 { font-family: var(--font-display); font-size: 30px; font-weight: 500; margin: 0 0 8px; }
.catalog-empty p { color: var(--ink-muted); font-size: 11px; margin: 0 0 23px; }
.catalog-pagination { display: flex; justify-content: center; margin-top: 45px; }
@media (max-width: 900px) {
  .banner-note { display: none; }
  .catalog-toolbar { align-items: flex-start; flex-direction: column; }
  .catalog-search { width: 100%; }
  .catalog-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
  .category-tabs { flex-wrap: nowrap; overflow-x: auto; width: 100%; padding-bottom: 5px; }
  .category-tabs button { white-space: nowrap; }
  .catalog-meta { align-items: flex-start; gap: 15px; flex-direction: column; }
  .sort-tabs { flex-wrap: wrap; }
  .catalog-grid { grid-template-columns: 1fr; }
}
</style>