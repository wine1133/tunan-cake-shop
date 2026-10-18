<template>
  <div class="account-wrap">
    <div class="container">
      <AccountHeader title="我的订单" subtitle="每一份为你制作的甜，都在这里留下记录。" />
      <div class="order-stats" v-if="orders.length">
        <div><span>累计预订</span><strong>{{ orders.length }}<em>单</em></strong></div>
        <div><span>甜蜜进行中</span><strong>{{ activeCount }}<em>单</em></strong></div>
        <div><span>累计消费</span><strong><small>¥</small>{{ money(totalSpent) }}</strong></div>
        <div class="mini-art"><el-icon><Present /></el-icon><span>会员生日月<br />可领取专属好礼</span></div>
      </div>

      <div class="order-filter">
        <button v-for="item in filters" :key="item.value" :class="{ active: filter === item.value }" @click="filter = item.value">
          {{ item.label }}<span>{{ item.count }}</span>
        </button>
      </div>

      <div v-loading="loading" class="orders-list">
        <article v-for="order in filteredOrders" :key="order.id" class="order-card">
          <div class="order-card-top">
            <div class="order-number"><span>订单编号</span><strong>#LM{{ String(order.id).padStart(6, '0') }}</strong></div>
            <div class="order-status" :class="`status-${order.status}`">{{ order.status }}</div>
          </div>
          <div class="order-card-main">
            <div class="order-product-image"><img :src="order.goodsImg" :alt="order.goodsName" /></div>
            <div class="order-product-info">
              <span class="order-category">TU NAN · HANDMADE</span>
              <h3>{{ order.goodsName }}</h3>
              <p>{{ order.goodsUnit }} · 数量 {{ order.num }}</p>
              <div class="order-timeline">
                <span class="done"></span><i :class="{ done: stepIndex(order.status) >= 1 }"></i><span :class="{ done: stepIndex(order.status) >= 1 }"></span><i :class="{ done: stepIndex(order.status) >= 2 }"></i><span :class="{ done: stepIndex(order.status) >= 2 }"></span><i :class="{ done: stepIndex(order.status) >= 3 }"></i><span :class="{ done: stepIndex(order.status) >= 3 }"></span>
              </div>
              <div class="timeline-labels"><span>已预订</span><span>制作中</span><span>待取货</span><span>已完成</span></div>
            </div>
            <div class="order-address">
              <span>收货信息</span>
              <strong>{{ order.aName }} · {{ order.aPhone }}</strong>
              <p>{{ order.aAddress }}</p>
            </div>
            <div class="order-price">
              <span>订单金额</span>
              <strong><small>¥</small>{{ money(order.total) }}</strong>
              <em>{{ order.time }}</em>
            </div>
          </div>
          <div class="order-card-foot">
            <span><el-icon><Clock /></el-icon> 下单时间 {{ order.time }}</span>
            <div>
              <button class="order-text-btn" @click="contactService">联系客服</button>
              <button class="order-text-btn danger" @click="deleteOrder(order)">{{ order.status === '已完成' ? '删除记录' : '取消预订' }}</button>
              <router-link to="/catalog" class="btn btn-outline btn-small">再订一份</router-link>
            </div>
          </div>
        </article>

        <div v-if="!loading && !filteredOrders.length" class="orders-empty">
          <div class="empty-circle"><el-icon><Dish /></el-icon></div>
          <h3>{{ orders.length ? '这里还没有这一状态的订单' : '还没有预订过蛋糕' }}</h3>
          <p>{{ orders.length ? '换一个筛选条件看看。' : '去挑一份喜欢的甜，让今天多一点仪式感。' }}</p>
          <router-link to="/catalog" class="btn btn-primary btn-small">去挑选蛋糕 <el-icon><ArrowRight /></el-icon></router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AccountHeader from '../components/AccountHeader.vue'
import request from '../utils/request'
import { money } from '../utils/format'

const orders = ref([])
const loading = ref(true)
const filter = ref('全部')
const filters = computed(() => [
  { label: '全部', value: '全部', count: orders.value.length },
  { label: '进行中', value: '进行中', count: orders.value.filter(o => ['待制作', '制作中', '待取货'].includes(o.status)).length },
  { label: '已完成', value: '已完成', count: orders.value.filter(o => o.status === '已完成').length }
])
const activeCount = computed(() => orders.value.filter(o => ['待制作', '制作中', '待取货'].includes(o.status)).length)
const totalSpent = computed(() => orders.value.filter(o => o.status !== '已取消').reduce((sum, o) => sum + Number(o.total || 0), 0))
const filteredOrders = computed(() => {
  if (filter.value === '全部') return orders.value
  if (filter.value === '进行中') return orders.value.filter(o => ['待制作', '制作中', '待取货'].includes(o.status))
  return orders.value.filter(o => o.status === filter.value)
})

const load = async () => {
  loading.value = true
  try {
    const res = await request.get('/orders/selectPage', { params: { pageNum: 1, pageSize: 50 } })
    orders.value = res.data?.list || []
  } finally {
    loading.value = false
  }
}

const stepIndex = (status) => ({ 待制作: 1, 制作中: 1, 待取货: 2, 已完成: 3, 已取消: 0 }[status] || 0)

const deleteOrder = async (order) => {
  try {
    await ElMessageBox.confirm(`确定要${order.status === '已完成' ? '删除这条订单记录' : '取消这份预订'}吗？`, '操作确认', { type: 'warning', confirmButtonText: '确定', cancelButtonText: '再想想' })
    await request.delete(`/orders/delete/${order.id}`)
    ElMessage.success('操作成功')
    load()
  } catch (error) {}
}

const contactService = () => ElMessage.info('兔南客服：021-6888 1024（每日 09:00-21:00）')
onMounted(load)
</script>

<style scoped>
.order-stats { display: grid; grid-template-columns: repeat(3, 1fr) 1.25fr; gap: 14px; margin-bottom: 34px; }
.order-stats > div { background: rgba(255,250,244,.72); border: 1px solid var(--line); border-radius: 18px; padding: 20px 22px; }
.order-stats span { color: var(--ink-muted); font-size: 9px; letter-spacing: .08em; }
.order-stats strong { display: block; font-family: var(--font-display); font-size: 34px; font-weight: 500; margin-top: 8px; }
.order-stats strong em { font-family: var(--font-body); font-style: normal; font-size: 9px; color: var(--ink-muted); margin-left: 4px; }
.order-stats strong small { font-size: 14px; }
.order-stats .mini-art { background: var(--ink); color: #f4e9db; display: flex; align-items: center; gap: 14px; border: 0; }
.mini-art .el-icon { font-size: 28px; color: var(--gold-light); }
.mini-art span { color: rgba(244,233,219,.6); font-size: 8px; line-height: 1.7; letter-spacing: .06em; }
.order-filter { display: flex; gap: 7px; margin-bottom: 18px; }
.order-filter button { border: 1px solid var(--line); background: transparent; color: var(--ink-soft); border-radius: 999px; padding: 9px 15px; cursor: pointer; font-size: 10px; transition: .2s; }
.order-filter button span { margin-left: 6px; color: var(--ink-muted); font-size: 8px; }
.order-filter button.active { background: var(--ink); color: white; }
.order-filter button.active span { color: rgba(255,255,255,.5); }
.orders-list { min-height: 300px; }
.order-card { background: rgba(255,250,244,.82); border: 1px solid var(--line); border-radius: 22px; margin-bottom: 16px; overflow: hidden; transition: .3s; }
.order-card:hover { box-shadow: var(--shadow-sm); }
.order-card-top { padding: 15px 23px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--line); background: rgba(240,230,216,.22); }
.order-number { display: flex; align-items: center; gap: 10px; }
.order-number span { color: var(--ink-muted); font-size: 8px; letter-spacing: .1em; }
.order-number strong { font-size: 10px; letter-spacing: .05em; }
.order-status { padding: 6px 12px; border-radius: 999px; font-size: 9px; background: var(--paper-deep); color: var(--ink-soft); }
.status-待制作, .status-制作中 { background: #f4ead4; color: #917039; }
.status-待取货 { background: var(--sage-pale); color: #61745d; }
.status-已完成 { background: #ece8e3; color: #7b6c64; }
.status-已取消 { background: #f6e4e2; color: #a55757; }
.order-card-main { display: grid; grid-template-columns: 110px 1.2fr 1fr 130px; gap: 22px; padding: 24px 23px; align-items: center; }
.order-product-image { width: 110px; height: 105px; border-radius: 14px; overflow: hidden; background: var(--paper-deep); }
.order-product-image img { width: 100%; height: 100%; object-fit: cover; }
.order-category { color: var(--rose-deep); font-size: 7px; letter-spacing: .17em; }
.order-product-info h3 { font-family: var(--font-display); font-size: 25px; font-weight: 600; margin: 5px 0 5px; }
.order-product-info > p { color: var(--ink-muted); font-size: 9px; margin: 0 0 16px; }
.order-timeline { display: flex; align-items: center; width: 165px; }
.order-timeline span { width: 8px; height: 8px; border-radius: 50%; border: 1px solid #cfc1b7; background: var(--paper); }
.order-timeline span.done { background: var(--rose); border-color: var(--rose); }
.order-timeline i { height: 1px; flex: 1; background: #ded2c8; }
.order-timeline i.done { background: var(--rose); }
.timeline-labels { width: 190px; display: flex; justify-content: space-between; color: var(--ink-muted); font-size: 7px; margin-top: 5px; }
.order-address { border-left: 1px solid var(--line); padding-left: 22px; }
.order-address span, .order-price > span { display: block; color: var(--ink-muted); font-size: 8px; letter-spacing: .08em; margin-bottom: 8px; }
.order-address strong { font-size: 10px; }
.order-address p { color: var(--ink-soft); font-size: 9px; line-height: 1.6; margin: 5px 0 0; }
.order-price { text-align: right; }
.order-price strong { font-family: var(--font-display); font-size: 30px; font-weight: 500; }
.order-price strong small { font-size: 12px; }
.order-price em { display: block; font-style: normal; color: var(--ink-muted); font-size: 8px; margin-top: 7px; }
.order-card-foot { display: flex; justify-content: space-between; align-items: center; padding: 13px 23px; border-top: 1px solid var(--line); }
.order-card-foot > span { display: flex; align-items: center; gap: 5px; color: var(--ink-muted); font-size: 8px; }
.order-card-foot > div { display: flex; align-items: center; gap: 6px; }
.order-text-btn { border: 0; background: none; color: var(--ink-soft); font-size: 9px; cursor: pointer; padding: 7px 9px; }
.order-text-btn.danger { color: var(--rose-deep); }
.orders-empty { text-align: center; padding: 75px 20px 95px; background: rgba(255,250,244,.55); border: 1px dashed var(--line); border-radius: 22px; }
.empty-circle { width: 72px; height: 72px; margin: 0 auto 19px; border-radius: 50%; background: var(--paper-deep); display: grid; place-items: center; color: var(--rose); font-size: 30px; }
.orders-empty h3 { font-family: var(--font-display); font-size: 28px; font-weight: 500; margin: 0 0 8px; }
.orders-empty p { color: var(--ink-muted); font-size: 10px; margin: 0 0 22px; }
@media (max-width: 900px) {
  .order-stats { grid-template-columns: repeat(3, 1fr); }
  .order-stats .mini-art { display: none; }
  .order-card-main { grid-template-columns: 90px 1fr 130px; }
  .order-product-image { width: 90px; height: 94px; }
  .order-address { display: none; }
}
@media (max-width: 620px) {
  .order-stats { grid-template-columns: 1fr 1fr; }
  .order-stats > div:last-child { display: block; grid-column: span 2; }
  .order-card-main { grid-template-columns: 75px 1fr; gap: 14px; }
  .order-product-image { width: 75px; height: 82px; }
  .order-price { grid-column: span 2; text-align: left; border-top: 1px solid var(--line); padding-top: 13px; display: flex; align-items: center; gap: 10px; }
  .order-price > span { margin: 0; }
  .order-price em { margin-left: auto; }
  .order-card-foot { flex-direction: column; align-items: flex-start; gap: 12px; }
  .order-card-foot > div { width: 100%; justify-content: flex-end; flex-wrap: wrap; }
  .order-timeline, .timeline-labels { display: none; }
}
</style>