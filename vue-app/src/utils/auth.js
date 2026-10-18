import { reactive } from 'vue'

const storedUser = localStorage.getItem('tunan-user')

export const authState = reactive({
  user: storedUser ? JSON.parse(storedUser) : null,
  token: localStorage.getItem('tunan-token') || ''
})

export function setAuth(payload) {
  authState.user = {
    id: payload.id,
    username: payload.username,
    name: payload.name,
    avatar: payload.avatar,
    role: payload.role
  }
  authState.token = payload.token
  localStorage.setItem('tunan-user', JSON.stringify(authState.user))
  localStorage.setItem('tunan-token', payload.token)
}

export function updateProfile(payload) {
  authState.user = {
    ...authState.user,
    ...payload
  }
  if (payload.token) {
    authState.token = payload.token
    localStorage.setItem('tunan-token', payload.token)
  }
  localStorage.setItem('tunan-user', JSON.stringify(authState.user))
}

export function logout() {
  authState.user = null
  authState.token = ''
  localStorage.removeItem('tunan-user')
  localStorage.removeItem('tunan-token')
}

export function isAdmin() {
  return authState.user?.role === '管理员'
}