<template>
  <div class="account-wrap">
    <div class="container">
      <AccountHeader title="个人中心" subtitle="在这里，照顾好属于你的兔南账户。" />

      <div class="profile-layout">
        <aside class="profile-aside">
          <div class="profile-art">
            <div class="avatar-large">
              <img v-if="profile.avatar" :src="profile.avatar" alt="" />
              <span v-else>{{ avatarText(profile.name) }}</span>
              <el-upload class="avatar-upload" :show-file-list="false" :http-request="uploadAvatar" accept="image/*">
                <button class="avatar-camera"><el-icon><Camera /></el-icon></button>
              </el-upload>
            </div>
            <span class="member-label">TU NAN MEMBER</span>
            <h2>{{ profile.name }}</h2>
            <p>@{{ profile.username }}</p>
            <div class="member-card">
              <span class="member-card-label">兔南会员</span>
              <strong>SWEET CLUB</strong>
              <div><span>NO. {{ String(profile.id || 0).padStart(6, '0') }}</span><span>{{ profile.role }}</span></div>
            </div>
          </div>
          <div class="profile-tip"><el-icon><MagicStick /></el-icon><p>生日当月预订蛋糕，可领取专属蜡烛与手写贺卡。</p></div>
        </aside>

        <div class="profile-content">
          <section class="profile-section">
            <div class="profile-section-head">
              <div><span class="eyebrow">PROFILE</span><h3>基本资料</h3></div>
              <button class="btn btn-primary btn-small" :disabled="savingProfile" @click="saveProfile">{{ savingProfile ? '保存中...' : '保存修改' }}</button>
            </div>
            <div class="profile-form-grid">
              <div class="field"><label class="field-label">昵称</label><el-input v-model="profile.name" size="large" /></div>
              <div class="field"><label class="field-label">账号</label><el-input v-model="profile.username" size="large" disabled /></div>
              <div class="field full-field"><label class="field-label">账户角色</label><el-input :model-value="profile.role" size="large" disabled /><p class="form-help">如需变更账户角色，请联系兔南客服。</p></div>
            </div>
          </section>

          <section class="profile-section password-section">
            <div class="profile-section-head">
              <div><span class="eyebrow">SECURITY</span><h3>修改密码</h3></div>
              <el-icon class="security-icon"><Lock /></el-icon>
            </div>
            <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-position="top">
              <div class="profile-form-grid">
                <el-form-item label="当前密码" prop="password"><el-input v-model="passwordForm.password" type="password" show-password size="large" /></el-form-item>
                <div></div>
                <el-form-item label="新密码" prop="newPassword"><el-input v-model="passwordForm.newPassword" type="password" show-password size="large" /></el-form-item>
                <el-form-item label="确认新密码" prop="confirmPassword"><el-input v-model="passwordForm.confirmPassword" type="password" show-password size="large" /></el-form-item>
              </div>
              <button class="btn btn-outline btn-small" :disabled="savingPassword" @click.prevent="changePassword">{{ savingPassword ? '保存中...' : '更新密码' }}</button>
            </el-form>
          </section>

          <section class="profile-section service-section">
            <div class="service-copy"><span class="eyebrow">NEED HELP?</span><h3>需要一点帮助？</h3><p>关于订单、配送或定制蛋糕，兔南客服每日 09:00-21:00 为你服务。</p></div>
            <div class="service-contact"><span><el-icon><Phone /></el-icon> 021-6888 1024</span><span><el-icon><Message /></el-icon> hello@tunan-cake.cn</span></div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import AccountHeader from '../components/AccountHeader.vue'
import request from '../utils/request'
import { authState, updateProfile } from '../utils/auth'
import { avatarText } from '../utils/format'

const profile = reactive({ id: null, username: '', name: '', avatar: '', role: '' })
const passwordForm = reactive({ password: '', newPassword: '', confirmPassword: '' })
const passwordFormRef = ref()
const savingProfile = ref(false)
const savingPassword = ref(false)

const validateConfirm = (rule, value, callback) => {
  if (!value) callback(new Error('请再次输入新密码'))
  else if (value !== passwordForm.newPassword) callback(new Error('两次输入的密码不一致'))
  else callback()
}
const passwordRules = {
  password: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
  newPassword: [{ required: true, message: '请输入新密码', trigger: 'blur' }, { min: 6, message: '新密码至少 6 位', trigger: 'blur' }],
  confirmPassword: [{ validator: validateConfirm, trigger: 'blur' }]
}

const loadProfile = async () => {
  const res = await request.get('/me')
  Object.assign(profile, res.data)
}

const uploadAvatar = async ({ file }) => {
  const data = new FormData()
  data.append('file', file)
  const res = await request.post('/files/upload', data, { headers: { 'Content-Type': 'multipart/form-data' } })
  profile.avatar = res.data
  await saveProfile()
}

const saveProfile = async () => {
  savingProfile.value = true
  try {
    const res = await request.put('/profile', { name: profile.name, avatar: profile.avatar })
    Object.assign(profile, res.data)
    updateProfile(res.data)
    ElMessage.success('个人资料已更新')
  } finally {
    savingProfile.value = false
  }
}

const changePassword = async () => {
  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return
    savingPassword.value = true
    try {
      await request.put('/updatePassword', { password: passwordForm.password, newPassword: passwordForm.newPassword })
      ElMessage.success('密码修改成功')
      Object.assign(passwordForm, { password: '', newPassword: '', confirmPassword: '' })
      passwordFormRef.value.resetFields()
    } finally {
      savingPassword.value = false
    }
  })
}

onMounted(loadProfile)
</script>

<style scoped>
.profile-layout { display: grid; grid-template-columns: 330px 1fr; gap: 24px; align-items: start; }
.profile-art { background: linear-gradient(145deg, var(--ink), #49322c); border-radius: 26px; padding: 42px 30px 31px; color: #f5e9db; text-align: center; position: relative; overflow: hidden; }
.profile-art::before { content: ''; position: absolute; width: 250px; height: 250px; border: 1px solid rgba(218,192,145,.12); border-radius: 50%; top: -120px; right: -100px; }
.profile-art::after { content: ''; position: absolute; width: 180px; height: 180px; border: 1px dashed rgba(218,192,145,.1); border-radius: 50%; bottom: -100px; left: -60px; }
.avatar-large { position: relative; width: 105px; height: 105px; margin: 0 auto 20px; border-radius: 50%; border: 1px solid rgba(218,192,145,.35); padding: 7px; }
.avatar-large > img, .avatar-large > span { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; display: grid; place-items: center; background: var(--paper-deep); color: var(--rose-deep); font-family: var(--font-display); font-size: 42px; }
.avatar-camera { position: absolute; right: 0; bottom: 4px; width: 32px; height: 32px; border-radius: 50%; border: 2px solid var(--ink); background: var(--gold-light); color: var(--ink); display: grid; place-items: center; cursor: pointer; }
.member-label { font-size: 7px; letter-spacing: .28em; color: var(--gold-light); }
.profile-art h2 { font-family: var(--font-display); font-size: 32px; font-weight: 500; margin: 9px 0 4px; }
.profile-art > p { color: rgba(245,233,219,.45); font-size: 9px; margin: 0 0 28px; }
.member-card { position: relative; z-index: 2; text-align: left; border: 1px solid rgba(218,192,145,.2); border-radius: 15px; padding: 17px; background: linear-gradient(115deg, rgba(255,255,255,.07), rgba(255,255,255,.01)); }
.member-card-label { display: block; color: rgba(245,233,219,.4); font-size: 7px; margin-bottom: 6px; }
.member-card > strong { font-family: var(--font-display); letter-spacing: .16em; font-size: 18px; font-weight: 500; }
.member-card > div { display: flex; justify-content: space-between; margin-top: 17px; color: rgba(245,233,219,.35); font-size: 6px; letter-spacing: .12em; }
.profile-tip { margin-top: 15px; display: flex; gap: 10px; padding: 15px 17px; border-radius: 15px; background: var(--rose-pale); color: var(--rose-deep); }
.profile-tip .el-icon { flex: 0 0 auto; margin-top: 2px; }
.profile-tip p { font-size: 9px; line-height: 1.6; margin: 0; }
.profile-content { display: flex; flex-direction: column; gap: 16px; }
.profile-section { background: rgba(255,250,244,.8); border: 1px solid var(--line); border-radius: 23px; padding: 27px 30px; }
.profile-section-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.profile-section-head h3 { font-family: var(--font-display); font-size: 25px; font-weight: 600; margin: 7px 0 0; }
.profile-form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 18px; }
.full-field { grid-column: span 2; }
.password-section .security-icon { color: var(--rose); font-size: 25px; }
.password-section :deep(.el-form-item) { margin-bottom: 18px; }
.service-section { display: flex; justify-content: space-between; align-items: center; background: var(--paper-deep); border: 0; }
.service-copy h3 { font-family: var(--font-display); font-size: 23px; font-weight: 600; margin: 7px 0 5px; }
.service-copy p { color: var(--ink-soft); font-size: 9px; margin: 0; }
.service-contact { display: flex; flex-direction: column; gap: 8px; }
.service-contact span { display: flex; align-items: center; gap: 7px; color: var(--ink-soft); font-size: 9px; }
.service-contact .el-icon { color: var(--rose); }
@media (max-width: 900px) {
  .profile-layout { grid-template-columns: 1fr; }
  .profile-art { max-width: 420px; width: 100%; margin: 0 auto; }
}
@media (max-width: 600px) {
  .profile-form-grid { grid-template-columns: 1fr; }
  .full-field { grid-column: auto; }
  .profile-section { padding: 22px 20px; }
  .service-section { flex-direction: column; align-items: flex-start; gap: 16px; }
}
</style>