import axios from 'axios'
import { ElMessage } from 'element-plus'
import { authState, logout } from './auth'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000
})

request.interceptors.request.use((config) => {
  if (authState.token) {
    config.headers.Authorization = `Bearer ${authState.token}`
  }
  return config
})

request.interceptors.response.use(
  (response) => {
    const payload = response.data
    if (payload?.code === '200') return payload
    if (payload?.code === '401') {
      logout()
      ElMessage.warning(payload.msg || '请先登录')
      if (window.location.pathname !== '/login') {
        window.location.href = `/login?redirect=${encodeURIComponent(window.location.pathname)}`
      }
    } else {
      ElMessage.error(payload?.msg || '操作失败，请稍后再试')
    }
    return Promise.reject(new Error(payload?.msg || 'Request failed'))
  },
  (error) => {
    ElMessage.error(error.response?.data?.detail || '网络连接异常，请检查服务是否启动')
    return Promise.reject(error)
  }
)

export default request