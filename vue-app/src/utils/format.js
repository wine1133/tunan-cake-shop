export const money = (value) => {
  const number = Number(value || 0)
  return number.toLocaleString('zh-CN', { minimumFractionDigits: 0, maximumFractionDigits: 2 })
}

export const avatarText = (name) => (name || '甜').slice(0, 1)

export const statusType = (status) => {
  const map = {
    待制作: 'warning',
    制作中: 'primary',
    待取货: 'success',
    已完成: 'info',
    已取消: 'danger'
  }
  return map[status] || 'info'
}