<template>
  <div class="auth-page">
    <div class="auth-visual">
      <img src="/images/hero-cake.jpg" alt="手作蛋糕" />
      <div class="auth-visual-shade"></div>
      <div class="auth-visual-top">
        <router-link to="/" class="auth-brand"><BrandMark /></router-link>
        <router-link to="/" class="back-link"><el-icon><Back /></el-icon> 返回首页</router-link>
      </div>
      <div class="auth-quote">
        <span class="quote-line"></span>
        <p>“把日常过成值得纪念的日子，<br />从一份认真做的甜开始。”</p>
        <span class="quote-by">兔南 · 主理人手记</span>
      </div>
      <div class="auth-visual-bottom">
        <span>SHANGHAI · EST. 2014</span>
        <span>FRESHLY BAKED DAILY</span>
      </div>
    </div>

    <div class="auth-panel">
      <div class="auth-panel-inner">
        <div class="mobile-brand"><BrandMark /></div>
        <span class="eyebrow">{{ tab === 'login' ? 'WELCOME BACK' : 'JOIN TU NAN' }}</span>
        <h1>{{ tab === 'login' ? '欢迎回来，' : '开启一段甜蜜，' }}<em>{{ tab === 'login' ? '甜蜜如初。' : '从这里开始。' }}</em></h1>
        <p class="auth-sub">{{ tab === 'login' ? '登录你的兔南账户，查看订单与专属心意。' : '创建账户，收藏你喜欢的每一份甜。' }}</p>

        <div class="auth-tabs">
          <button :class="{ active: tab === 'login' }" @click="switchTab('login')">登录</button>
          <button :class="{ active: tab === 'register' }" @click="switchTab('register')">注册</button>
        </div>

        <el-form v-if="tab === 'login'" ref="loginFormRef" :model="loginForm" :rules="loginRules" label-position="top" @submit.prevent="submitLogin">
          <div class="role-switch">
            <button :class="{ active: loginForm.role === '用户' }" type="button" @click="loginForm.role = '用户'"><el-icon><User /></el-icon>顾客登录</button>
            <button :class="{ active: loginForm.role === '管理员' }" type="button" @click="loginForm.role = '管理员'"><el-icon><Setting /></el-icon>管理后台</button>
          </div>
          <el-form-item label="账号" prop="username">
            <el-input v-model="loginForm.username" size="large" placeholder="请输入账号" :prefix-icon="User" autocomplete="username" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="loginForm.password" size="large" type="password" show-password placeholder="请输入密码" :prefix-icon="Lock" autocomplete="current-password" @keyup.enter="submitLogin" />
          </el-form-item>
          <div class="form-row">
            <el-checkbox v-model="remember">记住我</el-checkbox>
            <a href="#" @click.prevent>忘记密码？</a>
          </div>
          <el-button type="primary" size="large" class="auth-submit" :loading="loading" @click="submitLogin">
            登录兔南账户 <el-icon v-if="!loading"><ArrowRight /></el-icon>
          </el-button>
          <div class="demo-box">
            <div><span>体验账号</span><small>已为你准备好</small></div>
            <button type="button" @click="fillDemo('user')">顾客 demo</button>
            <button type="button" @click="fillDemo('admin')">管理员 demo</button>
          </div>
        </el-form>

        <el-form v-else ref="registerFormRef" :model="registerForm" :rules="registerRules" label-position="top" @submit.prevent="submitRegister">
          <el-form-item label="怎么称呼你" prop="name">
            <el-input v-model="registerForm.name" size="large" placeholder="例如：林小满" :prefix-icon="User" />
          </el-form-item>
          <el-form-item label="账号" prop="username">
            <el-input v-model="registerForm.username" size="large" placeholder="2-30 位字符" :prefix-icon="Postcard" autocomplete="username" />
          </el-form-item>
          <el-form-item label="设置密码" prop="password">
            <el-input v-model="registerForm.password" size="large" type="password" show-password placeholder="至少 6 位" :prefix-icon="Lock" autocomplete="new-password" />
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input v-model="registerForm.confirmPassword" size="large" type="password" show-password placeholder="请再次输入密码" :prefix-icon="Lock" autocomplete="new-password" @keyup.enter="submitRegister" />
          </el-form-item>
          <el-checkbox v-model="agreed" class="agreement">我已阅读并同意《用户服务协议》和《隐私政策》</el-checkbox>
          <el-button type="primary" size="large" class="auth-submit" :loading="loading" @click="submitRegister">
            创建我的账户 <el-icon v-if="!loading"><ArrowRight /></el-icon>
          </el-button>
        </el-form>

        <p class="switch-hint">
          {{ tab === 'login' ? '还没有兔南账户？' : '已经有账户了？' }}
          <button @click="switchTab(tab === 'login' ? 'register' : 'login')">{{ tab === 'login' ? '立即注册' : '直接登录' }}</button>
        </p>
        <p class="auth-footer">© 2026 兔南蛋糕零售店 · 让每一天都有一点甜</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Postcard } from '@element-plus/icons-vue'
import BrandMark from '../components/BrandMark.vue'
import request from '../utils/request'
import { setAuth } from '../utils/auth'

const route = useRoute()
const router = useRouter()
const tab = ref(route.query.tab === 'register' ? 'register' : 'login')
const loading = ref(false)
const remember = ref(true)
const agreed = ref(false)
const loginFormRef = ref()
const registerFormRef = ref()

const loginForm = reactive({ username: '', password: '', role: '用户' })
const registerForm = reactive({ name: '', username: '', password: '', confirmPassword: '' })

const loginRules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}
const validateConfirm = (rule, value, callback) => {
  if (!value) callback(new Error('请再次输入密码'))
  else if (value !== registerForm.password) callback(new Error('两次输入的密码不一致'))
  else callback()
}
const registerRules = {
  name: [{ required: true, message: '请告诉我们怎么称呼你', trigger: 'blur' }],
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }, { min: 2, max: 30, message: '账号长度需为 2-30 位', trigger: 'blur' }],
  password: [{ required: true, message: '请设置密码', trigger: 'blur' }, { min: 6, message: '密码至少 6 位', trigger: 'blur' }],
  confirmPassword: [{ validator: validateConfirm, trigger: 'blur' }]
}

const switchTab = (value) => {
  tab.value = value
  router.replace({ query: value === 'register' ? { tab: 'register' } : {} })
}

const fillDemo = (type) => {
  loginForm.role = type === 'admin' ? '管理员' : '用户'
  loginForm.username = type === 'admin' ? 'admin' : 'user'
  loginForm.password = type === 'admin' ? 'admin123' : 'user123'
}

const finishLogin = (payload) => {
  setAuth(payload)
  ElMessage.success(`欢迎回来，${payload.name}`)
  const redirect = route.query.redirect
  if (payload.role === '管理员') router.push('/admin')
  else router.push(typeof redirect === 'string' ? redirect : '/')
}

const submitLogin = async () => {
  if (!loginFormRef.value) return
  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      const res = await request.post('/login', loginForm)
      finishLogin(res.data)
    } finally {
      loading.value = false
    }
  })
}

const submitRegister = async () => {
  if (!registerFormRef.value) return
  await registerFormRef.value.validate(async (valid) => {
    if (!valid) return
    if (!agreed.value) {
      ElMessage.warning('请先阅读并同意用户服务协议')
      return
    }
    loading.value = true
    try {
      const res = await request.post('/register', {
        name: registerForm.name,
        username: registerForm.username,
        password: registerForm.password
      })
      finishLogin(res.data)
    } finally {
      loading.value = false
    }
  })
}

onMounted(() => {
  if (route.query.tab === 'register') tab.value = 'register'
})
</script>

<style scoped>
.auth-page { min-height: 100vh; display: grid; grid-template-columns: 1.02fr .98fr; background: var(--paper); }
.auth-visual { position: relative; min-height: 100vh; overflow: hidden; }
.auth-visual > img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.auth-visual-shade { position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(37,23,19,.24), rgba(37,23,19,.12) 45%, rgba(37,23,19,.7)); }
.auth-visual-top { position: absolute; z-index: 2; top: 35px; left: 45px; right: 45px; display: flex; justify-content: space-between; align-items: center; }
.auth-brand { text-decoration: none; }
.auth-brand :deep(.brand-mark) { color: white; }
.auth-brand :deep(.brand-cn) { color: rgba(255,255,255,.62); }
.back-link { color: rgba(255,255,255,.75); text-decoration: none; font-size: 10px; letter-spacing: .06em; display: flex; align-items: center; gap: 7px; }
.auth-quote { position: absolute; z-index: 2; left: 55px; right: 55px; bottom: 125px; color: white; }
.quote-line { display: block; width: 44px; height: 1px; background: var(--gold-light); margin-bottom: 22px; }
.auth-quote p { font-family: var(--font-display); font-size: clamp(27px, 2.5vw, 39px); line-height: 1.55; font-weight: 400; margin: 0 0 18px; }
.quote-by { color: rgba(255,255,255,.55); font-size: 9px; letter-spacing: .2em; }
.auth-visual-bottom { position: absolute; z-index: 2; left: 45px; right: 45px; bottom: 30px; display: flex; justify-content: space-between; color: rgba(255,255,255,.38); font-size: 7px; letter-spacing: .2em; }
.auth-panel { display: flex; align-items: center; justify-content: center; padding: 45px 30px; background: radial-gradient(circle at 100% 0, #f7eadf, transparent 34%), var(--paper); }
.auth-panel-inner { width: min(390px, 100%); }
.mobile-brand { display: none; margin-bottom: 42px; }
.auth-panel h1 { font-family: var(--font-display); font-size: clamp(34px, 3.1vw, 45px); font-weight: 500; line-height: 1.08; margin: 17px 0 12px; }
.auth-panel h1 em { display: block; color: var(--rose-deep); font-weight: 400; }
.auth-sub { color: var(--ink-soft); font-size: 11px; line-height: 1.7; margin: 0 0 27px; }
.auth-tabs { display: flex; border-bottom: 1px solid var(--line); margin-bottom: 27px; }
.auth-tabs button { flex: 1; border: 0; background: none; padding: 12px; color: var(--ink-muted); cursor: pointer; font-size: 12px; position: relative; }
.auth-tabs button::after { content: ''; position: absolute; left: 50%; bottom: -1px; width: 0; height: 2px; background: var(--rose-deep); transition: .3s; transform: translateX(-50%); }
.auth-tabs button.active { color: var(--ink); font-weight: 600; }
.auth-tabs button.active::after { width: 40px; }
.role-switch { display: grid; grid-template-columns: 1fr 1fr; background: var(--paper-deep); border-radius: 12px; padding: 4px; margin-bottom: 22px; }
.role-switch button { min-height: 39px; border: 0; border-radius: 9px; background: transparent; color: var(--ink-soft); font-size: 10px; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 6px; transition: .2s; }
.role-switch button.active { background: white; color: var(--ink); box-shadow: 0 3px 10px rgba(65,43,35,.08); font-weight: 600; }
:deep(.el-form-item) { margin-bottom: 18px; }
:deep(.el-form-item__label) { font-size: 10px; color: var(--ink-soft); padding-bottom: 7px; }
:deep(.el-form-item__error) { font-size: 9px; }
.form-row { display: flex; justify-content: space-between; align-items: center; margin: -2px 0 20px; }
.form-row a { color: var(--ink-muted); font-size: 9px; text-decoration: none; }
:deep(.el-checkbox__label) { font-size: 9px; color: var(--ink-soft); }
.auth-submit { width: 100%; min-height: 51px; border-radius: 12px; margin-top: 3px; font-size: 12px; letter-spacing: .08em; }
.demo-box { margin-top: 20px; padding: 12px 13px; border: 1px dashed rgba(97,69,60,.18); border-radius: 12px; display: flex; align-items: center; gap: 8px; background: rgba(247,241,231,.45); }
.demo-box > div { margin-right: auto; }
.demo-box span { display: block; font-size: 9px; font-weight: 600; }
.demo-box small { display: block; color: var(--ink-muted); font-size: 7px; margin-top: 2px; }
.demo-box button { border: 1px solid var(--line); background: white; border-radius: 7px; font-size: 8px; padding: 6px 8px; color: var(--ink-soft); cursor: pointer; white-space: nowrap; }
.demo-box button:hover { border-color: var(--rose); color: var(--rose-deep); }
.agreement { margin: 2px 0 17px; }
.agreement :deep(.el-checkbox__label) { line-height: 1.6; }
.switch-hint { text-align: center; color: var(--ink-muted); font-size: 9px; margin-top: 20px; }
.switch-hint button { border: 0; background: none; color: var(--rose-deep); cursor: pointer; font-size: 9px; font-weight: 600; margin-left: 4px; }
.auth-footer { text-align: center; color: #b4a59d; font-size: 7px; letter-spacing: .08em; margin: 38px 0 0; }
@media (max-width: 900px) {
  .auth-page { grid-template-columns: 1fr; }
  .auth-visual { display: none; }
  .auth-panel { min-height: 100vh; background: radial-gradient(circle at 100% 0, #f4e4d8, transparent 38%), var(--paper); }
  .mobile-brand { display: block; }
}
@media (max-width: 480px) {
  .auth-panel { padding: 30px 22px; align-items: flex-start; }
  .auth-panel-inner { padding-top: 10px; }
  .demo-box { flex-wrap: wrap; }
  .demo-box > div { width: 100%; }
}
</style>