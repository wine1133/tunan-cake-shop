<template>
  <div>
    <AdminPageHeader eyebrow="DELIVERY" title="收货地址" subtitle="查看所有顾客保存的配送信息，协助订单准确送达。" />

    <div class="address-admin-summary">
      <div class="summary-icon"><el-icon><Van /></el-icon></div>
      <div><span>地址总数</span><strong>{{ total }}</strong></div>
      <p>上海市内订单支持全程冷链配送。请勿在未经顾客确认的情况下修改收货信息。</p>
    </div>

    <div class="admin-card">
      <div class="admin-toolbar">
        <div class="admin-toolbar-left">
          <el-input v-model="keyword" class="admin-search" placeholder="搜索收货地址" clearable @keyup.enter="search" @clear="search"><template #prefix><el-icon><Search /></el-icon></template></el-input>
          <el-button @click="search"><el-icon><Search /></el-icon> 查询</el-button>
        </div>
        <div class="admin-toolbar-right"><el-button :loading="loading" @click="load"><el-icon><Refresh /></el-icon> 刷新</el-button></div>
      </div>
      <div class="admin-table-wrap">
        <el-table :data="rows" style="width: 100%" v-loading="loading">
          <el-table-column label="顾客" width="170">
            <template #default="{ row }"><div class="customer-cell"><i>{{ (row.userName || '客').slice(0,1) }}</i><div><strong>{{ row.userName }}</strong><em>ID {{ row.userId }}</em></div></div></template>
          </el-table-column>
          <el-table-column label="收货人" width="130"><template #default="{ row }"><strong class="receiver-name">{{ row.name }}</strong><span class="receiver-phone">{{ row.phone }}</span></template></el-table-column>
          <el-table-column label="收货地址" min-width="300"><template #default="{ row }"><span class="address-cell"><el-icon><Location /></el-icon>{{ row.address }}</span></template></el-table-column>
          <el-table-column label="标记" width="110"><template #default="{ row }"><span v-if="row.isDefault" class="default-pill">默认地址</span><span v-else class="muted">—</span></template></el-table-column>
          <el-table-column label="操作" width="90" align="center"><template #default="{ row }"><el-button size="small" type="danger" plain @click="removeAddress(row)"><el-icon><Delete /></el-icon> 删除</el-button></template></el-table-column>
        </el-table>
      </div>
      <div class="table-footer"><span>共 {{ total }} 个收货地址</span><el-pagination background layout="prev, pager, next" :page-size="pageSize" :current-page="pageNum" :total="total" @current-change="changePage" /></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AdminPageHeader from '../../components/AdminPageHeader.vue'
import request from '../../utils/request'

const rows = ref([])
const total = ref(0)
const pageNum = ref(1)
const pageSize = ref(9)
const keyword = ref('')
const loading = ref(true)

const load = async () => {
  loading.value = true
  try {
    const res = await request.get('/address/selectPage', { params: { pageNum: pageNum.value, pageSize: pageSize.value, address: keyword.value } })
    rows.value = res.data?.list || []
    total.value = res.data?.total || 0
  } finally { loading.value = false }
}
const search = () => { pageNum.value = 1; load() }
const changePage = (page) => { pageNum.value = page; load() }
const removeAddress = async (row) => {
  try {
    await ElMessageBox.confirm(`确定删除「${row.name}」的这个收货地址吗？`, '删除地址', { type: 'warning' })
    await request.delete(`/address/delete/${row.id}`)
    ElMessage.success('地址已删除')
    load()
  } catch (error) {}
}
onMounted(load)
</script>

<style scoped>
.address-admin-summary { display: flex; align-items: center; gap: 15px; padding: 18px 22px; background: rgba(255,250,244,.7); border: 1px solid var(--line); border-radius: 17px; margin-bottom: 18px; }
.summary-icon { width: 38px; height: 38px; border-radius: 11px; background: var(--sage-pale); color: var(--sage); display: grid; place-items: center; font-size: 19px; }
.address-admin-summary > div:nth-child(2) { display: flex; align-items: baseline; gap: 6px; }
.address-admin-summary span { color: var(--ink-muted); font-size: 8px; }
.address-admin-summary strong { font-family: var(--font-display); font-size: 26px; font-weight: 500; }
.address-admin-summary p { margin: 0 0 0 auto; color: var(--ink-muted); font-size: 8px; }
.customer-cell { display: flex; align-items: center; gap: 8px; }
.customer-cell i { width: 27px; height: 27px; border-radius: 50%; background: var(--paper-deep); color: var(--rose-deep); display: grid; place-items: center; font-style: normal; font-family: var(--font-display); font-size: 12px; }
.customer-cell strong { display: block; font-size: 9px; margin-bottom: 3px; }
.customer-cell em { color: var(--ink-muted); font-size: 7px; font-style: normal; }
.receiver-name { display: block; font-size: 10px; margin-bottom: 4px; }
.receiver-phone { color: var(--ink-muted); font-size: 8px; }
.address-cell { display: flex; gap: 5px; color: var(--ink-soft); font-size: 9px; line-height: 1.6; }
.address-cell .el-icon { color: var(--rose); margin-top: 2px; flex: 0 0 auto; }
.default-pill { background: var(--rose-pale); color: var(--rose-deep); border-radius: 99px; padding: 4px 9px; font-size: 8px; }
.table-footer { display: flex; justify-content: space-between; align-items: center; padding: 15px 22px; border-top: 1px solid var(--line); }
.table-footer > span { color: var(--ink-muted); font-size: 8px; }
@media (max-width: 750px) { .address-admin-summary p { display: none; } .table-footer { flex-direction: column; gap: 10px; } }
</style>