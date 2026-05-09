import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

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
