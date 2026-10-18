<template>
  <div>
    <AdminPageHeader eyebrow="CUSTOMERS" title="用户管理" subtitle="查看兔南会员资料，维护每一位顾客的账户。" />

    <div class="user-summary">
      <div><el-icon><User /></el-icon><span>注册用户</span><strong>{{ total }}</strong></div>
      <div><el-icon><UserFilled /></el-icon><span>今日活跃</span><strong>{{ Math.max(1, Math.round(total * .6)) }}</strong></div>
      <div><el-icon><Present /></el-icon><span>本月新增</span><strong>12</strong></div>
      <p>提示：用户默认密码为 <code>123456</code>，可在编辑时重置。</p>
    </div>

    <div class="admin-card">
      <div class="admin-toolbar">
        <div class="admin-toolbar-left">
          <el-input v-model="keyword" class="admin-search" placeholder="搜索昵称或账号" clearable @keyup.enter="search" @clear="search">
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
          <el-button @click="search"><el-icon><Search /></el-icon> 查询</el-button>
        </div>
        <div class="admin-toolbar-right">
          <el-button type="primary" @click="openCreate"><el-icon><Plus /></el-icon> 新增用户</el-button>
        </div>
      </div>
      <div class="admin-table-wrap">
        <el-table :data="rows" style="width: 100%" v-loading="loading">
          <el-table-column label="用户" min-width="190">
            <template #default="{ row }">
              <div class="table-product">
                <span class="user-avatar"><img v-if="row.avatar" :src="row.avatar" alt="" /><i v-else>{{ row.name.slice(0,1) }}</i></span>
                <div><strong>{{ row.name }}</strong><span>@{{ row.username }}</span></div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="角色" width="100"><template #default="{ row }"><el-tag type="info" effect="plain">{{ row.role }}</el-tag></template></el-table-column>
          <el-table-column label="注册时间" prop="createdAt" width="120" />
          <el-table-column label="账户状态" width="110"><template #default><span class="active-dot"><i></i>正常</span></template></el-table-column>
          <el-table-column label="操作" width="160" align="center">
            <template #default="{ row }">
              <div class="table-actions">
                <el-button size="small" @click="openEdit(row)"><el-icon><Edit /></el-icon> 编辑</el-button>
                <el-button size="small" type="danger" plain @click="removeUser(row)"><el-icon><Delete /></el-icon></el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="table-footer">
        <span>共 {{ total }} 位用户</span>
        <el-pagination background layout="prev, pager, next" :page-size="pageSize" :current-page="pageNum" :total="total" @current-change="changePage" />
      </div>
    </div>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑用户' : '新增用户'" width="480px" :close-on-click-modal="false">
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="账号" prop="username"><el-input v-model="form.username" :disabled="!!form.id" placeholder="请输入登录账号" /></el-form-item>
        <el-form-item label="昵称" prop="name"><el-input v-model="form.name" placeholder="请输入用户昵称" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" type="password" show-password :placeholder="form.id ? '不修改请留空' : '默认 123456'" /></el-form-item>
        <el-form-item label="头像">
          <el-upload class="avatar-upload-admin" :action="uploadUrl" :headers="uploadHeaders" :show-file-list="false" :on-success="handleAvatarSuccess">
            <span class="admin-avatar-preview"><img v-if="form.avatar" :src="form.avatar" alt="" /><el-icon v-else><Plus /></el-icon></span>
            <span class="upload-hint">上传用户头像</span>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" :loading="saving" @click="save">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AdminPageHeader from '../../components/AdminPageHeader.vue'
import request from '../../utils/request'
import { authState } from '../../utils/auth'

const rows = ref([])
const total = ref(0)
const pageNum = ref(1)
const pageSize = ref(8)
const keyword = ref('')
const loading = ref(true)
const dialogVisible = ref(false)
const saving = ref(false)
const formRef = ref()
const form = reactive({ id: null, username: '', name: '', password: '', avatar: '' })
const rules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入昵称', trigger: 'blur' }]
}
const uploadUrl = '/api/files/upload'
const uploadHeaders = { Authorization: `Bearer ${authState.token}` }

const load = async () => {
  loading.value = true
  try {
    const res = await request.get('/user/selectPage', { params: { pageNum: pageNum.value, pageSize: pageSize.value, name: keyword.value } })
    rows.value = res.data?.list || []
    total.value = res.data?.total || 0
  } finally { loading.value = false }
}
const search = () => { pageNum.value = 1; load() }
const changePage = (page) => { pageNum.value = page; load() }
const openCreate = () => { Object.assign(form, { id: null, username: '', name: '', password: '', avatar: '' }); dialogVisible.value = true }
const openEdit = (row) => { Object.assign(form, { ...row, password: '' }); dialogVisible.value = true }
const handleAvatarSuccess = (res) => { if (res.code === '200') form.avatar = res.data }
const save = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    saving.value = true
    try {
      if (form.id) await request.put('/user/update', form)
      else await request.post('/user/add', form)
      ElMessage.success('操作成功')
      dialogVisible.value = false
      load()
    } finally { saving.value = false }
  })
}
const removeUser = async (row) => {
  try {
    await ElMessageBox.confirm(`确定删除用户「${row.name}」吗？相关地址与订单将无法恢复。`, '删除用户', { type: 'warning' })
    await request.delete(`/user/delete/${row.id}`)
    ElMessage.success('用户已删除')
    load()
  } catch (error) {}
}
onMounted(load)
</script>

<style scoped>
.user-summary { display: grid; grid-template-columns: repeat(3, 150px) 1fr; gap: 10px; margin-bottom: 18px; }
.user-summary > div { background: rgba(255,250,244,.75); border: 1px solid var(--line); border-radius: 14px; padding: 13px 15px; display: grid; grid-template-columns: 24px 1fr auto; align-items: center; gap: 7px; }
.user-summary .el-icon { color: var(--rose); }
.user-summary span { color: var(--ink-muted); font-size: 8px; }
.user-summary strong { font-family: var(--font-display); font-size: 21px; font-weight: 500; }
.user-summary > p { margin: 0; align-self: center; color: var(--ink-muted); font-size: 8px; text-align: right; }
.user-summary code { color: var(--rose-deep); background: var(--rose-pale); border-radius: 4px; padding: 1px 4px; }
.user-avatar { width: 38px; height: 38px; border-radius: 50%; overflow: hidden; background: var(--paper-deep); display: grid; place-items: center; flex: 0 0 auto; }
.user-avatar img { width: 100%; height: 100%; object-fit: cover; }
.user-avatar i { color: var(--rose-deep); font-family: var(--font-display); font-style: normal; font-size: 17px; }
.active-dot { display: flex; align-items: center; gap: 5px; color: var(--sage); font-size: 9px; }
.active-dot i { width: 5px; height: 5px; border-radius: 50%; background: var(--sage); }
.table-footer { display: flex; justify-content: space-between; align-items: center; padding: 15px 22px; border-top: 1px solid var(--line); }
.table-footer > span { color: var(--ink-muted); font-size: 8px; }
.avatar-upload-admin { display: flex; align-items: center; gap: 11px; }
.admin-avatar-preview { width: 51px; height: 51px; border-radius: 50%; border: 1px dashed var(--line); display: grid; place-items: center; color: var(--ink-muted); overflow: hidden; background: var(--paper-deep); }
.admin-avatar-preview img { width: 100%; height: 100%; object-fit: cover; }
.upload-hint { color: var(--ink-muted); font-size: 9px; }
@media (max-width: 900px) {
  .user-summary { grid-template-columns: repeat(3, 1fr); }
  .user-summary > p { display: none; }
}
@media (max-width: 600px) {
  .user-summary { grid-template-columns: 1fr 1fr; }
  .user-summary > div:nth-child(3) { display: none; }
  .table-footer { flex-direction: column; gap: 10px; }
}
</style>