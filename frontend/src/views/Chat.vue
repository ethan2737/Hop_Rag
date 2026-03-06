<template>
  <div class="chat-page">
    <el-row :gutter="20" style="height: 100%;">
      <el-col :span="6" style="height: 100%;">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">对话设置</div>
          </template>

          <el-form label-width="80px">
            <el-form-item label="知识库">
              <el-select v-model="kbName" placeholder="选择知识库">
                <el-option v-for="kb in kbList" :key="kb" :label="kb" :value="kb" />
              </el-select>
            </el-form-item>

            <el-form-item label="选项">
              <el-checkbox v-model="useSearch">联网搜索</el-checkbox>
            </el-form-item>
            <el-form-item>
              <el-checkbox v-model="useTable">表格输出</el-checkbox>
            </el-form-item>
            <el-form-item>
              <el-checkbox v-model="multiHop">多跳推理</el-checkbox>
            </el-form-item>
          </el-form>

          <el-divider />

          <div class="examples">
            <div class="examples-title">示例问题</div>
            <div
              v-for="(q, i) in examples"
              :key="i"
              class="example-item"
              @click="handleExample(q)"
            >
              {{ q }}
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="18" style="height: 100%;">
        <el-card class="chat-card">
          <template #header>
            <div class="card-header">AI 对话</div>
          </template>

          <div class="chat-container" ref="chatContainer">
            <div v-if="messages.length === 0" class="empty-chat">
              <span class="empty-icon">🏥</span>
              <p>欢迎使用中医知识问答系统</p>
              <p class="empty-tip">请在上方选择知识库，然后输入问题</p>
            </div>
            <div v-else class="message-list">
              <div
                v-for="(msg, index) in messages"
                :key="index"
                :class="['message', msg.role]"
              >
                <div class="message-avatar">{{ msg.role === 'user' ? '你' : 'AI' }}</div>
                <div class="message-content" v-html="formatMessage(msg.content)"></div>
              </div>
              <div v-if="loading" class="loading-tip">
                <el-icon class="is-loading"><Loading /></el-icon>
                AI 正在思考...
              </div>
            </div>
          </div>

          <div class="input-area">
            <el-input
              v-model="question"
              placeholder="输入您的医疗问题..."
              :disabled="loading"
              @keyup.enter="handleSend"
              type="textarea"
              :rows="2"
              resize="none"
            />
            <el-button type="primary" @click="handleSend" :loading="loading" :icon="Promotion">
              发送
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, Promotion, Loading } from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'
import { getKnowledgeBases, chat } from '../api'

const md = new MarkdownIt()

const kbList = ref([])
const kbName = ref('')
const useSearch = ref(true)
const useTable = ref(true)
const multiHop = ref(false)
const question = ref('')
const messages = ref([])
const loading = ref(false)
const chatContainer = ref(null)

const examples = [
  '中医如何辨证治疗糖尿病？',
  '针灸治疗失眠的常用穴位有哪些？',
  '伤寒论中关于桂枝汤的论述',
  '中医养生的基本原则和方法'
]

const formatMessage = (content) => {
  return md.render(content)
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

const handleSend = async () => {
  if (!question.value.trim()) {
    ElMessage.warning('请输入问题')
    return
  }
  if (!kbName.value) {
    ElMessage.warning('请选择知识库')
    return
  }

  const userMsg = question.value.trim()
  messages.value.push({ role: 'user', content: userMsg })
  question.value = ''
  loading.value = true
  scrollToBottom()

  try {
    const res = await chat({
      question: userMsg,
      kb_name: kbName.value,
      use_search: useSearch.value,
      use_table_format: useTable.value,
      multi_hop: multiHop.value,
      chat_history: messages.value.filter(m => m.role !== 'user').map(m => ({ role: m.role, content: m.content }))
    })
    messages.value.push({ role: 'assistant', content: res.data })
    scrollToBottom()
  } catch (e) {
    ElMessage.error('请求失败，请重试')
  } finally {
    loading.value = false
  }
}

const handleExample = (q) => {
  question.value = q
}

const loadKbList = async () => {
  try {
    const res = await getKnowledgeBases()
    kbList.value = res.data || []
    if (kbList.value.length > 0) {
      kbName.value = kbList.value[0]
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadKbList()
})
</script>

<style scoped>
.chat-page {
  height: calc(100vh - 80px);
}
.settings-card {
  height: 100%;
  overflow-y: auto;
}
.chat-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.card-header {
  font-weight: 600;
}
.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  min-height: 400px;
  max-height: 500px;
}
.empty-chat {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}
.empty-icon {
  font-size: 48px;
}
.empty-tip {
  font-size: 13px;
  color: #c0c4cc;
}
.message-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.message {
  display: flex;
  gap: 10px;
  max-width: 90%;
}
.message.user {
  flex-direction: row-reverse;
  margin-left: auto;
}
.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  flex-shrink: 0;
}
.message.assistant .message-avatar {
  background: #67c23a;
}
.message-content {
  background: #f4f4f5;
  padding: 12px 16px;
  border-radius: 8px;
  line-height: 1.6;
  word-break: break-word;
}
.message.user .message-content {
  background: #ecf5ff;
}
.message-content :deep(pre) {
  background: #2d2d2d;
  color: #f8f8f2;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}
.loading-tip {
  text-align: center;
  color: #909399;
  padding: 10px;
}
.input-area {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e4e7ed;
}
.input-area .el-textarea {
  flex: 1;
}
.examples {
  margin-top: 10px;
}
.examples-title {
  font-size: 13px;
  color: #909399;
  margin-bottom: 10px;
}
.example-item {
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 8px;
  cursor: pointer;
  font-size: 13px;
  color: #606266;
  transition: all 0.2s;
}
.example-item:hover {
  background: #ecf5ff;
  color: #409eff;
}
</style>
