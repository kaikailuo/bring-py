<template>
  <div class="student-layout">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-left">
        <div class="logo">
          <el-icon class="logo-icon"><School /></el-icon>
          <span class="logo-text">Python学习平台</span>
        </div>
      </div>
      
      <div class="header-center">
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          class="header-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="/student/dashboard">
            <el-icon><House /></el-icon>
            <span>学习仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/student/practice">
            <el-icon><EditPen /></el-icon>
            <span>编程练习</span>
          </el-menu-item>
          <el-menu-item index="/student/resources">
            <el-icon><FolderOpened /></el-icon>
            <span>教学资源</span>
          </el-menu-item>
          <el-menu-item index="/student/forum">
            <el-icon><ChatDotRound /></el-icon>
            <span>互动交流</span>
          </el-menu-item>
        </el-menu>
      </div>
      
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <div class="user-info">
            <el-avatar :src="userStore.user?.avatar" :size="32">
              <el-icon><User /></el-icon>
            </el-avatar>
            <span class="username">{{ userStore.userName }}</span>
            <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">
                <el-icon><User /></el-icon>
                个人资料
              </el-dropdown-item>
              <el-dropdown-item command="settings">
                <el-icon><Setting /></el-icon>
                系统设置
              </el-dropdown-item>
              <el-dropdown-item divided command="logout">
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <div class="main-container">
      <!-- 侧边栏 -->
      <aside class="sidebar">
        <div class="sidebar-content">
          <!-- 学习进度 -->
          <div class="progress-card education-card">
            <h3 class="card-title">
              <el-icon><TrendCharts /></el-icon>
              学习进度
            </h3>
            <div class="progress-stats">
              <div class="stat-item">
                <span class="stat-label">已完成课程</span>
                <span class="stat-value">8/12</span>
              </div>
              <el-progress :percentage="67" :stroke-width="8" />
            </div>
            <div class="progress-details">
              <div class="detail-item">
                <span class="detail-label">Python基础</span>
                <span class="detail-status completed">已完成</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">数据结构</span>
                <span class="detail-status in-progress">进行中</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">算法入门</span>
                <span class="detail-status pending">未开始</span>
              </div>
            </div>
          </div>

          <!-- 快捷导航 -->
          <div class="quick-nav education-card">
            <h3 class="card-title">
              <el-icon><Guide /></el-icon>
              快捷导航
            </h3>
            <div class="nav-items">
              <div class="nav-item" @click="$router.push('/student/practice')">
                <el-icon><EditPen /></el-icon>
                <span>编程练习</span>
                <el-badge :value="3" class="nav-badge" />
              </div>
              <div class="nav-item" @click="$router.push('/student/resources')">
                <el-icon><Document /></el-icon>
                <span>学习资料</span>
              </div>
              <div class="nav-item" @click="$router.push('/student/forum')">
                <el-icon><ChatDotRound /></el-icon>
                <span>讨论区</span>
                <el-badge :value="5" class="nav-badge" />
              </div>
              <div class="nav-item" @click="showAIAssistant = true">
                <el-icon><Magic /></el-icon>
                <span>AI助手</span>
              </div>
            </div>
          </div>

          <!-- 最近学习 -->
          <div class="recent-learning education-card">
            <h3 class="card-title">
              <el-icon><Clock /></el-icon>
              最近学习
            </h3>
            <div class="recent-items">
              <div class="recent-item">
                <div class="item-icon">
                  <el-icon><VideoPlay /></el-icon>
                </div>
                <div class="item-content">
                  <div class="item-title">Python列表操作</div>
                  <div class="item-meta">2小时前</div>
                </div>
              </div>
              <div class="recent-item">
                <div class="item-icon">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="item-content">
                  <div class="item-title">数据结构基础</div>
                  <div class="item-meta">1天前</div>
                </div>
              </div>
              <div class="recent-item">
                <div class="item-icon">
                  <el-icon><EditPen /></el-icon>
                </div>
                <div class="item-content">
                  <div class="item-title">编程练习</div>
                  <div class="item-meta">3天前</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- 主内容区 -->
      <main class="content">
        <router-view />
      </main>

      <!-- 右侧面板 -->
      <aside class="right-panel">
        <div class="panel-content">
          <!-- AI助手 -->
          <div class="ai-assistant education-card">
            <div class="assistant-header">
              <h3 class="card-title">
                <el-icon><Magic /></el-icon>
                AI编程助手
              </h3>
              <el-button type="primary" size="small" @click="showAIAssistant = true">
                开始对话
              </el-button>
            </div>
            <div class="assistant-preview">
              <div class="preview-item">
                <el-icon><ChatDotRound /></el-icon>
                <span>有什么编程问题可以问我</span>
              </div>
              <div class="preview-item">
                <el-icon><Lightbulb /></el-icon>
                <span>我可以帮你调试代码</span>
              </div>
              <div class="preview-item">
                <el-icon><Guide /></el-icon>
                <span>为你推荐学习路径</span>
              </div>
            </div>
          </div>

          <!-- 学习统计 -->
          <div class="learning-stats education-card">
            <h3 class="card-title">
              <el-icon><TrendCharts /></el-icon>
              学习统计
            </h3>
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-number">24</div>
                <div class="stat-label">学习天数</div>
              </div>
              <div class="stat-card">
                <div class="stat-number">156</div>
                <div class="stat-label">代码行数</div>
              </div>
              <div class="stat-card">
                <div class="stat-number">8</div>
                <div class="stat-label">完成练习</div>
              </div>
              <div class="stat-card">
                <div class="stat-number">3</div>
                <div class="stat-label">获得徽章</div>
              </div>
            </div>
          </div>

          <!-- 公告通知 -->
          <div class="notifications education-card">
            <h3 class="card-title">
              <el-icon><Bell /></el-icon>
              最新通知
            </h3>
            <div class="notification-list">
              <div class="notification-item">
                <div class="notification-icon">
                  <el-icon><Trophy /></el-icon>
                </div>
                <div class="notification-content">
                  <div class="notification-title">恭喜获得新徽章！</div>
                  <div class="notification-desc">Python基础掌握者</div>
                </div>
              </div>
              <div class="notification-item">
                <div class="notification-icon">
                  <el-icon><Calendar /></el-icon>
                </div>
                <div class="notification-content">
                  <div class="notification-title">新课程上线</div>
                  <div class="notification-desc">算法入门课程已发布</div>
                </div>
              </div>
              <div class="notification-item">
                <div class="notification-icon">
                  <el-icon><Star /></el-icon>
                </div>
                <div class="notification-content">
                  <div class="notification-title">作业提醒</div>
                  <div class="notification-desc">数据结构作业即将截止</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <!-- AI助手对话框 -->
    <el-dialog
      v-model="showAIAssistant"
      title="AI编程助手"
      width="800px"
      :before-close="handleAIAssistantClose"
    >
      <div class="ai-assistant-dialog">
        <div class="chat-messages">
          <div class="message ai-message">
            <div class="message-avatar">
              <el-icon><Magic /></el-icon>
            </div>
            <div class="message-content">
              <div class="message-text">
                你好！我是你的AI编程助手，有什么Python编程问题需要帮助吗？
              </div>
            </div>
          </div>
        </div>
        <div class="chat-input">
          <el-input
            v-model="aiMessage"
            placeholder="输入你的编程问题..."
            type="textarea"
            :rows="3"
          />
          <el-button type="primary" @click="sendAIMessage" :disabled="!aiMessage.trim()">
            发送
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 响应式数据
const showAIAssistant = ref(false)
const aiMessage = ref('')

// 计算属性
const activeMenu = computed(() => route.path)

// 方法
const handleMenuSelect = (index) => {
  router.push(index)
}

const handleCommand = async (command) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人资料功能开发中...')
      break
    case 'settings':
      ElMessage.info('系统设置功能开发中...')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        userStore.logout()
        router.push('/home')
        ElMessage.success('已退出登录')
      } catch {
        // 用户取消
      }
      break
  }
}

const handleAIAssistantClose = () => {
  showAIAssistant.value = false
  aiMessage.value = ''
}

const sendAIMessage = () => {
  if (!aiMessage.value.trim()) return
  
  // 模拟AI回复
  ElMessage.success('AI助手功能开发中，敬请期待！')
  aiMessage.value = ''
}
</script>

<style scoped>
.student-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: $bg-secondary;
}

/* 头部导航 */
.header {
  height: 64px;
  background: white;
  border-bottom: 1px solid $border-color;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 $spacing-lg;
  box-shadow: $box-shadow;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: $font-size-lg;
  font-weight: bold;
  color: $education-blue;
}

.logo-icon {
  font-size: $font-size-xl;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.header-menu {
  border-bottom: none;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm $spacing-md;
  border-radius: $border-radius;
  cursor: pointer;
  transition: background-color 0.3s ease;
  
  &:hover {
    background: $bg-hover;
  }
}

.username {
  font-weight: 500;
  color: $text-primary;
}

.dropdown-icon {
  font-size: $font-size-sm;
  color: $text-secondary;
}

/* 主容器 */
.main-container {
  flex: 1;
  display: grid;
  grid-template-columns: 280px 1fr 300px;
  gap: $spacing-lg;
  padding: $spacing-lg;
  overflow: hidden;
}

/* 侧边栏 */
.sidebar {
  overflow-y: auto;
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

/* 右侧面板 */
.right-panel {
  overflow-y: auto;
}

.panel-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

/* 内容区域 */
.content {
  background: white;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  overflow-y: auto;
}

/* 卡片样式 */
.education-card {
  padding: $spacing-lg;
  background: white;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
}

.card-title {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: $font-size-md;
  font-weight: bold;
  color: $text-primary;
  margin-bottom: $spacing-md;
}

/* 学习进度 */
.progress-stats {
  margin-bottom: $spacing-md;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-sm;
}

.stat-label {
  color: $text-secondary;
  font-size: $font-size-sm;
}

.stat-value {
  font-weight: bold;
  color: $education-blue;
}

.progress-details {
  margin-top: $spacing-md;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-sm 0;
  border-bottom: 1px solid $border-color;
  
  &:last-child {
    border-bottom: none;
  }
}

.detail-label {
  color: $text-primary;
  font-size: $font-size-sm;
}

.detail-status {
  font-size: $font-size-xs;
  padding: $spacing-xs $spacing-sm;
  border-radius: 12px;
  
  &.completed {
    background: $success-color;
    color: white;
  }
  
  &.in-progress {
    background: $warning-color;
    color: white;
  }
  
  &.pending {
    background: $bg-hover;
    color: $text-secondary;
  }
}

/* 快捷导航 */
.nav-items {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm $spacing-md;
  border-radius: $border-radius;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  
  &:hover {
    background: $bg-hover;
    transform: translateX(4px);
  }
}

.nav-badge {
  margin-left: auto;
}

/* 最近学习 */
.recent-items {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm;
  border-radius: $border-radius;
  transition: background-color 0.3s ease;
  
  &:hover {
    background: $bg-hover;
  }
}

.item-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: $education-blue;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-content {
  flex: 1;
}

.item-title {
  font-size: $font-size-sm;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.item-meta {
  font-size: $font-size-xs;
  color: $text-secondary;
}

/* AI助手 */
.assistant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-md;
}

.assistant-preview {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.preview-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm;
  background: $bg-secondary;
  border-radius: $border-radius;
  font-size: $font-size-sm;
  color: $text-secondary;
}

/* 学习统计 */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-md;
}

.stat-card {
  text-align: center;
  padding: $spacing-md;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.stat-number {
  font-size: $font-size-xl;
  font-weight: bold;
  color: $education-blue;
  margin-bottom: $spacing-xs;
}

.stat-label {
  font-size: $font-size-xs;
  color: $text-secondary;
}

/* 通知 */
.notification-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: $spacing-sm;
  padding: $spacing-sm;
  border-radius: $border-radius;
  transition: background-color 0.3s ease;
  
  &:hover {
    background: $bg-hover;
  }
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: $education-green;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-size: $font-size-sm;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.notification-desc {
  font-size: $font-size-xs;
  color: $text-secondary;
}

/* AI助手对话框 */
.ai-assistant-dialog {
  height: 400px;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: $spacing-md;
}

.message {
  display: flex;
  gap: $spacing-sm;
  margin-bottom: $spacing-md;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: $education-blue;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
}

.message-text {
  padding: $spacing-sm $spacing-md;
  background: $bg-secondary;
  border-radius: $border-radius;
  font-size: $font-size-sm;
}

.chat-input {
  display: flex;
  gap: $spacing-sm;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-container {
    grid-template-columns: 250px 1fr 250px;
  }
}

@media (max-width: 992px) {
  .main-container {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto;
  }
  
  .sidebar,
  .right-panel {
    order: 2;
  }
  
  .content {
    order: 1;
  }
  
  .sidebar-content,
  .panel-content {
    flex-direction: row;
    overflow-x: auto;
  }
  
  .education-card {
    min-width: 250px;
  }
}

@media (max-width: 768px) {
  .header {
    padding: 0 $spacing-md;
  }
  
  .header-center {
    display: none;
  }
  
  .main-container {
    padding: $spacing-md;
  }
}
</style>
