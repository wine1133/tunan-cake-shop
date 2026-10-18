<template>
  <div>
    <AdminPageHeader eyebrow="COLLECTIONS" title="分类管理" subtitle="用清晰的分类，让顾客更轻松地找到心仪的味道。" />

    <div class="category-stats">
      <div><span>分类总数</span><strong>{{ categories.length }}</strong><small>个</small></div>
      <p>分类名称将展示在店铺首页与筛选栏中。删除分类前，请先移动或下架该分类下的蛋糕。</p>
    </div>

    <div class="category-admin-grid" v-loading="loading">
      <article v-for="(category, index) in categories" :key="category.id" class="category-admin-card" :class="`palette-${index % 4}`">
        <div class="category-card-head">
          <span class="category-symbol">{{ category.name.slice(0, 1) }}</span>
          <span class="category-number">0{{ index + 1 }}</span>
        </div>
        <div class="category-card-copy">
          <h3>{{ category.name }}</h3>
          <p>{{ category.description || '为这一类甜，写下一点温柔的介绍。' }}</p>
        </div>
        <div class="category-card-foot">
          <span><el-icon><Dish /></el-icon>{{ goodsCount[category.id] || 0 }} 款蛋糕</span>
          <div>
            <button @click="openEdit(category)"><el-icon><Edit /></el-icon> 编辑</button>
            <button class="danger" @click="removeCategory(category)"><el-icon><Delete /></el-icon></button>
          </div>
        </div>
      </article>
      <button class="category-add-card" @click="openCreate">
        <span><el-icon><Plus /></el-icon></span>
        <strong>创建新分类</strong>
        <p>为新的味道留一个位置</p>
      </button>
    </div>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑分类' : '新增分类'" width="450px" :close-on-click-modal="false">
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="分类名称" prop="name"><el-input v-model="form.name" placeholder="例如：法式慕斯" /></el-form-item>
        <el-form-item label="分类介绍"><el-input v-model="form.description" type="textarea" :rows="3" placeholder="用一句话描述这一分类的风味特点" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" :loading="saving" @click="save">保存分类</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AdminPageHeader from '../../components/AdminPageHeader.vue'
import request from '../../utils/request'

const categories = ref([])
const goodsCount = ref({})
const loading = ref(true)
const dialogVisible = ref(false)
const saving = ref(false)
const formRef = ref()
const form = reactive({ id: null, name: '', description: '', icon: '' })
const rules = { name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }] }

const load = async () => {
  loading.value = true
  try {
    const [categoryRes, goodsRes] = await Promise.all([
      request.get('/category/selectAll'),
      request.get('/goods/selectPage', { params: { pageNum: 1, pageSize: 100 } })
    ])
    categories.value = categoryRes.data || []
    const counts = {}
    for (const goods of goodsRes.data?.list || []) counts[goods.categoryId] = (counts[goods.categoryId] || 0) + 1
    goodsCount.value = counts
  } finally { loading.value = false }
}

const openCreate = () => { Object.assign(form, { id: null, name: '', description: '', icon: '' }); dialogVisible.value = true }
const openEdit = (category) => { Object.assign(form, category); dialogVisible.value = true }
const save = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    saving.value = true
    try {
      if (form.id) await request.put('/category/update', form)
      else await request.post('/category/add', form)
      ElMessage.success('分类已保存')
      dialogVisible.value = false
      load()
    } finally { saving.value = false }
  })
}
const removeCategory = async (category) => {
  try {
    await ElMessageBox.confirm(`确定删除分类「${category.name}」吗？`, '删除分类', { type: 'warning' })
    await request.delete(`/category/delete/${category.id}`)
    ElMessage.success('分类已删除')
    load()
  } catch (error) {}
}
onMounted(load)
</script>

<style scoped>
.category-stats { display: flex; align-items: center; gap: 30px; margin-bottom: 22px; padding: 17px 22px; border: 1px solid var(--line); background: rgba(255,250,244,.65); border-radius: 16px; }
.category-stats > div { display: flex; align-items: baseline; gap: 6px; white-space: nowrap; }
.category-stats span { color: var(--ink-muted); font-size: 8px; letter-spacing: .08em; }
.category-stats strong { font-family: var(--font-display); font-size: 30px; font-weight: 500; }
.category-stats small { color: var(--ink-muted); font-size: 8px; }
.category-stats p { margin: 0; color: var(--ink-muted); font-size: 8px; line-height: 1.7; border-left: 1px solid var(--line); padding-left: 25px; }
.category-admin-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; min-height: 240px; }
.category-admin-card { min-height: 235px; border-radius: 20px; border: 1px solid var(--line); padding: 20px 21px 0; background: rgba(255,250,244,.8); display: flex; flex-direction: column; position: relative; overflow: hidden; transition: .3s; }
.category-admin-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-sm); }
.category-admin-card::before { content: ''; position: absolute; width: 130px; height: 130px; border-radius: 50%; right: -55px; top: -65px; opacity: .32; }
.palette-0::before { background: #efd7d5; } .palette-1::before { background: #e8d7bd; } .palette-2::before { background: #dce5d6; } .palette-3::before { background: #dddde5; }
.category-card-head { display: flex; justify-content: space-between; align-items: flex-start; position: relative; z-index: 2; }
.category-symbol { width: 48px; height: 48px; border-radius: 15px; display: grid; place-items: center; background: var(--paper-deep); color: var(--rose-deep); font-family: var(--font-display); font-size: 24px; }
.palette-1 .category-symbol { background: #f4ead8; color: #96743d; }
.palette-2 .category-symbol { background: var(--sage-pale); color: #67775f; }
.palette-3 .category-symbol { background: #e9e7ec; color: #6e6877; }
.category-number { color: var(--ink-muted); font-family: var(--font-display); font-size: 14px; }
.category-card-copy { margin-top: 21px; flex: 1; }
.category-card-copy h3 { font-family: var(--font-display); font-size: 27px; font-weight: 600; margin: 0 0 7px; }
.category-card-copy p { color: var(--ink-soft); font-size: 9px; line-height: 1.7; margin: 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.category-card-foot { border-top: 1px solid var(--line); min-height: 47px; display: flex; align-items: center; justify-content: space-between; margin-top: 15px; }
.category-card-foot > span { display: flex; align-items: center; gap: 5px; color: var(--ink-muted); font-size: 8px; }
.category-card-foot > div { display: flex; gap: 3px; }
.category-card-foot button { border: 0; background: none; color: var(--ink-soft); cursor: pointer; font-size: 8px; padding: 6px; display: flex; align-items: center; gap: 3px; }
.category-card-foot button.danger { color: var(--ink-muted); }
.category-add-card { min-height: 235px; border-radius: 20px; border: 1px dashed rgba(67,47,41,.2); background: rgba(255,250,244,.27); display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: pointer; color: var(--ink-soft); transition: .25s; }
.category-add-card:hover { border-color: var(--rose); background: rgba(255,250,244,.65); }
.category-add-card > span { width: 46px; height: 46px; border-radius: 50%; background: var(--paper-deep); display: grid; place-items: center; color: var(--rose-deep); font-size: 19px; margin-bottom: 12px; }
.category-add-card strong { font-size: 11px; }
.category-add-card p { color: var(--ink-muted); font-size: 8px; margin: 6px 0 0; }
@media (max-width: 1050px) { .category-admin-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 650px) { .category-admin-grid { grid-template-columns: 1fr; } .category-stats p { display: none; } }
</style>