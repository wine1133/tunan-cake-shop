<template>
  <div class="announcement">
    <span>秋日限定 · 白桃乌龙慕斯现已上新</span>
    <span class="announcement-dot"></span>
    <span>上海市内冷链配送 · 至少提前 24 小时预订</span>
  </div>
  <header class="store-header" :class="{ scrolled }">
    <div class="header-inner">
      <router-link to="/" class="brand-link" aria-label="返回首页"><BrandMark /></router-link>
      <nav class="desktop-nav">
        <router-link to="/">首页</router-link>
        <router-link to="/catalog">全部蛋糕</router-link>
        <a href="/#our-story">品牌故事</a>
        <router-link v-if="authState.user" to="/orders">我的订单</router-link>
      </nav>
      <div class="header-actions">
        <router-link v-if="authState.user" to="/orders" class="icon-action" aria-label="我的订单">
          <el-icon><ShoppingBag /></el-icon>
        </router-link>
        <template v-if="authState.user">
          <el-dropdown trigger="click" @command="handleCommand">
            <button class="account-trigger">
              <span class="avatar-mini">
                <img v-if="authState.user.avatar" :src="authState.user.avatar" alt="" />
                <span v-else>{{ avatarText(authState.user.name) }}</span>
              </span>
              <span class="account-name">{{ authState.user.name }}</span>
              <el-icon class="chevron"><ArrowDown /></el-icon>
            </button>
            <template #dropdown>
              <el-dropdown-menu class="account-menu">
                <el-dropdown-item v-if="isAdmin()" command="admin"><el-icon><Grid /></el-icon>管理后台</el-dropdown-item>
                <el-dropdown-item command="orders"><el-icon><Tickets /></el-icon>我的订单</el-dropdown-item>
                <el-dropdown-item command="addresses"><el-icon><Location /></el-icon>收货地址</el-dropdown-item>
                <el-dropdown-item command="profile"><el-icon><User /></el-icon>个人中心</el-dropdown-item>
                <el-dropdown-item divided command="logout"><el-icon><SwitchButton /></el-icon>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <router-link to="/login" class="login-link">登录</router-link>
          <router-link to="/login?tab=register" class="btn btn-primary btn-small">立即预订</router-link>
        </template>
        <button class="mobile-toggle" @click="drawerVisible = true" aria-label="打开菜单">
          <el-icon><Menu /></el-icon>
        </button>
      </div>
    </div>
  </header>

  <el-drawer v-model="drawerVisible" direction="rtl" size="82%" :with-header="false" class="mobile-drawer">
    <div class="drawer-content">
      <BrandMark />
      <nav class="drawer-nav" @click="drawerVisible = false">
        <router-link to="/">首页 <span>01</span></router-link>
        <router-link to="/catalog">全部蛋糕 <span>02</span></router-link>
        <a href="/#our-story">品牌故事 <span>03</span></a>
        <router-link v-if="authState.user" to="/orders">我的订单 <span>04</span></router-link>
        <router-link v-if="authState.user" to="/profile">个人中心 <span>05</span></router-link>
      </nav>
      <div class="drawer-footer">
        <template v-if="authState.user">
          <p>你好，{{ authState.user.name }}</p>
          <button class="btn btn-outline full" @click="handleCommand('logout')">退出登录</button>
        </template>
        <template v-else>
          <p>登录后即可预订与查看订单</p>
          <router-link to="/login" class="btn btn-primary full" @click="drawerVisible = false">登录 / 注册</router-link>
        </template>
      </div>
    </div>
  </el-drawer>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import BrandMark from './BrandMark.vue'
import { authState, isAdmin, logout } from '../utils/auth'
import { avatarText } from '../utils/format'

const router = useRouter()
const drawerVisible = ref(false)
const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 18 }
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onBeforeUnmount(() => window.removeEventListener('scroll', onScroll))

const handleCommand = (command) => {
  drawerVisible.value = false
  if (command === 'logout') {
    logout()
    router.push('/')
    return
  }
  if (command === 'admin') router.push('/admin')
  if (command === 'orders') router.push('/orders')
  if (command === 'addresses') router.push('/addresses')
  if (command === 'profile') router.push('/profile')
}
</script>

<style scoped>
.announcement {
  height: 34px; display: flex; justify-content: center; align-items: center; gap: 18px;
  background: var(--ink); color: #f1e5d2; font-size: 11px; letter-spacing: .13em;
}
.announcement-dot { width: 3px; height: 3px; border-radius: 50%; background: var(--gold-light); }
.store-header {
  height: 84px; position: sticky; top: 0; z-index: 50; transition: .35s ease;
  background: rgba(250, 246, 239, .82); backdrop-filter: blur(18px);
  border-bottom: 1px solid rgba(66, 45, 39, .08);
}
.store-header.scrolled { background: rgba(250, 246, 239, .96); box-shadow: 0 12px 40px rgba(64, 42, 34, .07); }
.header-inner { max-width: 1280px; height: 100%; margin: 0 auto; padding: 0 32px; display: flex; align-items: center; }
.brand-link { text-decoration: none; }
.desktop-nav { display: flex; align-items: center; gap: 36px; margin-left: 76px; }
.desktop-nav a { color: var(--ink-soft); text-decoration: none; font-size: 13px; letter-spacing: .08em; position: relative; padding: 8px 0; }
.desktop-nav a::after { content: ''; position: absolute; height: 1px; width: 0; background: var(--rose); left: 0; bottom: 2px; transition: width .3s ease; }
.desktop-nav a:hover, .desktop-nav a.router-link-active { color: var(--ink); }
.desktop-nav a:hover::after, .desktop-nav a.router-link-active::after { width: 100%; }
.header-actions { margin-left: auto; display: flex; align-items: center; gap: 16px; }
.icon-action { width: 36px; height: 36px; border-radius: 50%; border: 1px solid rgba(47, 33, 29, .13); display: grid; place-items: center; color: var(--ink); }
.login-link { color: var(--ink); text-decoration: none; font-size: 13px; letter-spacing: .08em; }
.account-trigger { display: flex; align-items: center; gap: 9px; background: none; border: 0; cursor: pointer; color: var(--ink); padding: 4px; }
.avatar-mini { width: 36px; height: 36px; border-radius: 50%; overflow: hidden; background: var(--rose-pale); color: var(--rose-deep); display: grid; place-items: center; font-family: var(--font-display); font-size: 16px; border: 1px solid rgba(140, 74, 85, .18); }
.avatar-mini img { width: 100%; height: 100%; object-fit: cover; }
.account-name { max-width: 82px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 13px; }
.chevron { font-size: 11px; color: var(--ink-muted); }
.mobile-toggle { display: none; border: 0; background: none; font-size: 22px; color: var(--ink); }
.drawer-content { display: flex; flex-direction: column; min-height: 100%; padding: 30px 10px; }
.drawer-nav { display: flex; flex-direction: column; margin-top: 55px; }
.drawer-nav a { color: var(--ink); text-decoration: none; font-family: var(--font-display); font-size: 30px; padding: 18px 4px; border-bottom: 1px solid rgba(66,45,39,.1); display: flex; justify-content: space-between; align-items: center; }
.drawer-nav span { font-family: var(--font-body); font-size: 10px; color: var(--ink-muted); }
.drawer-footer { margin-top: auto; padding: 32px 4px 10px; }
.drawer-footer p { color: var(--ink-soft); font-size: 13px; }
@media (max-width: 900px) {
  .desktop-nav { display: none; }
  .header-inner { padding: 0 20px; }
  .store-header { height: 70px; }
  .announcement span:last-child, .announcement-dot { display: none; }
  .mobile-toggle { display: grid; place-items: center; }
  .account-name { display: none; }
  .header-actions .login-link { display: none; }
}
</style>