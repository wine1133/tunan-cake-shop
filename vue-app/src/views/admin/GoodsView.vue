<template>
  <div>
    <AdminPageHeader eyebrow="CAKE CATALOG" title="蛋糕管理" subtitle="维护在售蛋糕、库存、价格与展示信息。" >
      <el-button type="primary" @click="openCreate"><el-icon><Plus /></el-icon> 上架新蛋糕</el-button>
    </AdminPageHeader>

    <div class="goods-summary">
      <div><span>在售蛋糕</span><strong>{{ total }}</strong><small>款</small></div>
      <div><span>库存紧张</span><strong class="warn">{{ lowStock }}</strong><small>款</small></div>
      <div><span>售罄商品</span><strong>{{ soldOut }}</strong><small>款</small></div>
      <p><el-icon><InfoFilled /></el-icon> 修改库存后，店铺端将实时同步。</p>
    </div>

    <div class="admin-card">
      <div class="admin-toolbar">
        <div class="admin-toolbar-left">
          <el-input v-model="keyword" class="admin-search" placeholder="搜索蛋糕名称" clearable @keyup.enter="search" @clear="search">
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
          <el-select v-model="categoryFilter" placeholder="全部分类" clearable style="width: 150px" @change="search">
            <el-option v-for="item in categories" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
          <el-button @click="search"><el-icon><Search /></el-icon> 查询</el-button>
        </div>
        <div class="admin-toolbar-right">
          <el-button :loading="loading" @click="load"><el-icon><Refresh /></el-icon></el-button>
          <el-button type="primary" @click="openCreate"><el-icon><Plus /></el-icon> 新增</el-button>
        </div>
      </div>
      <div class="admin-table-wrap">
        <el-table :data="rows" style="width: 100%" v-loading="loading">
          <el-table-column label="蛋糕信息" min-width="210">
            <template #default="{ row }">
              <div class="table-product goods-cell">
                <img :src="row.img" :alt="row.name" />
                <div><strong>{{ row.name }}</strong><span>{{ row.unit }} · {{ row.categoryName }}</span></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="售价" width="115">
            <template #default="{ row }"><span class="goods-price">¥{{ money(row.price) }}</span><em class="goods-unit">/{{ row.unit }}</em></template>
          </el-table-column>
          <el-table-column label="库存" width="90" align="center">
            <template #default="{ row }"><span class="stock-pill" :class="{ low: row.num <= 8, zero: row.num === 0 }">{{ row.num === 0 ? '售罄' : row.num }}</span></template>
          </el-table-column>
          <el-table-column label="销量" prop="sales" width="80" align="center" />
          <el-table-column label="评分" width="80" align="center"><template #default="{ row }"><span class="rating-cell">★ {{ row.rating }}</span></template></el-table-column>
          <el-table-column label="描述" prop="description" min-width="180" show-overflow-tooltip />
          <el-table-column label="标签" width="105"><template #default="{ row }"><el-tag v-if="row.tag" type="info" effect="plain">{{ row.tag }}</el-tag><span v-else class="muted">—</span></template></el-table-column>
          <el-table-column label="操作" width="150" align="center">
            <template #default="{ row }">
              <div class="table-actions">
                <el-button size="small" @click="openEdit(row)"><el-icon><Edit /></el-icon></el-button>
                <el-button size="small" type="danger" plain @click="removeGoods(row)"><el-icon><Delete /></el-icon></el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="table-footer">
        <span>共 {{ total }} 款蛋糕</span>
        <el-pagination background layout="prev, pager, next" :page-size="pageSize" :current-page="pageNum" :total="total" @current-change="changePage" />
      </div>
    </div>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑蛋糕' : '上架新蛋糕'" width="760px" :close-on-click-modal="false" top="5vh">
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <div class="form-layout">
          <div class="image-column">
            <label class="field-label">蛋糕图片</label>
            <el-upload class="goods-upload" :action="uploadUrl" :headers="uploadHeaders" :show-file-list="false" :on-success="handleUploadSuccess" accept="image/*">
              <div class="goods-image-preview" :class="{ empty: !form.img }">
                <img v-if="form.img" :src="form.img" alt="" />
                <div v-else><el-icon><Plus /></el-icon><span>上传图片</span></div>
                <div v-if="form.img" class="change-image"><el-icon><Camera /></el-icon> 更换图片</div>
              </div>
            </el-upload>
            <p class="upload-note">建议尺寸 800 × 1000px<br />支持 JPG / PNG / WebP，最大 5MB</p>
          </div>
          <div class="form-column">
            <div class="form-two">
              <el-form-item label="蛋糕名称" prop="name"><el-input v-model="form.name" placeholder="例如：云朵草莓蛋糕" /></el-form-item>
              <el-form-item label="所属分类" prop="categoryId">
                <el-select v-model="form.categoryId" placeholder="选择分类" style="width: 100%">
                  <el-option v-for="item in categories" :key="item.id" :label="item.name" :value="item.id" />
                </el-select>
              </el-form-item>
            </div>
            <el-form-item label="蛋糕描述" prop="description"><el-input v-model="form.description" type="textarea" :rows="3" maxlength="500" show-word-limit placeholder="描述风味、原料与适合的场景" /></el-form-item>
            <div class="form-three">
              <el-form-item label="价格（元）" prop="price"><el-input-number v-model="form.price" :min="0" :precision="2" :step="10" controls-position="right" style="width: 100%" /></el-form-item>
              <el-form-item label="库存" prop="num"><el-input-number v-model="form.num" :min="0" :max="999" controls-position="right" style="width: 100%" /></el-form-item>
              <el-form-item label="规格" prop="unit"><el-input v-model="form.unit" placeholder="6寸" /></el-form-item>
            </div>
            <div class="form-two">
              <el-form-item label="展示标签"><el-input v-model="form.tag" placeholder="例如：人气 TOP1" /></el-form-item>
              <el-form-item label="评分"><el-input-number v-model="form.rating" :min="0" :max="5" :step="0.1" :precision="1" controls-position="right" style="width: 100%" /></el-form-item>
            </div>
          </div>
        </div>
      </el-form>
      <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" :loading="saving" @click="save">{{ form.id ? '保存修改' : '确认上架' }}</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AdminPageHeader from '../../components/AdminPageHeader.vue'
import request from '../../utils/request'
import { authState } from '../../utils/auth'
import { money } from '../../utils/format'

const rows = ref([])
const categories = ref([])
const total = ref(0)
const pageNum = ref(1)
const pageSize = ref(8)
const keyword = ref('')
const categoryFilter = ref(null)
const loading = ref(true)
const dialogVisible = ref(false)
const saving = ref(false)
const formRef = ref()
const form = reactive({ id: null, name: '', description: '', img: '', price: 0, num: 0, unit: '6寸', categoryId: null, tag: '', rating: 4.9, sales: 0 })
const rules = {
  name: [{ required: true, message: '请输入蛋糕名称', trigger: 'blur' }],
  categoryId: [{ required: true, message: '请选择所属分类', trigger: 'change' }],
  description: [{ required: true, message: '请输入蛋糕描述', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  num: [{ required: true, message: '请输入库存', trigger: 'blur' }],
  unit: [{ required: true, message: '请输入规格', trigger: 'blur' }],
  img: [{ required: true, message: '请上传蛋糕图片', trigger: 'change' }]
}
const uploadUrl = '/api/files/upload'
const uploadHeaders = { Authorization: `Bearer ${authState.token}` }
const lowStock = computed(() => rows.value.filter(item => item.num > 0 && item.num <= 8).length)
const soldOut = computed(() => rows.value.filter(item => item.num === 0).length)

const load = async () => {
  loading.value = true
  try {
    const res = await request.get('/goods/selectPage', { params: { pageNum: pageNum.value, pageSize: pageSize.value, name: keyword.value, categoryId: categoryFilter.value || 0 } })
    rows.value = res.data?.list || []
    total.value = res.data?.total || 0
  } finally { loading.value = false }
}
const loadCategories = async () => {
  const res = await request.get('/category/selectAll')
  categories.value = res.data || []
}
const search = () => { pageNum.value = 1; load() }
const changePage = (page) => { pageNum.value = page; load() }
const resetForm = () => Object.assign(form, { id: null, name: '', description: '', img: '', price: 0, num: 0, unit: '6寸', categoryId: null, tag: '', rating: 4.9, sales: 0 })
const openCreate = () => { resetForm(); dialogVisible.value = true }
const openEdit = (row) => { Object.assign(form, { ...row }); dialogVisible.value = true }
const handleUploadSuccess = (res) => {
  if (res.code === '200') {
    form.img = res.data
    ElMessage.success('图片上传成功')
  } else ElMessage.error(res.msg)
}
const save = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    saving.value = true
    try {
      if (form.id) await request.put('/goods/update', form)
      else await request.post('/goods/add', form)
      ElMessage.success(form.id ? '蛋糕信息已更新' : '新蛋糕已上架')
      dialogVisible.value = false
      load()
    } finally { saving.value = false }
  })
}
const removeGoods = async (row) => {
  try {
    await ElMessageBox.confirm(`确定下架并删除「${row.name}」吗？`, '删除蛋糕', { type: 'warning' })
    await request.delete(`/goods/delete/${row.id}`)
    ElMessage.success('蛋糕已删除')
    load()
  } catch (error) {}
}
onMounted(() => { loadCategories(); load() })
</script>

<style scoped>
.goods-summary { display: grid; grid-template-columns: repeat(3, 150px) 1fr; gap: 10px; margin-bottom: 18px; }
.goods-summary > div { background: rgba(255,250,244,.75); border: 1px solid var(--line); border-radius: 14px; padding: 13px 15px; display: flex; align-items: baseline; gap: 5px; }
.goods-summary span { color: var(--ink-muted); font-size: 8px; margin-right: auto; }
.goods-summary strong { font-family: var(--font-display); font-size: 24px; font-weight: 500; }
.goods-summary strong.warn { color: #a97935; }
.goods-summary small { color: var(--ink-muted); font-size: 8px; }
.goods-summary p { margin: 0; align-self: center; text-align: right; color: var(--ink-muted); font-size: 8px; display: flex; justify-content: flex-end; gap: 5px; }
.goods-cell img { width: 54px; height: 54px; }
.goods-price { font-family: var(--font-display); font-size: 18px; font-weight: 600; }
.goods-unit { color: var(--ink-muted); font-size: 7px; font-style: normal; margin-left: 2px; }
.stock-pill { display: inline-block; padding: 4px 9px; border-radius: 99px; background: var(--sage-pale); color: #5e735a; font-size: 9px; }
.stock-pill.low { background: #f6ead5; color: #9a7338; }
.stock-pill.zero { background: #f6e3e1; color: #a55757; }
.rating-cell { color: var(--gold); font-size: 9px; }
.table-footer { display: flex; justify-content: space-between; align-items: center; padding: 15px 22px; border-top: 1px solid var(--line); }
.table-footer > span { color: var(--ink-muted); font-size: 8px; }
.form-layout { display: grid; grid-template-columns: 210px 1fr; gap: 28px; }
.image-column .field-label { display: block; margin-bottom: 9px; }
.goods-image-preview { width: 210px; height: 250px; border-radius: 17px; overflow: hidden; position: relative; background: var(--paper-deep); border: 1px dashed rgba(67,47,41,.16); cursor: pointer; }
.goods-image-preview img { width: 100%; height: 100%; object-fit: cover; }
.goods-image-preview.empty > div { height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; color: var(--ink-muted); font-size: 9px; }
.goods-image-preview.empty .el-icon { font-size: 26px; }
.change-image { position: absolute; inset: auto 0 0 0; background: rgba(38,24,20,.65); color: white; text-align: center; padding: 9px; font-size: 8px; }
.upload-note { color: var(--ink-muted); font-size: 8px; line-height: 1.7; margin: 10px 0 0; }
.form-two { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-three { display: grid; grid-template-columns: 1.2fr 1fr 1fr; gap: 12px; }
.form-column :deep(.el-form-item) { margin-bottom: 16px; }
@media (max-width: 800px) {
  .goods-summary { grid-template-columns: repeat(3, 1fr); }
  .goods-summary p { display: none; }
  .form-layout { grid-template-columns: 1fr; }
  .goods-image-preview { width: 100%; height: 190px; }
  .form-two, .form-three { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 550px) {
  .goods-summary { grid-template-columns: 1fr 1fr; }
  .goods-summary > div:nth-child(3) { display: none; }
  .form-two, .form-three { grid-template-columns: 1fr; gap: 0; }
  .table-footer { flex-direction: column; gap: 10px; }
}
</style>