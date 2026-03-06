import axios from 'axios'

// 创建 axios 实例
// 使用相对路径，通过 Vite 代理转发到后端
const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    console.log('[API Request]', config.method.toUpperCase(), config.url, config.data || config.params)
    return config
  },
  error => {
    console.error('[API Request Error]', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log('[API Response]', response.config.url, response.data)
    return response
  },
  error => {
    console.error('[API Response Error]', error.config?.url, error.message)
    if (error.response) {
      console.error('Response status:', error.response.status)
      console.error('Response data:', error.response.data)
    }
    return Promise.reject(error)
  }
)

// ==================== 知识库管理 API ====================

/**
 * 获取知识库列表
 * GET /api/knowledge-bases
 */
export const getKnowledgeBases = () => {
  return api.get('/knowledge-bases')
}

/**
 * 创建知识库
 * POST /api/knowledge-base
 */
export const createKnowledgeBase = (name) => {
  const formData = new FormData()
  formData.append('name', name)
  return api.post('/knowledge-base', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 删除知识库
 * DELETE /api/knowledge-base/{name}
 */
export const deleteKnowledgeBase = (name) => {
  return api.delete(`/knowledge-base/${name}`)
}

/**
 * 获取知识库文件列表
 * GET /api/knowledge-base/{name}/files
 */
export const getKbFiles = (name) => {
  return api.get(`/knowledge-base/${name}/files`)
}

/**
 * 上传文件到知识库
 * POST /api/upload
 */
export const uploadFiles = (formData) => {
  return api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 聊天问答
 * POST /api/chat
 */
export const chat = (data) => {
  return api.post('/chat', data)
}

export default api
