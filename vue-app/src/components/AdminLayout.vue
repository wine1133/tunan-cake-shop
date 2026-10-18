<template>
  <div class="admin-shell">
    <aside class="admin-sidebar">
      <div class="sidebar-top">
        <router-link to="/admin" class="admin-brand"><BrandMark /></router-link>
        <span class="admin-label">MANAGEMENT</span>
      </div>
      <nav class="admin-nav">
        <span class="nav-section">工作台</span>
        <router-link to="/admin" end><el-icon><DataLine /></el-icon><span>数据总览</span></router-link>
        <span class="nav-section">店铺管理</span>
        <router-link to="/admin/goods"><el-icon><Dish /></el-icon><span>蛋糕管理</span></router-link>
        <router-link to="/admin/categories"><el-icon><CollectionTag /></el-icon><span>分类管理</span></router-link>
        <router-link to="/admin/orders"><el-icon><Tickets /></el-icon><span>订单管理</span><em v-if="pendingCount">{{ pendingCount }}</em></router-link>
        <router-link to="/admin/users"><el-icon><User /></el-icon><span>用户管理</span></router-link>
        <router-link to="/admin/addresses"><el-icon><Location /></el-icon><span>收货地址</span></router-link>
        <router-link to="/admin/notices"><el-icon><Bell /></el-icon><span>系统公告</span></router-link>
      </nav>
      <div class="sidebar-bottom">
        <router-link to="/" class="store-link"><el-icon><Back /></el-icon><span>返回店铺首页</span></router-link>
        <div class="sidebar-user">
          <span class="sidebar-avatar">{{ avatarText(authState.user?.name) }}</span>
          <div><strong>{{ authState.user?.name }}</strong><span>{{ authState.user?.role }}</span></div>
          <el-dropdown trigger="click" @command="handleCommand">
            <button class="user-more"><el-icon><MoreFilled /></el-icon></button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="store"><el-icon><Shop /></el-icon>返回店铺</el-dropdown-item>
                <el-dropdown-item command="logout" divided><el-icon><SwitchButton /></el-icon>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </aside>

    <div class="admin-main">
      <header class="admin-topbar">
        <div class="topbar-left">
          <button class="mobile-menu-btn" @click="mobileOpen = true"><el-icon><Menu /></el-icon></button>
          <div class="breadcrumb"><span>TU NAN</span><el-icon><ArrowRight /></el-icon><strong>{{ currentTitle }}</strong></div>
        </div>
        <div class="topbar-right">
          <span class="today"><el-icon><Calendar /></el-icon>{{ today }}</span>
          <button class="topbar-icon" @click="goNotices"><el-icon><Bell /></el-icon><i v-if="pendingCount"></i></button>
          <div class="topbar-avatar">{{ avatarText(authState.user?.name) }}</div>
        </div>
      </header>
      <main class="admin-content"><router-view /></main>
    </div>

    <el-drawer v-model="mobileOpen" direction="ltr" size="78%" :with-header="false" class="admin-mobile-drawer">
      <div class="mobile-admin-inner">
        <BrandMark />
        <nav @click="mobileOpen = false">
          <router-link to="/admin" end><el-icon><DataLine /></el-icon>数据总览</router-link>
          <router-link to="/admin/goods"><el-icon><Dish /></el-icon>蛋糕管理</router-link>
          <router-link to="/admin/categories"><el-icon><CollectionTag /></el-icon>分类管理</router-link>
          <router-link to="/admin/orders"><el-icon><Tickets /></el-icon>订单管理</router-link>
          <router-link to="/admin/users"><el-icon><User /></el-icon>用户管理</router-link>
          <router-link to="/admin/addresses"><el-icon><Location /></el-icon>收货地址</router-link>
          <router-link to="/admin/notices"><el-icon><Bell /></el-icon>系统公告</router-link>
          <router-link to="/"><el-icon><Shop /></el-icon>返回店铺</router-link>
        </nav>
        <button class="btn btn-outline full" @click="handleCommand('logout')">退出登录</button>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BrandMark from './BrandMark.vue'
import { authState, logout } from '../utils/auth'
import { avatarText } from '../utils/format'
import request from '../utils/request'

const route = useRoute()
const router = useRouter()
const mobileOpen = ref(false)
const pendingCount = ref(0)
const titles = {
  'admin-dashboard': '数据总览',
  'admin-goods': '蛋糕管理',
  'admin-categories': '分类管理',
  'admin-orders': '订单管理',
  'admin-users': '用户管理',
  'admin-addresses': '收货地址',
  'admin-notices': '系统公告'
}
const currentTitle = computed(() => titles[route.name] || '管理中心')
const today = new Date().toLocaleDateString('zh-CN', { month: 'long', day: 'numeric', weekday: 'long' })

const loadPending = async () => {
  try {
    const res = await request.get('/orders/selectPage', { params: { status: '待制作', pageNum: 1, pageSize: 50 } })
    pendingCount.value = res.data?.total || 0
  } catch (error) {}
}

const handleCommand = (command) => {
  if (command === 'store') router.push('/')
  if (command === 'logout') {
    logout()
    router.push('/login')
  }
}
const goNotices = () => router.push('/admin/notices')
onMounted(loadPending)
</script>

<style scoped>
.admin-shell { min-height: 100vh; background: #f4ede3; display: flex; }
.admin-sidebar { width: 238px; flex: 0 0 238px; background: linear-gradient(165deg, #30211d, #3d2923); color: #e7dacb; min-height: 100vh; position: sticky; top: 0; height: 100vh; display: flex; flex-direction: column; padding: 27px 16px 18px; }
.sidebar-top { padding: 0 12px 30px; }
.admin-brand { text-decoration: none; }
.admin-brand :deep(.brand-mark) { color: #f3e6d5; }
.admin-brand :deep(.brand-cn) { color: rgba(243,230,213,.42); }
.admin-label { display: block; margin-top: 22px; color: rgba(231,218,203,.3); font-size: 7px; letter-spacing: .28em; }
.admin-nav { display: flex; flex-direction: column; gap: 3px; }
.nav-section { display: block; margin: 19px 12px 8px; color: rgba(231,218,203,.28); font-size: 7px; letter-spacing: .2em; }
.admin-nav a { min-height: 45px; border-radius: 11px; color: rgba(231,218,203,.62); text-decoration: none; display: flex; align-items: center; gap: 11px; padding: 0 13px; font-size: 11px; transition: .22s; position: relative; }
.admin-nav a .el-icon { font-size: 17px; }
.admin-nav a:hover { color: #fff3e4; background: rgba(255,255,255,.05); }
.admin-nav a.router-link-active { background: rgba(217,194,142,.12); color: #f7e9d6; }
.admin-nav a.router-link-active::before { content: ''; position: absolute; left: -16px; width: 2px; height: 22px; border-radius: 0 2px 2px 0; background: var(--gold-light); }
.admin-nav a em { margin-left: auto; background: var(--rose); color: white; border-radius: 999px; min-width: 18px; height: 18px; padding: 0 5px; display: grid; place-items: center; font-size: 8px; font-style: normal; }
.sidebar-bottom { margin-top: auto; }
.store-link { display: flex; align-items: center; gap: 8px; color: rgba(231,218,203,.4); text-decoration: none; font-size: 9px; padding: 12px 13px; border-top: 1px solid rgba(255,255,255,.07); margin-bottom: 11px; }
.store-link:hover { color: #f7e9d6; }
.sidebar-user { background: rgba(255,255,255,.055); border: 1px solid rgba(255,255,255,.07); border-radius: 13px; padding: 10px; display: flex; align-items: center; gap: 9px; }
.sidebar-avatar { width: 33px; height: 33px; border-radius: 50%; background: var(--rose-pale); color: var(--rose-deep); display: grid; place-items: center; font-family: var(--font-display); font-size: 15px; }
.sidebar-user div { min-width: 0; }
.sidebar-user strong { display: block; font-size: 9px; color: #f7e9d6; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sidebar-user div span { color: rgba(231,218,203,.35); font-size: 7px; }
.user-more { margin-left: auto; border: 0; background: none; color: rgba(231,218,203,.4); cursor: pointer; }
.admin-main { flex: 1; min-width: 0; }
.admin-topbar { height: 68px; background: rgba(255,250,244,.68); backdrop-filter: blur(16px); border-bottom: 1px solid rgba(67,47,41,.09); padding: 0 30px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 30; }
.topbar-left { display: flex; align-items: center; gap: 13px; }
.breadcrumb { display: flex; align-items: center; gap: 9px; color: var(--ink-muted); font-size: 8px; letter-spacing: .1em; }
.breadcrumb strong { color: var(--ink); font-size: 10px; font-weight: 600; }
.topbar-right { display: flex; align-items: center; gap: 15px; }
.today { display: flex; align-items: center; gap: 6px; color: var(--ink-muted); font-size: 8px; }
.topbar-icon { position: relative; width: 32px; height: 32px; border: 1px solid var(--line); background: rgba(255,255,255,.4); border-radius: 50%; color: var(--ink-soft); display: grid; place-items: center; cursor: pointer; }
.topbar-icon i { position: absolute; right: 5px; top: 5px; width: 5px; height: 5px; background: var(--rose); border-radius: 50%; }
.topbar-avatar { width: 32px; height: 32px; border-radius: 50%; background: var(--paper-deep); color: var(--rose-deep); font-family: var(--font-display); display: grid; place-items: center; font-size: 14px; }
.admin-content { padding: 28px 30px 50px; max-width: 1500px; margin: 0 auto; }
.mobile-menu-btn { display: none; border: 0; background: none; font-size: 20px; color: var(--ink); }
.mobile-admin-inner { min-height: 100%; display: flex; flex-direction: column; }
.mobile-admin-inner nav { display: flex; flex-direction: column; margin: 35px 0 30px; }
.mobile-admin-inner nav a { display: flex; align-items: center; gap: 12px; padding: 15px 6px; text-decoration: none; color: var(--ink-soft); border-bottom: 1px solid var(--line); font-size: 13px; }
.mobile-admin-inner nav a.router-link-active { color: var(--rose-deep); }
.mobile-admin-inner .btn { margin-top: auto; }
@media (max-width: 900px) {
  .admin-sidebar { display: none; }
  .mobile-menu-btn { display: grid; place-items: center; }
  .admin-topbar { padding: 0 18px; }
  .today { display: none; }
  .admin-content { padding: 20px 16px 40px; }
}
</style>