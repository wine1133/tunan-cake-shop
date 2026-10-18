<template>
  <div class="account-wrap">
    <div class="container">
      <AccountHeader title="收货地址" subtitle="提前保存常用地址，让每一次预订都更从容。" />
      <div class="address-intro">
        <div class="address-intro-copy">
          <span class="eyebrow">DELIVERY & PICKUP</span>
          <h2>把甜蜜，送到你身边。</h2>
          <p>上海市内支持全程冷链配送。也可选择到店自提，订单完成后我们会与你确认具体时间。</p>
          <div class="intro-tags"><span><el-icon><Van /></el-icon> 同城冷链</span><span><el-icon><Location /></el-icon> 门店自提</span><span><el-icon><Clock /></el-icon> 准时送达</span></div>
        </div>
        <div class="address-count"><span>已保存地址</span><strong>{{ addresses.length }}</strong><small>个</small></div>
      </div>

      <div class="address-section-head">
        <div><h3>我的地址簿</h3><span>ADDRESS BOOK</span></div>
        <button class="btn btn-primary btn-small" @click="openCreate"><el-icon><Plus /></el-icon> 新增地址</button>
      </div>

      <div v-loading="loading" class="address-grid">
        <article v-for="(address, index) in addresses" :key="address.id" class="address-card" :class="{ default: address.isDefault }">
          <div class="address-card-top">
            <span class="address-index">0{{ index + 1 }}</span>
            <span v-if="address.isDefault" class="default-badge">默认地址</span>
            <el-dropdown trigger="click" @command="(cmd) => handleCommand(cmd, address)">
              <button class="more-btn"><el-icon><MoreFilled /></el-icon></button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="default" :disabled="address.isDefault"><el-icon><Select /></el-icon>设为默认</el-dropdown-item>
                  <el-dropdown-item command="edit"><el-icon><Edit /></el-icon>编辑地址</el-dropdown-item>
                  <el-dropdown-item command="delete" divided><el-icon><Delete /></el-icon>删除地址</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          <div class="address-person">
            <div class="person-icon">{{ address.name.slice(0, 1) }}</div>
            <div><h3>{{ address.name }}</h3><p>{{ address.phone }}</p></div>
          </div>
          <p class="address-detail"><el-icon><LocationFilled /></el-icon>{{ address.address }}</p>
          <div class="address-actions">
            <button @click="openEdit(address)"><el-icon><Edit /></el-icon> 编辑</button>
            <button class="danger" @click="removeAddress(address)"><el-icon><Delete /></el-icon> 删除</button>
          </div>
        </article>

        <button class="add-address-card" @click="openCreate">
          <span><el-icon><Plus /></el-icon></span>
          <strong>添加新地址</strong>
          <p>为下一次甜蜜做好准备</p>
        </button>
      </div>
    </div>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑收货地址' : '添加收货地址'" width="480px" :close-on-click-modal="false">
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <div class="dialog-grid">
          <el-form-item label="收货人" prop="name"><el-input v-model="form.name" placeholder="请输入姓名" /></el-form-item>
          <el-form-item label="联系方式" prop="phone"><el-input v-model="form.phone" placeholder="请输入手机号" /></el-form-item>
        </div>
        <el-form-item label="详细地址" prop="address"><el-input v-model="form.address" type="textarea" :rows="3" placeholder="省 / 市 / 区 / 街道 / 门牌号" /></el-form-item>
        <el-form-item><el-checkbox v-model="form.isDefault">设为默认收货地址</el-checkbox></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="saveAddress">保存地址</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AccountHeader from '../components/AccountHeader.vue'
import request from '../utils/request'

const addresses = ref([])
const loading = ref(true)
const dialogVisible = ref(false)
const saving = ref(false)
const formRef = ref()
const form = reactive({ id: null, name: '', phone: '', address: '', isDefault: false })
const rules = {
  name: [{ required: true, message: '请输入收货人', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系方式', trigger: 'blur' }, { pattern: /^1\d{10}$/, message: '请输入正确的手机号', trigger: 'blur' }],
  address: [{ required: true, message: '请输入详细地址', trigger: 'blur' }]
}

const load = async () => {
  loading.value = true
  try {
    const res = await request.get('/address/selectAll')
    addresses.value = res.data || []
  } finally {
    loading.value = false
  }
}

const resetForm = () => Object.assign(form, { id: null, name: '', phone: '', address: '', isDefault: false })
const openCreate = () => { resetForm(); dialogVisible.value = true }
const openEdit = (address) => { Object.assign(form, { ...address, isDefault: address.isDefault }); dialogVisible.value = true }

const saveAddress = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    saving.value = true
    try {
      if (form.id) await request.put('/address/update', form)
      else await request.post('/address/add', form)
      ElMessage.success(form.id ? '地址已更新' : '地址已添加')
      dialogVisible.value = false
      load()
    } finally {
      saving.value = false
    }
  })
}

const setDefault = async (address) => {
  await request.put('/address/update', { ...address, isDefault: true, userId: address.userId })
  ElMessage.success('已设为默认地址')
  load()
}

const removeAddress = async (address) => {
  try {
    await ElMessageBox.confirm('删除后将无法恢复，确定删除这个地址吗？', '删除地址', { type: 'warning' })
    await request.delete(`/address/delete/${address.id}`)
    ElMessage.success('地址已删除')
    load()
  } catch (error) {}
}

const handleCommand = (command, address) => {
  if (command === 'default') setDefault(address)
  if (command === 'edit') openEdit(address)
  if (command === 'delete') removeAddress(address)
}

onMounted(load)
</script>

<style scoped>
.address-intro { position: relative; overflow: hidden; display: flex; justify-content: space-between; align-items: center; padding: 36px 42px; border-radius: 26px; background: linear-gradient(120deg, var(--ink), #4a332c); color: #f7ecdf; margin-bottom: 44px; }
.address-intro::after { content: ''; position: absolute; width: 320px; height: 320px; border: 1px solid rgba(218,192,145,.18); border-radius: 50%; right: 65px; top: -155px; }
.address-intro::before { content: ''; position: absolute; width: 200px; height: 200px; border: 1px dashed rgba(218,192,145,.14); border-radius: 50%; right: 125px; top: -95px; }
.address-intro .eyebrow { color: var(--gold-light); }
.address-intro-copy { position: relative; z-index: 2; }
.address-intro h2 { font-family: var(--font-display); font-size: 38px; font-weight: 400; margin: 13px 0 9px; }
.address-intro p { color: rgba(247,236,223,.62); font-size: 10px; line-height: 1.8; max-width: 560px; margin: 0; }
.intro-tags { display: flex; gap: 9px; margin-top: 22px; }
.intro-tags span { display: flex; align-items: center; gap: 5px; border: 1px solid rgba(255,255,255,.12); border-radius: 999px; padding: 7px 11px; color: rgba(247,236,223,.7); font-size: 8px; }
.address-count { position: relative; z-index: 2; text-align: center; padding-left: 50px; margin-right: 15px; }
.address-count span { display: block; color: rgba(247,236,223,.45); font-size: 8px; letter-spacing: .12em; }
.address-count strong { font-family: var(--font-display); font-size: 64px; font-weight: 400; line-height: 1.1; }
.address-count small { font-size: 10px; color: rgba(247,236,223,.45); }
.address-section-head { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 22px; }
.address-section-head h3 { font-family: var(--font-display); font-size: 28px; font-weight: 600; margin: 0 0 2px; }
.address-section-head span { color: var(--ink-muted); font-size: 8px; letter-spacing: .18em; }
.address-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; min-height: 240px; }
.address-card { background: rgba(255,250,244,.8); border: 1px solid var(--line); border-radius: 21px; padding: 21px 22px 17px; transition: .3s; }
.address-card:hover { box-shadow: var(--shadow-sm); transform: translateY(-2px); }
.address-card.default { border-color: rgba(140,74,85,.28); background: linear-gradient(135deg, #fffaf4, #f9efeb); }
.address-card-top { display: flex; align-items: center; justify-content: space-between; min-height: 24px; }
.address-index { color: var(--ink-muted); font-family: var(--font-display); font-size: 14px; }
.default-badge { margin-left: auto; background: var(--rose-pale); color: var(--rose-deep); border-radius: 999px; padding: 5px 9px; font-size: 8px; }
.more-btn { border: 0; background: none; color: var(--ink-muted); margin-left: 8px; cursor: pointer; }
.address-person { display: flex; align-items: center; gap: 12px; margin: 15px 0 16px; }
.person-icon { width: 42px; height: 42px; border-radius: 50%; background: var(--paper-deep); color: var(--rose-deep); display: grid; place-items: center; font-family: var(--font-display); font-size: 20px; }
.address-person h3 { font-size: 13px; margin: 0 0 4px; }
.address-person p { color: var(--ink-muted); font-size: 9px; margin: 0; }
.address-detail { min-height: 37px; color: var(--ink-soft); font-size: 10px; line-height: 1.65; margin: 0 0 14px; display: flex; gap: 6px; }
.address-detail .el-icon { color: var(--rose); margin-top: 3px; flex: 0 0 auto; }
.address-actions { display: flex; gap: 6px; border-top: 1px solid var(--line); padding-top: 12px; }
.address-actions button { border: 0; background: none; color: var(--ink-soft); font-size: 9px; cursor: pointer; display: flex; align-items: center; gap: 4px; padding: 5px 8px 5px 0; }
.address-actions button.danger { margin-left: auto; color: var(--ink-muted); }
.add-address-card { min-height: 258px; border: 1px dashed rgba(67,47,41,.2); border-radius: 21px; background: rgba(255,250,244,.3); display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: pointer; color: var(--ink-soft); transition: .25s; }
.add-address-card:hover { border-color: var(--rose); background: rgba(255,250,244,.65); }
.add-address-card > span { width: 46px; height: 46px; border-radius: 50%; background: var(--paper-deep); color: var(--rose-deep); display: grid; place-items: center; font-size: 19px; margin-bottom: 12px; }
.add-address-card strong { font-size: 11px; }
.add-address-card p { color: var(--ink-muted); font-size: 8px; margin: 6px 0 0; }
.dialog-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
@media (max-width: 700px) {
  .address-intro { padding: 28px; }
  .address-count { display: none; }
  .address-intro h2 { font-size: 31px; }
  .intro-tags { flex-wrap: wrap; }
  .address-grid { grid-template-columns: 1fr; }
  .dialog-grid { grid-template-columns: 1fr; gap: 0; }
}
</style>