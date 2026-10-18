<template>
  <div>
    <AdminPageHeader eyebrow="ORDER CENTER" title="订单管理" subtitle="跟进每一份蛋糕的制作状态，让甜蜜准时抵达。" />

    <div class="order-summary">
      <div><span>全部订单</span><strong>{{ total }}</strong><small>单</small></div>
      <div><span>本页金额</span><strong><small>¥</small>{{ money(pageTotal) }}</strong></div>
      <div><span>待处理</span><strong class="warn">{{ pending }}</strong><small>单</small></div>
      <p><el-icon><InfoFilled /></el-icon> 订单状态变更后，顾客端将立即同步。</p>
    </div>

    <div class="admin-card">
      <div class="admin-toolbar">
        <div class="admin-toolbar-left">
          <el-input v-model="keyword" class="admin-search" placeholder="搜索商品名称" clearable @keyup.enter="search" @clear="search">
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
          <el-select v-model="statusFilter" placeholder="全部状态" clearable style="width: 130px" @change="search">
            <el-option v-for="item in statuses" :key="item" :label="item" :value="item" />
          </el-select>
          <el-button @click="search"><el-icon><Search /></el-icon> 查询</el-button>
        </div>
        <div class="admin-toolbar-right">
          <el-button :loading="loading" @click="load"><el-icon><Refresh /></el-icon> 刷新</el-button>
        </div>
      </div>
      <div class="admin-table-wrap">
        <el-table :data="rows" style="width: 100%" v-loading="loading">
          <el-table-column label="订单号" width="125">
            <template #default="{ row }"><span class="order-no">#LM{{ String(row.id).padStart(6, '0') }}</span><em class="order-time">{{ row.time }}</em></template>
          </el-table-column>
          <el-table-column label="顾客" width="140">
            <template #default="{ row }"><div class="customer-cell"><i>{{ (row.userName || '客').slice(0,1) }}</i><div><strong>{{ row.userName }}</strong><em>{{ row.aPhone }}</em></div></div></template>
          </el-table-column>
          <el-table-column label="蛋糕" min-width="190">
            <template #default="{ row }"><div class="table-product"><img :src="row.goodsImg" alt="" /><div><strong>{{ row.goodsName }}</strong><span>{{ row.goodsUnit }} × {{ row.num }}</span></div></div></template>
          </el-table-column>
          <el-table-column label="收货地址" min-width="190"><template #default="{ row }"><span class="address-cell"><el-icon><Location /></el-icon>{{ row.aAddress }}</span></template></el-table-column>
          <el-table-column label="总价" width="100"><template #default="{ row }"><strong class="price-cell">¥{{ money(row.total) }}</strong></template></el-table-column>
          <el-table-column label="订单状态" width="130">
            <template #default="{ row }">
              <el-select :model-value="row.status" size="small" class="status-select" @change="(value) => updateStatus(row, value)">
                <el-option v-for="item in statuses" :key="item" :label="item" :value="item" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="115" align="center">
            <template #default="{ row }">
              <div class="table-actions">
                <el-button size="small" @click="openDetail(row)"><el-icon><View /></el-icon> 详情</el-button>
                <el-button size="small" type="danger" plain @click="removeOrder(row)"><el-icon><Delete /></el-icon></el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="table-footer"><span>共 {{ total }} 条订单</span><el-pagination background layout="prev, pager, next" :page-size="pageSize" :current-page="pageNum" :total="total" @current-change="changePage" /></div>
    </div>

    <el-drawer v-model="detailVisible" title="订单详情" size="430px">
      <div v-if="current" class="order-detail">
        <div class="detail-hero">
          <img :src="current.goodsImg" alt="" />
          <div><span>ORDER #LM{{ String(current.id).padStart(6, '0') }}</span><h3>{{ current.goodsName }}</h3><p>{{ current.goodsUnit }} · 数量 {{ current.num }}</p></div>
        </div>
        <div class="detail-section"><span class="detail-label">订单状态</span><div class="detail-status-row"><el-tag :type="statusType(current.status)" effect="light">{{ current.status }}</el-tag><em>{{ current.time }}</em></div></div>
        <div class="detail-section"><span class="detail-label">收货信息</span><strong>{{ current.aName }} · {{ current.aPhone }}</strong><p>{{ current.aAddress }}</p></div>
        <div class="detail-section"><span class="detail-label">顾客账户</span><strong>{{ current.userName }}</strong><p>用户 ID：{{ current.userId }}</p></div>
        <div class="detail-total"><span>订单金额</span><strong>¥{{ money(current.total) }}</strong></div>
        <el-button class="full" type="primary" @click="nextStatus(current)">更新为「{{ nextStatusLabel(current.status) }}」</el-button>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AdminPageHeader from '../../components/AdminPageHeader.vue'
import request from '../../utils/request'
import { money, statusType } from '../../utils/format'

const rows = ref([])
const total = ref(0)
const pageNum = ref(1)
const pageSize = ref(8)
const keyword = ref('')
const statusFilter = ref('')
const loading = ref(true)
const detailVisible = ref(false)
const current = ref(null)
const statuses = ['待制作', '制作中', '待取货', '已完成', '已取消']
const pageTotal = computed(() => rows.value.reduce((sum, item) => sum + Number(item.total || 0), 0))
const pending = computed(() => rows.value.filter(item => ['待制作', '制作中'].includes(item.status)).length)

const load = async () => {
  loading.value = true
  try {
    const res = await request.get('/orders/selectPage', { params: { pageNum: pageNum.value, pageSize: pageSize.value, goodsName: keyword.value, status: statusFilter.value } })
    rows.value = res.data?.list || []
    total.value = res.data?.total || 0
  } finally { loading.value = false }
}
const search = () => { pageNum.value = 1; load() }
const changePage = (page) => { pageNum.value = page; load() }
const openDetail = (row) => { current.value = row; detailVisible.value = true }
const nextStatusLabel = (status) => ({ 待制作: '制作中', 制作中: '待取货', 待取货: '已完成', 已完成: '已完成', 已取消: '待制作' }[status] || '待制作')
const nextStatus = (row) => updateStatus(row, nextStatusLabel(row.status))

const updateStatus = async (row, value) => {
  if (value === row.status) return
  try {
    await request.put(`/orders/status/${row.id}`, { status: value })
    row.status = value
    if (current.value?.id === row.id) current.value.status = value
    ElMessage.success('订单状态已更新')
  } catch (error) { load() }
}
const removeOrder = async (row) => {
  try {
    await ElMessageBox.confirm(`确定删除订单「#LM${String(row.id).padStart(6, '0')}」吗？库存将自动回补。`, '删除订单', { type: 'warning' })
    await request.delete(`/orders/delete/${row.id}`)
    ElMessage.success('订单已删除')
    load()
  } catch (error) {}
}
onMounted(load)
</script>

<style scoped>
.order-summary { display: grid; grid-template-columns: repeat(3, 150px) 1fr; gap: 10px; margin-bottom: 18px; }
.order-summary > div { background: rgba(255,250,244,.75); border: 1px solid var(--line); border-radius: 14px; padding: 13px 15px; display: flex; align-items: baseline; gap: 5px; }
.order-summary span { color: var(--ink-muted); font-size: 8px; margin-right: auto; }
.order-summary strong { font-family: var(--font-display); font-size: 24px; font-weight: 500; }
.order-summary strong.warn { color: #a97935; }
.order-summary small { color: var(--ink-muted); font-size: 8px; }
.order-summary p { margin: 0; align-self: center; text-align: right; color: var(--ink-muted); font-size: 8px; display: flex; justify-content: flex-end; gap: 5px; }
.order-no { display: block; font-size: 9px; font-weight: 600; margin-bottom: 4px; }
.order-time { display: block; font-size: 7px; color: var(--ink-muted); font-style: normal; }
.customer-cell { display: flex; align-items: center; gap: 8px; }
.customer-cell i { width: 27px; height: 27px; border-radius: 50%; background: var(--paper-deep); color: var(--rose-deep); display: grid; place-items: center; font-style: normal; font-family: var(--font-display); font-size: 12px; }
.customer-cell strong { display: block; font-size: 9px; margin-bottom: 3px; }
.customer-cell em { color: var(--ink-muted); font-size: 7px; font-style: normal; }
.address-cell { display: flex; gap: 5px; color: var(--ink-soft); font-size: 8px; line-height: 1.5; }
.address-cell .el-icon { color: var(--rose); margin-top: 2px; flex: 0 0 auto; }
.price-cell { font-family: var(--font-display); font-size: 18px; font-weight: 600; }
.status-select { width: 105px; }
.status-select :deep(.el-select__wrapper) { min-height: 30px; font-size: 9px; }
.table-footer { display: flex; justify-content: space-between; align-items: center; padding: 15px 22px; border-top: 1px solid var(--line); }
.table-footer > span { color: var(--ink-muted); font-size: 8px; }
.order-detail { padding: 0 6px; }
.detail-hero { display: flex; gap: 15px; padding-bottom: 22px; border-bottom: 1px solid var(--line); }
.detail-hero img { width: 95px; height: 95px; object-fit: cover; border-radius: 14px; }
.detail-hero span { color: var(--rose-deep); font-size: 7px; letter-spacing: .1em; }
.detail-hero h3 { font-family: var(--font-display); font-size: 27px; font-weight: 600; margin: 7px 0 5px; }
.detail-hero p { color: var(--ink-muted); font-size: 9px; margin: 0; }
.detail-section { padding: 19px 0; border-bottom: 1px solid var(--line); }
.detail-label { display: block; color: var(--ink-muted); font-size: 8px; letter-spacing: .09em; margin-bottom: 9px; }
.detail-section strong { font-size: 11px; }
.detail-section p { color: var(--ink-soft); font-size: 9px; line-height: 1.6; margin: 5px 0 0; }
.detail-status-row { display: flex; justify-content: space-between; align-items: center; }
.detail-status-row em { color: var(--ink-muted); font-size: 8px; font-style: normal; }
.detail-total { display: flex; justify-content: space-between; align-items: center; padding: 22px 0; }
.detail-total span { color: var(--ink-muted); font-size: 9px; }
.detail-total strong { font-family: var(--font-display); font-size: 32px; font-weight: 500; color: var(--rose-deep); }
@media (max-width: 800px) {
  .order-summary { grid-template-columns: repeat(3, 1fr); }
  .order-summary p { display: none; }
}
@media (max-width: 550px) {
  .order-summary { grid-template-columns: 1fr 1fr; }
  .order-summary > div:nth-child(3) { display: none; }
  .table-footer { flex-direction: column; gap: 10px; }
}
</style>