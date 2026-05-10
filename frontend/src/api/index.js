import axios from 'axios'

const baseURL = import.meta.env.PROD
  ? (import.meta.env.VITE_API_BASE_URL || '') + '/api'
  : '/api'

const api = axios.create({ baseURL, timeout: 30000 })

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

export const authAPI = {
  login: data => api.post('/auth/login', data),
  register: data => api.post('/auth/register', data),
  getUserInfo: () => api.get('/auth/user_info'),
  updateProfile: data => api.put('/auth/update_profile', data)
}

export const demandAPI = {
  create: data => api.post('/demand/create', data),
  list: () => api.get('/demand/list'),
  detail: id => api.get(`/demand/${id}`),
  update: (id, data) => api.put(`/demand/${id}`, data)
}

export const matchAPI = {
  run: demandId => api.post('/match/run', { demand_id: demandId }),
  result: demandId => api.get(`/match/result/${demandId}`)
}

export const orderAPI = {
  create: data => api.post('/order/create', data),
  list: () => api.get('/order/list'),
  detail: id => api.get(`/order/${id}`),
  updateStatus: (id, status) => api.put(`/order/${id}/status`, { status })
}

export const ratingAPI = {
  submit: data => api.post('/rating/submit', data),
  tutorRatings: tutorId => api.get(`/rating/tutor/${tutorId}`)
}

export const courseAPI = {
  create: data => api.post('/course/create', data),
  list: orderId => api.get(`/course/list/${orderId}`),
  update: (id, data) => api.put(`/course/${id}`, data)
}

export const messageAPI = {
  send: data => api.post('/message/send', data),
  conversations: () => api.get('/message/conversations'),
  chat: partnerId => api.get(`/message/chat/${partnerId}`)
}

export const resourceAPI = {
  list: (params = {}) => api.get('/resource/list', { params }),
  create: data => api.post('/resource/create', data),
  detail: id => api.get(`/resource/${id}`)
}

export const paymentAPI = {
  list: () => api.get('/payment/list'),
  create: data => api.post('/payment/create', data)
}

// 消息 — 用户名搜索
messageAPI.searchUser = username => api.get('/message/search_user', { params: { username } })

// 家教搜索
export const tutorSearchAPI = {
  search: (params = {}) => api.get('/tutor/search', { params })
}

// AI助手
export const aiAssistantAPI = {
  faqList: () => api.get('/ai_assistant/faq_list'),
  chat: data => api.post('/ai_assistant/chat', data)
}
