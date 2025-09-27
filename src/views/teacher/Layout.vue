<template>
  <div class="teacher-layout">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-left">
        <div class="logo">
          <el-icon class="logo-icon"><School /></el-icon>
          <span class="logo-text">教师管理平台</span>
        </div>
      </div>
      
      <div class="header-center">
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          class="header-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="/teacher/dashboard">
            <el-icon><House /></el-icon>
            <span>教学仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/teacher/class-management">
            <el-icon><UserFilled /></el-icon>
            <span>班级管理</span>
          </el-menu-item>
          <el-menu-item index="/teacher/resource-management">
            <el-icon><FolderOpened /></el-icon>
            <span>资源管理</span>
          </el-menu-item>
          <el-menu-item index="/teacher/analytics">
            <el-icon><TrendCharts /></el-icon>
            <span>学情分析</span>
          </el-menu-item>
          <el-menu-item index="/teacher/question-monitor">
            <el-icon><ChatDotRound /></el-icon>
            <span>问题监控</span>
          </el-menu-item>
        </el-menu>
      </div>
      
      <div class="header-right">
        <div class="notification-bell">
          <el-badge :value="unreadNotifications" :max="99">
            <el-icon class="bell-icon"><Bell /></el-icon>
          </el-badge>
        </div>
        
        <el-dropdown @command="handleCommand">
          <div class="user-info">
            <el-avatar :src="userStore.user?.avatar" :size="32">
              <el-icon><UserFilled /></el-icon>
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
          <!-- 快速统计 -->
          <div class="quick-stats education-card">
            <h3 class="card-title">
              <el-icon><DataAnalysis /></el-icon>
              快速统计
            </h3>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-icon students">
                  <el-icon><User /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ teacherStats.totalStudents }}</div>
                  <div class="stat-label">学生总数</div>
                </div>
              </div>
              <div class="stat-item">
                <div class="stat-icon classes">
                  <el-icon><UserFilled /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ teacherStats.totalClasses }}</div>
                  <div class="stat-label">班级数量</div>
                </div>
              </div>
              <div class="stat-item">
                <div class="stat-icon resources">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ teacherStats.totalResources }}</div>
                  <div class="stat-label">教学资源</div>
                </div>
              </div>
              <div class="stat-item">
                <div class="stat-icon questions">
                  <el-icon><QuestionFilled /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ teacherStats.pendingQuestions }}</div>
                  <div class="stat-label">待回答问题</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 快捷操作 -->
          <div class="quick-actions education-card">
            <h3 class="card-title">
              <el-icon><Lightning /></el-icon>
              快捷操作
            </h3>
            <div class="action-items">
              <div class="action-item" @click="$router.push('/teacher/resource-management')">
                <el-icon><Upload /></el-icon>
                <span>上传资源</span>
              </div>
              <div class="action-item" @click="$router.push('/teacher/class-management')">
                <el-icon><UserFilled /></el-icon>
                <span>班级管理</span>
              </div>
              <div class="action-item" @click="$router.push('/teacher/question-monitor')">
                <el-icon><ChatDotRound /></el-icon>
                <span>答疑中心</span>
              </div>
              <div class="action-item" @click="createAssignment">
                <el-icon><EditPen /></el-icon>
                <span>布置作业</span>
              </div>
            </div>
          </div>

          <!-- 今日待办 -->
          <div class="today-tasks education-card">
            <h3 class="card-title">
              <el-icon><Calendar /></el-icon>
              今日待办
            </h3>
            <div class="task-list">
              <div class="task-item" v-for="task in todayTasks" :key="task.id">
                <div class="task-icon" :class="task.priority">
                  <el-icon><component :is="task.icon" /></el-icon>
                </div>
                <div class="task-content">
                  <div class="task-title">{{ task.title }}</div>
                  <div class="task-time">{{ task.time }}</div>
                </div>
                <div class="task-status">
                  <el-tag size="small" :type="task.status === 'completed' ? 'success' : 'warning'">
                    {{ task.status === 'completed' ? '已完成' : '待处理' }}
                  </el-tag>
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
          <!-- 学生活动 -->
          <div class="student-activity education-card">
            <div class="activity-header">
              <h3 class="card-title">
                <el-icon><TrendCharts /></el-icon>
                学生活动
              </h3>
              <el-button type="primary" size="small" @click="$router.push('/teacher/analytics')">
                查看详情
              </el-button>
            </div>
            <div class="activity-list">
              <div class="activity-item" v-for="activity in studentActivities" :key="activity.id">
                <div class="activity-avatar">
                  <el-avatar :src="activity.avatar" :size="32">
                    <el-icon><User /></el-icon>
                  </el-avatar>
                </div>
                <div class="activity-content">
                  <div class="activity-text">{{ activity.action }}</div>
                  <div class="activity-meta">{{ activity.time }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 热门话题 -->
          <div class="hot-topics education-card">
            <h3 class="card-title">
              <el-icon><Star /></el-icon>
              热门话题
            </h3>
            <div class="topic-list">
              <div class="topic-item" v-for="topic in hotTopics" :key="topic.id">
                <div class="topic-title">{{ topic.title }}</div>
                <div class="topic-stats">
                  <span class="topic-views">{{ topic.views }} 浏览</span>
                  <span class="topic-replies">{{ topic.replies }} 回复</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 系统公告 -->
          <div class="system-announcements education-card">
            <h3 class="card-title">
              <el-icon><Bell /></el-icon>
              系统公告
            </h3>
            <div class="announcement-list">
              <div class="announcement-item" v-for="announcement in announcements" :key="announcement.id">
                <div class="announcement-icon">
                  <el-icon><component :is="announcement.icon" /></el-icon>
                </div>
                <div class="announcement-content">
                  <div class="announcement-title">{{ announcement.title }}</div>
                  <div class="announcement-time">{{ announcement.time }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 响应式数据
const unreadNotifications = ref(5)

const teacherStats = ref({
  totalStudents: 156,
  totalClasses: 8,
  totalResources: 89,
  pendingQuestions: 12
})

const todayTasks = ref([
  {
    id: 1,
    title: '批改Python基础作业',
    time: '09:00',
    priority: 'high',
    icon: 'EditPen',
    status: 'pending'
  },
  {
    id: 2,
    title: '准备数据结构课程',
    time: '14:00',
    priority: 'medium',
    icon: 'Document',
    status: 'completed'
  },
  {
    id: 3,
    title: '回答学生问题',
    time: '16:00',
    priority: 'high',
    icon: 'ChatDotRound',
    status: 'pending'
  }
])

const studentActivities = ref([
  {
    id: 1,
    action: '张同学完成了Python基础练习',
    time: '5分钟前',
    avatar: ''
  },
  {
    id: 2,
    action: '李同学提交了数据结构作业',
    time: '10分钟前',
    avatar: ''
  },
  {
    id: 3,
    action: '王同学在论坛提出了问题',
    time: '15分钟前',
    avatar: ''
  }
])

const hotTopics = ref([
  {
    id: 1,
    title: 'Python列表操作的最佳实践',
    views: 156,
    replies: 23
  },
  {
    id: 2,
    title: '如何理解递归算法',
    views: 134,
    replies: 18
  },
  {
    id: 3,
    title: '数据结构学习心得分享',
    views: 98,
    replies: 15
  }
])

const announcements = ref([
  {
    id: 1,
    title: '新功能上线：AI编程助手',
    time: '2小时前',
    icon: 'Magic'
  },
  {
    id: 2,
    title: '系统维护通知',
    time: '1天前',
    icon: 'Setting'
  },
  {
    id: 3,
    title: '教师培训活动安排',
    time: '3天前',
    icon: 'Calendar'
  }
])

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

const createAssignment = () => {
  ElMessage.info('布置作业功能开发中...')
}

onMounted(() => {
  // 初始化数据
})
</script>

<style scoped>
.teacher-layout {
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
  color: $education-green;
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
  gap: $spacing-lg;
}

.notification-bell {
  cursor: pointer;
  padding: $spacing-sm;
  border-radius: $border-radius;
  transition: background-color 0.3s ease;
  
  &:hover {
    background: $bg-hover;
  }
}

.bell-icon {
  font-size: 1.2rem;
  color: $text-secondary;
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
  grid-template-columns: 300px 1fr 320px;
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

/* 快速统计 */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-md;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.stat-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: $font-size-sm;
  
  &.students {
    background: $education-blue;
  }
  
  &.classes {
    background: $education-green;
  }
  
  &.resources {
    background: $education-orange;
  }
  
  &.questions {
    background: $education-purple;
  }
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  line-height: 1;
}

.stat-label {
  font-size: $font-size-xs;
  color: $text-secondary;
}

/* 快捷操作 */
.action-items {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-sm;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-xs;
  padding: $spacing-md;
  background: $bg-secondary;
  border-radius: $border-radius;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: $education-green;
    color: white;
    transform: translateY(-2px);
  }
}

.action-item .el-icon {
  font-size: 1.2rem;
}

.action-item span {
  font-size: $font-size-xs;
  text-align: center;
}

/* 今日待办 */
.task-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.task-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.task-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: $font-size-xs;
  
  &.high {
    background: $error-color;
  }
  
  &.medium {
    background: $warning-color;
  }
  
  &.low {
    background: $success-color;
  }
}

.task-content {
  flex: 1;
}

.task-title {
  font-size: $font-size-sm;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.task-time {
  font-size: $font-size-xs;
  color: $text-secondary;
}

/* 学生活动 */
.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-md;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.activity-avatar {
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: $font-size-sm;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.activity-meta {
  font-size: $font-size-xs;
  color: $text-secondary;
}

/* 热门话题 */
.topic-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.topic-item {
  padding: $spacing-sm;
  background: $bg-secondary;
  border-radius: $border-radius;
  cursor: pointer;
  transition: background-color 0.3s ease;
  
  &:hover {
    background: $bg-hover;
  }
}

.topic-title {
  font-size: $font-size-sm;
  color: $text-primary;
  margin-bottom: $spacing-xs;
  line-height: 1.4;
}

.topic-stats {
  display: flex;
  gap: $spacing-md;
  font-size: $font-size-xs;
  color: $text-secondary;
}

/* 系统公告 */
.announcement-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.announcement-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.announcement-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: $education-blue;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: $font-size-xs;
}

.announcement-content {
  flex: 1;
}

.announcement-title {
  font-size: $font-size-sm;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.announcement-time {
  font-size: $font-size-xs;
  color: $text-secondary;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .main-container {
    grid-template-columns: 280px 1fr 280px;
  }
}

@media (max-width: 1200px) {
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
  
  .stats-grid,
  .action-items {
    grid-template-columns: 1fr;
  }
}
</style>
