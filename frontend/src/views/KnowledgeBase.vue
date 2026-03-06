<template>
  <div class="kb-page">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>知识库管理</span>
            </div>
          </template>

          <el-form label-width="80px">
            <el-form-item label="选择知识库">
              <el-select v-model="selectedKb" placeholder="请选择知识库" @change="handleKbChange">
                <el-option v-for="kb in kbList" :key="kb" :label="kb" :value="kb" />
              </el-select>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="refreshKbList" :icon="Refresh">刷新</el-button>
              <el-button type="danger" @click="handleDelete" :icon="Delete" :disabled="!selectedKb || selectedKb === 'default'">删除</el-button>
            </el-form-item>
          </el-form>

          <el-divider />

          <div class="create-section">
            <h4>创建新知识库</h4>
            <el-input v-model="newKbName" placeholder="输入知识库名称" style="width: 200px; margin-right: 10px;" />
            <el-button type="primary" @click="createKb" :icon="Plus">创建</el-button>
            <div v-if="kbStatus" class="status-text">{{ kbStatus }}</div>
          </div>

          <el-divider />

          <div class="upload-section">
            <h4>上传文档</h4>
            <el-upload
              ref="uploadRef"
              :auto-upload="false"
              :file-list="fileList"
              :on-change="handleFileChange"
              :on-remove="handleFileRemove"
              accept=".txt,.pdf"
              multiple
              drag
            >
              <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
              <div class="el-upload__text">拖拽文件到这里或<em>点击上传</em></div>
            </el-upload>
            <el-button type="primary" @click="handleUpload" :icon="Upload" :disabled="fileList.length === 0" style="margin-top: 10px;">
              上传到知识库
            </el-button>
            <div v-if="uploadStatus" class="status-text">{{ uploadStatus }}</div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>知识库内容</span>
            </div>
          </template>
          <div v-if="kbFiles.length === 0" class="empty-tip">
            选择知识库查看文件列表
          </div>
          <el-list v-else>
            <el-list-item v-for="file in kbFiles" :key="file">
              <el-icon><Document /></el-icon>
              <span style="margin-left: 8px;">{{ file }}</span>
            </el-list-item>
          </el-list>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Delete, Plus, Upload, UploadFilled, Document } from '@element-plus/icons-vue'
import { getKnowledgeBases, createKnowledgeBase, deleteKnowledgeBase, getKbFiles, uploadFiles } from '../api'

const kbList = ref([])
const selectedKb = ref('')
const newKbName = ref('')
const kbStatus = ref('')
const kbFiles = ref([])
const fileList = ref([])
const uploadRef = ref(null)
const uploadStatus = ref('')

const refreshKbList = async () => {
  try {
    const res = await getKnowledgeBases()
    kbList.value = res.data
    if (kbList.value.length > 0 && !selectedKb.value) {
      selectedKb.value = kbList.value[0]
    }
    handleKbChange()
  } catch (e) {
    ElMessage.error('获取知识库列表失败')
  }
}

const handleKbChange = async () => {
  if (!selectedKb.value) return
  try {
    const res = await getKbFiles(selectedKb.value)
    kbFiles.value = res.data || []
  } catch (e) {
    kbFiles.value = []
  }
}

const createKb = async () => {
  if (!newKbName.value.trim()) {
    ElMessage.warning('请输入知识库名称')
    return
  }
  try {
    const res = await createKnowledgeBase(newKbName.value)
    kbStatus.value = res.data
    newKbName.value = ''
    refreshKbList()
  } catch (e) {
    ElMessage.error('创建失败')
  }
}

const handleDelete = async () => {
  if (!selectedKb.value || selectedKb.value === 'default') return
  try {
    await ElMessageBox.confirm(`确定要删除知识库 "${selectedKb.value}" 吗？`, '提示', { type: 'warning' })
    const res = await deleteKnowledgeBase(selectedKb.value)
    ElMessage.success(res.data || '删除成功')
    refreshKbList()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleFileChange = (file, files) => {
  fileList.value = files
}

const handleFileRemove = (file, files) => {
  fileList.value = files
}

const handleUpload = async () => {
  if (!selectedKb.value) {
    ElMessage.warning('请先选择知识库')
    return
  }
  if (fileList.value.length === 0) {
    ElMessage.warning('请选择要上传的文件')
    return
  }
  const formData = new FormData()
  formData.append('kb_name', selectedKb.value)
  fileList.value.forEach(item => {
    formData.append('files', item.raw)
  })
  try {
    uploadStatus.value = '上传中...'
    const res = await uploadFiles(formData)
    uploadStatus.value = res.data
    fileList.value = []
    uploadRef.value?.clearFiles()
    handleKbChange()
  } catch (e) {
    uploadStatus.value = '上传失败'
    ElMessage.error('上传失败')
  }
}

onMounted(() => {
  refreshKbList()
})
</script>

<style scoped>
.kb-page {
  height: 100%;
}
.card-header {
  font-weight: 600;
}
.status-text {
  margin-top: 10px;
  color: #909399;
  font-size: 14px;
}
.create-section h4, .upload-section h4 {
  margin: 0 0 15px 0;
  color: #303133;
}
.empty-tip {
  text-align: center;
  color: #909399;
  padding: 40px 0;
}
</style>
