<template>
  <el-dialog v-model="visible" width="880px" class="order-dialog" :show-close="false" destroy-on-close>
    <div v-if="product" class="order-panel">
      <div class="order-visual">
        <img :src="product.img" :alt="product.name" />
        <div class="visual-overlay">
          <span class="visual-tag">{{ product.categoryName }}</span>
          <div>
            <p>TU NAN PÂTISSERIE</p>
            <h2>{{ product.name }}</h2>
          </div>
        </div>
        <button class="dialog-close" @click="visible = false"><el-icon><Close /></el-icon></button>
      </div>
      <div class="order-form">
        <div class="dialog-heading">
          <span class="eyebrow">Reservation</span>
          <h3>预订这份甜蜜</h3>
          <p>{{ product.description }}</p>
        </div>
        <div class="order-facts">
          <div><span>规格</span><strong>{{ product.unit }}</strong></div>
          <div><span>剩余</span><strong>{{ product.num }} 份</strong></div>
          <div><span>评分</span><strong>{{ product.rating }} <em>★</em></strong></div>
        </div>
        <div class="form-section">
          <div class="section-label"><span>01</span>选择收货地址</div>
          <div v-if="addresses.length" class="address-options">
            <button v-for="address in addresses" :key="address.id" class="address-option" :class="{ selected: selectedAddress === address.id }" @click="selectedAddress = address.id">
              <span class="radio"></span>
              <span><strong>{{ address.name }} · {{ address.phone }}</strong><em>{{ address.address }}</em></span>
              <span v-if="address.isDefault" class="default-tag">默认</span>
            </button>
          </div>
          <div v-else class="no-address">
            <p>还没有收货地址，先添加一个吧</p>
            <button class="text-link" @click="goAddresses">前往添加 <el-icon><Right /></el-icon></button>
          </div>
        </div>
        <div class="form-section quantity-row">
          <div class="section-label"><span>02</span>选择数量</div>
          <el-input-number v-model="quantity" :min="1" :max="Math.min(product.num, 9)" controls-position="right" />
        </div>
        <div class="order-summary">
          <div><span>甜蜜小计</span><strong>¥{{ money(product.price * quantity) }}</strong></div>
          <small>新鲜手作 · 下单后 24 小时内确认</small>
        </div>
        <button class="btn btn-primary full submit-order" :disabled="!selectedAddress || submitting" @click="submitOrder">
          <el-icon v-if="submitting" class="is-loading"><Loading /></el-icon>
          <el-icon v-else><ShoppingBag /></el-icon>
          {{ submitting ? '正在确认...' : '确认预订' }}
        </button>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../utils/request'
import { money } from '../utils/format'

const emit = defineEmits(['ordered'])
const router = useRouter()
const visible = ref(false)
const product = ref(null)
const addresses = ref([])
const selectedAddress = ref(null)
const quantity = ref(1)
const submitting = ref(false)

const open = async (item) => {
  product.value = item
  quantity.value = 1
  selectedAddress.value = null
  addresses.value = []
  visible.value = true
  try {
    const res = await request.get('/address/selectAll')
    addresses.value = res.data || []
    const preferred = addresses.value.find((item) => item.isDefault) || addresses.value[0]
    selectedAddress.value = preferred?.id || null
  } catch (error) {}
}

defineExpose({ open })

const goAddresses = () => {
  visible.value = false
  router.push('/addresses')
}

const submitOrder = async () => {
  if (!selectedAddress.value) return
  submitting.value = true
  try {
    await request.post('/orders/add', {
      goodsId: product.value.id,
      addressId: selectedAddress.value,
      num: quantity.value
    })
    ElMessage.success('预订成功，甜蜜正在准备中')
    visible.value = false
    emit('ordered')
    router.push('/orders')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.order-panel { display: grid; grid-template-columns: .9fr 1.1fr; min-height: 590px; }
.order-visual { position: relative; border-radius: 20px; overflow: hidden; min-height: 500px; }
.order-visual img { width: 100%; height: 100%; object-fit: cover; position: absolute; inset: 0; }
.order-visual::after { content: ''; position: absolute; inset: 0; background: linear-gradient(to top, rgba(36,23,20,.7), transparent 55%); }
.visual-overlay { position: absolute; z-index: 2; left: 30px; right: 30px; bottom: 32px; color: white; }
.visual-overlay p { margin: 0 0 9px; font-size: 8px; letter-spacing: .25em; opacity: .7; }
.visual-overlay h2 { font-family: var(--font-display); font-size: 35px; margin: 0; font-weight: 500; }
.visual-tag { display: inline-block; padding: 7px 10px; border-radius: 999px; background: rgba(255,255,255,.17); backdrop-filter: blur(8px); font-size: 9px; margin-bottom: 16px; }
.dialog-close { position: absolute; z-index: 3; top: 17px; right: 17px; width: 34px; height: 34px; border-radius: 50%; border: 0; background: rgba(255,250,244,.9); color: var(--ink); cursor: pointer; }
.order-form { padding: 14px 14px 8px 38px; }
.dialog-heading h3 { font-family: var(--font-display); font-size: 42px; font-weight: 500; margin: 8px 0 8px; line-height: 1; }
.dialog-heading p { color: var(--ink-soft); font-size: 11px; line-height: 1.8; margin: 0 0 20px; }
.order-facts { display: grid; grid-template-columns: repeat(3, 1fr); background: var(--paper-deep); border-radius: 14px; padding: 13px 15px; margin-bottom: 20px; }
.order-facts div { display: flex; flex-direction: column; gap: 4px; }
.order-facts span { font-size: 9px; color: var(--ink-muted); }
.order-facts strong { font-size: 12px; }
.order-facts em { color: var(--gold); font-style: normal; }
.form-section { margin-bottom: 18px; }
.section-label { color: var(--ink-soft); font-size: 10px; font-weight: 600; letter-spacing: .08em; margin-bottom: 10px; }
.section-label span { color: var(--rose); margin-right: 7px; font-family: var(--font-display); font-size: 13px; }
.address-options { display: flex; flex-direction: column; gap: 7px; max-height: 142px; overflow: auto; padding-right: 3px; }
.address-option { display: flex; align-items: center; text-align: left; gap: 10px; padding: 11px; border-radius: 12px; border: 1px solid var(--line); background: rgba(255,255,255,.55); cursor: pointer; color: var(--ink); }
.address-option.selected { border-color: rgba(140,74,85,.55); background: var(--rose-pale); }
.radio { width: 15px; height: 15px; border-radius: 50%; border: 1px solid #b8a89f; flex: 0 0 auto; }
.address-option.selected .radio { border: 4px solid var(--rose-deep); }
.address-option strong { display: block; font-size: 10px; margin-bottom: 3px; }
.address-option em { display: block; font-style: normal; color: var(--ink-soft); font-size: 9px; line-height: 1.4; }
.default-tag { margin-left: auto; background: var(--ink); color: white; border-radius: 999px; padding: 3px 7px; font-size: 8px; }
.no-address { padding: 15px; border: 1px dashed var(--line); border-radius: 14px; }
.no-address p { margin: 0 0 10px; color: var(--ink-muted); font-size: 10px; }
.no-address .text-link { background: none; border: 0; border-bottom: 1px solid; cursor: pointer; padding: 0 0 4px; }
.quantity-row { display: flex; align-items: center; justify-content: space-between; }
.quantity-row .section-label { margin: 0; }
:deep(.el-input-number) { width: 120px; }
.order-summary { border-top: 1px solid var(--line); padding-top: 14px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.order-summary div { display: flex; flex-direction: column; gap: 4px; }
.order-summary span { color: var(--ink-muted); font-size: 9px; }
.order-summary strong { font-family: var(--font-display); font-size: 28px; }
.order-summary small { color: var(--ink-muted); font-size: 8px; }
.submit-order { min-height: 51px; }
@media (max-width: 820px) {
  .order-panel { grid-template-columns: 1fr; }
  .order-visual { min-height: 260px; }
  .order-form { padding: 26px 6px 5px; }
}
</style>