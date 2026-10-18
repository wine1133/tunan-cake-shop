<template>
  <div class="dashboard-page">
    <div class="dashboard-heading">
      <div>
        <span class="eyebrow">OVERVIEW</span>
        <h1>早安，{{ authState.user?.name }}。</h1>
        <p>今天也一起，认真对待每一份甜蜜。</p>
      </div>
      <div class="heading-actions">
        <button class="btn btn-outline btn-small" @click="load"><el-icon><Refresh /></el-icon> 刷新数据</button>
        <router-link to="/admin/goods" class="btn btn-primary btn-small"><el-icon><Plus /></el-icon> 上架蛋糕</router-link>
      </div>
    </div>

    <div class="kpi-grid" v-loading="loading">
      <div class="kpi-card card-rose">
        <div class="kpi-icon"><el-icon><Money /></el-icon></div>
        <div class="kpi-copy"><span>累计营业额</span><strong><small>¥</small>{{ money(stats.kpi.revenue) }}</strong><em><el-icon><TopRight /></el-icon> 有效订单收入</em></div>
        <div class="kpi-decoration">SALES</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon sage"><el-icon><Tickets /></el-icon></div>
        <div class="kpi-copy"><span>预订订单</span><strong>{{ stats.kpi.orders }}<small> 单</small></strong><em><el-icon><Clock /></el-icon> {{ stats.kpi.pending }} 单进行中</em></div>
        <div class="kpi-decoration">ORDERS</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon gold"><el-icon><User /></el-icon></div>
        <div class="kpi-copy"><span>兔南会员</span><strong>{{ stats.kpi.users }}<small> 人</small></strong><em><el-icon><Plus /></el-icon> 本月新增 {{ stats.kpi.newUsers }} 位</em></div>
        <div class="kpi-decoration">MEMBERS</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon ink"><el-icon><Dish /></el-icon></div>
        <div class="kpi-copy"><span>在售蛋糕</span><strong>{{ stats.kpi.goods }}<small> 款</small></strong><em><el-icon><Box /></el-icon> 客单价 ¥{{ money(stats.kpi.avgOrder) }}</em></div>
        <div class="kpi-decoration">CAKES</div>
      </div>
    </div>

    <div class="dashboard-row main-row">
      <section class="admin-card chart-card">
        <div class="chart-head">
          <div><span class="eyebrow">WEEKLY SALES</span><h3>近 7 日营业额</h3></div>
          <span class="chart-total">¥{{ money(weekTotal) }}</span>
        </div>
        <div class="bar-chart">
          <div class="grid-lines"><i></i><i></i><i></i><i></i></div>
          <div class="bar-column" v-for="(item, index) in stats.week" :key="item.date">
            <div class="bar-value">{{ item.value ? `¥${money(item.value)}` : '' }}</div>
            <div class="bar-track"><div class="bar-fill" :class="{ today: index === stats.week.length - 1 }" :style="{ height: barHeight(item.value) }"></div></div>
            <span>{{ item.date }}</span>
          </div>
        </div>
      </section>

      <section class="admin-card category-chart">
        <div class="chart-head">
          <div><span class="eyebrow">CATEGORY MIX</span><h3>品类销售占比</h3></div>
        </div>
        <div class="donut-wrap">
          <div class="donut" :style="{ background: donutBackground }"><div><strong>{{ stats.categoryDistribution.length }}</strong><span>品类</span></div></div>
          <div class="category-legend">
            <div v-for="(item, index) in stats.categoryDistribution.slice(0, 5)" :key="item.id">
              <i :style="{ background: chartColors[index] }"></i>
              <span>{{ item.name }}</span>
              <strong>{{ item.percent }}%</strong>
            </div>
          </div>
        </div>
        <div class="category-bars">
          <div v-for="(item, index) in stats.categoryDistribution.slice(0, 3)" :key="item.id">
            <span>{{ item.name }}</span><div><i :style="{ width: `${Math.min(item.percent, 100)}%`, background: chartColors[index] }"></i></div><strong>{{ item.percent }}%</strong>
          </div>
        </div>
      </section>
    </div>

    <div class="dashboard-row bottom-row">
      <section class="admin-card recent-orders">
        <div class="admin-section-title">
          <h3>最近订单</h3>
          <router-link to="/admin/orders" class="text-link">查看全部 <el-icon><Right /></el-icon></router-link>
        </div>
        <el-table :data="stats.recentOrders" style="width: 100%">
          <el-table-column label="顾客" min-width="120">
            <template #default="{ row }"><span class="customer-cell"><i>{{ (row.userName || '客').slice(0,1) }}</i>{{ row.userName }}</span></template>
          </el-table-column>
          <el-table-column label="蛋糕" min-width="170">
            <template #default="{ row }"><span class="order-goods"><img :src="row.goodsImg" alt="" /><span><strong>{{ row.goodsName }}</strong><em>{{ row.time }}</em></span></span></template>
          </el-table-column>
          <el-table-column label="数量" prop="num" width="65" align="center" />
          <el-table-column label="金额" width="100">
            <template #default="{ row }"><strong class="amount">¥{{ money(row.total) }}</strong></template>
          </el-table-column>
          <el-table-column label="状态" width="105">
            <template #default="{ row }"><span class="status-pill" :class="`s-${row.status}`">{{ row.status }}</span></template>
          </el-table-column>
        </el-table>
      </section>

      <div class="side-column">
        <section class="admin-card low-stock-card">
          <div class="admin-section-title">
            <h3>库存提醒</h3>
            <router-link to="/admin/goods" class="text-link">管理 <el-icon><Right /></el-icon></router-link>
          </div>
          <div class="stock-list">
            <div v-for="item in stats.lowStock" :key="item.id" class="stock-item">
              <img :src="item.img" alt="" />
              <div><strong>{{ item.name }}</strong><span>库存仅剩 {{ item.num }} 份</span></div>
              <span class="stock-badge" :class="{ urgent: item.num <= 5 }">{{ item.num <= 5 ? '需补货' : '偏低' }}</span>
            </div>
            <div v-if="!stats.lowStock.length" class="empty-block">目前库存充足</div>
          </div>
        </section>
        <section class="quick-panel">
          <span class="eyebrow">QUICK ACTION</span>
          <h3>今天的兔南事务</h3>
          <div class="quick-actions">
            <router-link to="/admin/orders"><el-icon><Tickets /></el-icon><span>处理订单</span><em>{{ stats.kpi.pending }}</em></router-link>
            <router-link to="/admin/notices"><el-icon><Bell /></el-icon><span>发布公告</span><el-icon><Right /></el-icon></router-link>
            <router-link to="/admin/categories"><el-icon><CollectionTag /></el-icon><span>整理分类</span><el-icon><Right /></el-icon></router-link>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { authState } from '../../utils/auth'
import request from '../../utils/request'
import { money } from '../../utils/format'

const loading = ref(true)
const chartColors = ['#9d6069', '#c9a66a', '#7c8c72', '#36342c', '#c98f7c', '#8d9fa2']
const stats = reactive({
  kpi: { revenue: 0, orders: 0, pending: 0, users: 0, goods: 0, newUsers: 0, avgOrder: 0 },
  week: [],
  categoryDistribution: [],
  lowStock: [],
  recentOrders: []
})

const weekTotal = computed(() => stats.week.reduce((sum, item) => sum + Number(item.value || 0), 0))
const maxWeek = computed(() => Math.max(...stats.week.map(item => Number(item.value || 0)), 1))
const barHeight = (value) => `${Math.max(4, (Number(value || 0) / maxWeek.value) * 100)}%`
const donutBackground = computed(() => {
  if (!stats.categoryDistribution.length) return '#e7dbcf'
  let current = 0
  const pieces = stats.categoryDistribution.map((item, index) => {
    const start = current
    current += Number(item.percent || 0)
    return `${chartColors[index % chartColors.length]} ${start}% ${Math.min(current, 100)}%`
  })
  if (current < 100) pieces.push(`#e7dbcf ${current}% 100%`)
  return `conic-gradient(${pieces.join(', ')})`
})

const load = async () => {
  loading.value = true
  try {
    const res = await request.get('/dashboard/stats')
    Object.assign(stats, res.data)
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>

<style scoped>
.dashboard-heading { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 26px; }
.dashboard-heading h1 { font-family: var(--font-display); font-size: 40px; font-weight: 500; margin: 9px 0 5px; letter-spacing: -.02em; }
.dashboard-heading p { color: var(--ink-muted); font-size: 10px; margin: 0; }
.heading-actions { display: flex; gap: 8px; }
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 17px; min-height: 125px; }
.kpi-card { position: relative; overflow: hidden; min-height: 125px; padding: 22px 20px; border-radius: 19px; border: 1px solid var(--line); background: rgba(255,250,244,.84); box-shadow: 0 6px 22px rgba(65,43,35,.045); display: flex; gap: 14px; align-items: flex-start; }
.kpi-card.card-rose { background: linear-gradient(140deg, #8f525b, #6e3c46); color: white; border: 0; }
.kpi-icon { width: 35px; height: 35px; border-radius: 10px; display: grid; place-items: center; background: var(--rose-pale); color: var(--rose-deep); font-size: 17px; flex: 0 0 auto; }
.kpi-icon.sage { background: var(--sage-pale); color: var(--sage); }
.kpi-icon.gold { background: #f4ead6; color: #a17d3e; }
.kpi-icon.ink { background: #e8e4df; color: var(--ink); }
.card-rose .kpi-icon { background: rgba(255,255,255,.12); color: #f3d9c0; }
.kpi-copy { position: relative; z-index: 2; }
.kpi-copy > span { display: block; color: var(--ink-muted); font-size: 8px; letter-spacing: .09em; margin-bottom: 8px; }
.card-rose .kpi-copy > span { color: rgba(255,255,255,.55); }
.kpi-copy strong { display: block; font-family: var(--font-display); font-size: 30px; font-weight: 500; line-height: 1; white-space: nowrap; }
.kpi-copy strong small { font-family: var(--font-body); font-size: 10px; color: var(--ink-muted); }
.card-rose .kpi-copy strong small { color: rgba(255,255,255,.45); }
.kpi-copy em { display: flex; align-items: center; gap: 4px; margin-top: 11px; color: var(--sage); font-size: 7px; font-style: normal; white-space: nowrap; }
.card-rose .kpi-copy em { color: rgba(255,255,255,.56); }
.kpi-decoration { position: absolute; right: 10px; bottom: 5px; font-family: var(--font-display); font-size: 11px; letter-spacing: .20em; opacity: .08; }
.card-rose .kpi-decoration { color: white; opacity: .15; }
.dashboard-row { display: grid; gap: 17px; margin-bottom: 17px; }
.main-row { grid-template-columns: 1.6fr .9fr; }
.chart-card, .category-chart { padding: 22px 23px; min-height: 350px; }
.chart-head { display: flex; justify-content: space-between; align-items: flex-start; }
.chart-head h3 { font-family: var(--font-display); font-size: 24px; font-weight: 600; margin: 6px 0 0; }
.chart-total { font-family: var(--font-display); color: var(--rose-deep); font-size: 22px; }
.bar-chart { height: 230px; display: flex; gap: 11px; align-items: stretch; position: relative; padding: 25px 3px 0; }
.grid-lines { position: absolute; inset: 22px 0 28px; display: flex; flex-direction: column; justify-content: space-between; }
.grid-lines i { display: block; border-top: 1px dashed rgba(67,47,41,.08); }
.bar-column { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; position: relative; z-index: 2; height: 100%; }
.bar-value { font-size: 6px; color: var(--ink-muted); height: 17px; }
.bar-track { width: 100%; max-width: 37px; flex: 1; display: flex; align-items: flex-end; }
.bar-fill { width: 100%; border-radius: 6px 6px 3px 3px; background: linear-gradient(to top, #d2aeb2, #a6636d); transition: height .8s cubic-bezier(.2,.7,.2,1); min-height: 4px; }
.bar-fill.today { background: linear-gradient(to top, #c2a468, #8a6c35); }
.bar-column > span { height: 25px; display: flex; align-items: flex-end; color: var(--ink-muted); font-size: 7px; }
.donut-wrap { display: flex; align-items: center; gap: 20px; margin: 26px 0 19px; }
.donut { width: 118px; height: 118px; border-radius: 50%; flex: 0 0 auto; display: grid; place-items: center; position: relative; }
.donut::after { content: ''; position: absolute; width: 77px; height: 77px; border-radius: 50%; background: var(--paper); }
.donut > div { position: relative; z-index: 2; text-align: center; }
.donut strong { display: block; font-family: var(--font-display); font-size: 28px; font-weight: 500; line-height: 1; }
.donut span { color: var(--ink-muted); font-size: 7px; }
.category-legend { flex: 1; display: flex; flex-direction: column; gap: 9px; }
.category-legend div { display: flex; align-items: center; gap: 7px; font-size: 8px; }
.category-legend i { width: 6px; height: 6px; border-radius: 50%; flex: 0 0 auto; }
.category-legend span { color: var(--ink-soft); }
.category-legend strong { margin-left: auto; font-size: 8px; }
.category-bars { border-top: 1px solid var(--line); padding-top: 17px; display: flex; flex-direction: column; gap: 10px; }
.category-bars > div { display: grid; grid-template-columns: 58px 1fr 32px; align-items: center; gap: 7px; }
.category-bars span { color: var(--ink-soft); font-size: 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.category-bars div div { height: 5px; background: var(--paper-deep); border-radius: 99px; overflow: hidden; }
.category-bars div div i { display: block; height: 100%; border-radius: 99px; }
.category-bars strong { text-align: right; color: var(--ink-muted); font-size: 7px; font-weight: 500; }
.bottom-row { grid-template-columns: 1.6fr .9fr; }
.recent-orders { overflow: hidden; }
.recent-orders .admin-section-title { padding-bottom: 10px; }
.recent-orders .text-link { font-size: 8px; }
.customer-cell { display: flex; align-items: center; gap: 7px; font-size: 10px; }
.customer-cell i { width: 25px; height: 25px; border-radius: 50%; display: grid; place-items: center; background: var(--paper-deep); color: var(--rose-deep); font-style: normal; font-family: var(--font-display); font-size: 11px; }
.order-goods { display: flex; align-items: center; gap: 9px; }
.order-goods img { width: 34px; height: 34px; border-radius: 8px; object-fit: cover; }
.order-goods strong { display: block; font-size: 9px; margin-bottom: 3px; }
.order-goods em { color: var(--ink-muted); font-size: 7px; font-style: normal; }
.amount { font-family: var(--font-display); font-size: 16px; font-weight: 600; }
.status-pill { display: inline-block; border-radius: 99px; padding: 4px 8px; font-size: 7px; background: #eee8e1; color: #7b6b62; }
.s-待制作, .s-制作中 { background: #f4ead4; color: #917039; }
.s-待取货 { background: var(--sage-pale); color: #61745d; }
.s-已完成 { background: #ece8e3; color: #7b6c64; }
.s-已取消 { background: #f6e4e2; color: #a55757; }
.side-column { display: flex; flex-direction: column; gap: 17px; }
.low-stock-card { padding-bottom: 10px; }
.stock-list { padding: 3px 16px 10px; }
.stock-item { display: flex; align-items: center; gap: 9px; padding: 9px 5px; border-bottom: 1px solid var(--line); }
.stock-item:last-child { border-bottom: 0; }
.stock-item img { width: 34px; height: 34px; border-radius: 8px; object-fit: cover; }
.stock-item div { flex: 1; min-width: 0; }
.stock-item strong { display: block; font-size: 9px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 3px; }
.stock-item div span { color: var(--ink-muted); font-size: 7px; }
.stock-badge { border-radius: 99px; padding: 4px 7px; font-size: 7px; background: #f8edda; color: #9c7a3e; white-space: nowrap; }
.stock-badge.urgent { background: #f6e3e1; color: #a55757; }
.quick-panel { border-radius: 19px; background: var(--ink); color: #f0e3d4; padding: 22px 21px; }
.quick-panel .eyebrow { color: var(--gold-light); }
.quick-panel h3 { font-family: var(--font-display); font-size: 22px; font-weight: 500; margin: 7px 0 16px; }
.quick-actions { display: flex; flex-direction: column; }
.quick-actions a { display: flex; align-items: center; gap: 8px; padding: 11px 0; border-top: 1px solid rgba(255,255,255,.1); color: rgba(240,227,212,.6); text-decoration: none; font-size: 8px; }
.quick-actions a:hover { color: #f0e3d4; }
.quick-actions a span { flex: 1; }
.quick-actions a em { background: var(--rose); color: white; border-radius: 99px; font-size: 7px; padding: 2px 6px; font-style: normal; }
@media (max-width: 1150px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
  .main-row, .bottom-row { grid-template-columns: 1fr; }
}
@media (max-width: 650px) {
  .dashboard-heading { align-items: flex-start; flex-direction: column; gap: 17px; }
  .dashboard-heading h1 { font-size: 34px; }
  .heading-actions { width: 100%; }
  .heading-actions .btn { flex: 1; }
  .kpi-grid { grid-template-columns: 1fr; }
  .kpi-card { min-height: 110px; }
  .donut-wrap { gap: 12px; }
  .chart-card, .category-chart { padding: 18px; }
  .bar-chart { gap: 4px; }
  .bar-track { max-width: 25px; }
}
</style>