<template>
  <div>
    <AdminPageHeader eyebrow="ANNOUNCEMENTS" title="系统公告" subtitle="把新品、活动与重要说明，及时告诉每一位顾客。">
      <el-button type="primary" @click="openCreate"><el-icon><Plus /></el-icon> 发布公告</el-button>
    </AdminPageHeader>

    <div class="notice-admin-top">
      <div><el-icon><Bell /></el-icon><span>已发布公告</span><strong>{{ total }}</strong><small>条</small></div>
      <p>公告会展示在店铺首页的「兔南播报」与后台通知中，发布前请确认内容准确。</p>
    </div>

    <div class="notice-admin-grid" v-loading="loading">
      <article v-for="(notice, index) in rows" :key="notice.id" class="notice-admin-card" :class="{ featured: index === 0 }">
        <div class="notice-card-top">
          <span class="notice-index">{{ String(index + 1).padStart(2, '0') }}</span>
          <span class="notice-time">{{ notice.time }}</span>
        </div>
        <div class="notice-symbol">“</div>
        <h3>{{ notice.name }}</h3>
        <p>{{ notice.content }}</p>
        <div class="notice-card-foot">
          <span><el-icon><View /></el-icon> 店铺首页展示</span>
          <div>
            <button @click="openEdit(notice)"><el-icon><Edit /></el-icon> 编辑</button>
            <button class="danger" @click="removeNotice(notice)"><el-icon><Delete /></el-icon></button>
          </div>
        </div>
      </article>
      <button class="notice-add-card" @click="openCreate"><span><el-icon><Plus /></el-icon></span><strong>写下新的兔南播报</strong><p>新品、活动或门店通知</p></button>
    </div>
    <div class="pagination-wrap" v-if="total > pageSize"><el-pagination background layout="prev, pager, next" :page-size="pageSize" :current-page="pageNum" :total="total" @current-change="changePage" /></div>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑公告' : '发布新公告'" width="520px" :close-on-click-modal="false">
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="公告标题" prop="name"><el-input v-model="form.name" placeholder="简洁地概括这条消息" maxlength="80" show-word-limit /></el-form-item>
        <el-form-item label="公告内容" prop="content"><el-input v-model="form.content" type="textarea" :rows="5" placeholder="写下具体内容与时间范围" maxlength="500" show-word-limit /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" :loading="saving" @click="save">确认发布</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AdminPageHeader from '../../components/AdminPageHeader.vue'
import request from '../../utils/request'

const rows = ref([])
const total = ref(0)
const pageNum = ref(1)
const pageSize = ref(8)
const loading = ref(true)
const dialogVisible = ref(false)
const saving = ref(false)
const formRef = ref()
const form = reactive({ id: null, name: '', content: '' })
const rules = {
  name: [{ required: true, message: '请输入公告标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入公告内容', trigger: 'blur' }]
}

const load = async () => {
  loading.value = true
  try {
    const res = await request.get('/notice/selectPage', { params: { pageNum: pageNum.value, pageSize: pageSize.value } })
    rows.value = res.data?.list || []
    total.value = res.data?.total || 0
  } finally { loading.value = false }
}
const changePage = (page) => { pageNum.value = page; load() }
const openCreate = () => { Object.assign(form, { id: null, name: '', content: '' }); dialogVisible.value = true }
const openEdit = (notice) => { Object.assign(form, notice); dialogVisible.value = true }
const save = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    saving.value = true
    try {
      if (form.id) await request.put('/notice/update', form)
      else await request.post('/notice/add', form)
      ElMessage.success('公告已发布')
      dialogVisible.value = false
      load()
    } finally { saving.value = false }
  })
}
const removeNotice = async (notice) => {
  try {
    await ElMessageBox.confirm(`确定删除公告「${notice.name}」吗？`, '删除公告', { type: 'warning' })
    await request.delete(`/notice/delete/${notice.id}`)
    ElMessage.success('公告已删除')
    load()
  } catch (error) {}
}
onMounted(load)
</script>

<style scoped>
.notice-admin-top { display: flex; align-items: center; gap: 24px; margin-bottom: 19px; padding: 15px 21px; border: 1px solid var(--line); border-radius: 15px; background: rgba(255,250,244,.65); }
.notice-admin-top > div { display: flex; align-items: baseline; gap: 5px; }
.notice-admin-top .el-icon { color: var(--rose); align-self: center; margin-right: 3px; }
.notice-admin-top span { color: var(--ink-muted); font-size: 8px; }
.notice-admin-top strong { font-family: var(--font-display); font-size: 25px; font-weight: 500; }
.notice-admin-top small { color: var(--ink-muted); font-size: 8px; }
.notice-admin-top p { margin: 0 0 0 auto; color: var(--ink-muted); font-size: 8px; }
.notice-admin-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; min-height: 250px; }
.notice-admin-card { min-height: 245px; border-radius: 20px; border: 1px solid var(--line); background: rgba(255,250,244,.8); padding: 20px 22px 0; display: flex; flex-direction: column; position: relative; overflow: hidden; }
.notice-admin-card.featured { background: linear-gradient(145deg, #f5e6e4, #fff9f2); border-color: rgba(140,74,85,.17); }
.notice-admin-card::after { content: ''; position: absolute; width: 130px; height: 130px; border: 1px solid rgba(140,74,85,.1); border-radius: 50%; right: -60px; top: -68px; }
.notice-card-top { display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 2; }
.notice-index { color: var(--rose); font-family: var(--font-display); font-size: 15px; }
.notice-time { color: var(--ink-muted); font-size: 7px; letter-spacing: .05em; }
.notice-symbol { color: var(--rose); font-family: var(--font-display); font-size: 42px; line-height: .5; height: 23px; margin-top: 18px; opacity: .5; }
.notice-admin-card h3 { font-family: var(--font-display); font-size: 24px; font-weight: 600; margin: 4px 0 8px; }
.notice-admin-card > p { color: var(--ink-soft); font-size: 9px; line-height: 1.75; margin: 0; flex: 1; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.notice-card-foot { border-top: 1px solid var(--line); min-height: 48px; display: flex; justify-content: space-between; align-items: center; margin-top: 14px; }
.notice-card-foot > span { display: flex; align-items: center; gap: 4px; color: var(--ink-muted); font-size: 7px; }
.notice-card-foot > div { display: flex; gap: 4px; }
.notice-card-foot button { border: 0; background: none; cursor: pointer; color: var(--ink-soft); font-size: 8px; padding: 6px; display: flex; gap: 3px; align-items: center; }
.notice-card-foot button.danger { color: var(--ink-muted); }
.notice-add-card { min-height: 245px; border: 1px dashed rgba(67,47,41,.2); border-radius: 20px; background: rgba(255,250,244,.3); display: flex; flex-direction: column; justify-content: center; align-items: center; color: var(--ink-soft); cursor: pointer; transition: .25s; }
.notice-add-card:hover { border-color: var(--rose); background: rgba(255,250,244,.65); }
.notice-add-card > span { width: 48px; height: 48px; border-radius: 50%; background: var(--paper-deep); color: var(--rose-deep); display: grid; place-items: center; font-size: 20px; margin-bottom: 12px; }
.notice-add-card strong { font-size: 11px; }
.notice-add-card p { color: var(--ink-muted); font-size: 8px; margin: 6px 0 0; }
.pagination-wrap { display: flex; justify-content: center; margin-top: 25px; }
@media (max-width: 800px) { .notice-admin-grid { grid-template-columns: 1fr; } .notice-admin-top p { display: none; } }
</style>