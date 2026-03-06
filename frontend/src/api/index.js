import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000
})

// 知识库管理
export const getKnowledgeBases = () => api.get('/knowledge-bases')
export const createKnowledgeBase = (name) => api.post('/knowledge-base', { name })
export const deleteKnowledgeBase = (name) => api.delete(`/knowledge-base/${name}`)
export const getKbFiles = (name) => api.get(`/knowledge-base/${name}/files`)

// 文件上传
export const uploadFiles = (formData) => api.post('/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})

// 问答
export const chat = (data) => api.post('/chat', data, {
  headers: { 'Content-Type': 'application/json' }
})

export default api
