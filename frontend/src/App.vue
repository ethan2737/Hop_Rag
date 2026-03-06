<template>
  <el-container class="app-container">
    <el-aside width="200px">
      <div class="logo">
        <span class="logo-icon">🏥</span>
        <span class="logo-text">Hop-RAG</span>
      </div>
      <el-menu
        :default-active="route.path"
        router
        class="side-menu"
      >
        <el-menu-item index="/knowledge-base">
          <el-icon><FolderOpened /></el-icon>
          <span>知识库管理</span>
        </el-menu-item>
        <el-menu-item index="/chat">
          <el-icon><ChatDotRound /></el-icon>
          <span>AI 对话</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <div class="header-title">中医知识问答系统</div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style scoped>
.app-container {
  height: 100vh;
}
.el-aside {
  background: #fff;
  border-right: 1px solid #e4e7ed;
}
.logo {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid #e4e7ed;
}
.logo-icon {
  font-size: 28px;
}
.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}
.side-menu {
  border-right: none;
}
.el-header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  padding: 0 20px;
}
.header-title {
  font-size: 16px;
  color: #606266;
}
.el-main {
  background: #f5f7fa;
  padding: 20px;
}
</style>
