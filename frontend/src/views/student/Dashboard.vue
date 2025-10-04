<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1 class="page-title">学习仪表盘</h1>
      <div class="welcome-message">
        <span class="greeting">你好，{{ userStore.userName }}！</span>
        <span class="date">{{ currentDate }}</span>
      </div>
    </div>

    <div class="dashboard-content">
      <!-- 学习概览 -->
      <div class="overview-section">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><TrendCharts /></el-icon>
            学习概览
          </h2>
          <div class="section-actions">
            <el-button-group size="small" class="view-switcher">
              <el-button 
                :type="currentView === 'overview' ? 'primary' : 'default'"
                @click="switchView('overview')"
              >
                概览
              </el-button>
              <el-button 
                :type="currentView === 'detailed' ? 'primary' : 'default'"
                @click="switchView('detailed')"
              >
                详细
              </el-button>
              <el-button 
                :type="currentView === 'progress' ? 'primary' : 'default'"
                @click="switchView('progress')"
              >
                进度
              </el-button>
            </el-button-group>
            <el-button type="primary" @click="$router.push('/student/practice')">
              继续学习
            </el-button>
          </div>
        </div>
        
        <!-- 滑动视图容器 -->
        <div class="dashboard-swipe">
          <SwipeContainer
            :items="dashboardViews"
            :items-per-view="1"
            :autoplay="false"
            :show-indicators="false"
            :show-navigation="false"
            :loop="false"
            ref="swipeRef"
            @slide-change="onViewChange"
          >
            <template #default="{ item }">
              <component :is="item.component" :data="item.data" />
            </template>
          </SwipeContainer>
        </div>
      </div>

      <!-- 课程进度 -->
      <div class="courses-section">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><Reading /></el-icon>
            我的课程
          </h2>
          <el-button type="text" @click="$router.push('/student/resources')">
            查看全部
          </el-button>
        </div>
        
        <div class="courses-grid">
          <div class="course-card education-card" v-for="course in courses" :key="course.id">
            <div class="course-header">
              <div class="course-icon" :class="course.status">
                <el-icon><component :is="course.icon" /></el-icon>
              </div>
              <div class="course-info">
                <h3 class="course-title">{{ course.title }}</h3>
                <p class="course-desc">{{ course.description }}</p>
              </div>
            </div>
            
            <div class="course-progress">
              <div class="progress-info">
                <span class="progress-label">学习进度</span>
                <span class="progress-percentage">{{ course.progress }}%</span>
              </div>
              <el-progress :percentage="course.progress" :stroke-width="8" />
            </div>
            
            <div class="course-actions">
              <el-button 
                type="primary" 
                size="small" 
                @click="startCourse(course)"
                :disabled="course.status === 'locked'"
              >
                {{ course.status === 'completed' ? '复习' : course.status === 'in-progress' ? '继续' : '开始' }}
              </el-button>
              <el-button size="small" @click="viewCourseDetails(course)">
                详情
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习活动 -->
      <div class="activity-section">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><Clock /></el-icon>
            最近活动
          </h2>
        </div>
        
        <div class="activity-timeline">
          <div class="timeline-item" v-for="activity in activities" :key="activity.id">
            <div class="timeline-dot" :class="activity.type">
              <el-icon><component :is="activity.icon" /></el-icon>
            </div>
            <div class="timeline-content">
              <div class="activity-title">{{ activity.title }}</div>
              <div class="activity-desc">{{ activity.description }}</div>
              <div class="activity-time">{{ activity.time }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习统计图表 -->
      <div class="charts-section">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><DataAnalysis /></el-icon>
            学习统计
          </h2>
          <el-radio-group v-model="chartPeriod" size="small">
            <el-radio-button value="week">本周</el-radio-button>
            <el-radio-button value="month">本月</el-radio-button>
            <el-radio-button value="year">本年</el-radio-button>
          </el-radio-group>
        </div>
        
        <div class="charts-grid">
          <div class="chart-card education-card">
            <h3 class="chart-title">学习时长统计</h3>
            <div class="chart-placeholder">
              <el-icon><TrendCharts /></el-icon>
              <p>学习时长图表</p>
              <small>显示{{ chartPeriod }}的学习时长变化</small>
            </div>
          </div>
          
          <div class="chart-card education-card">
            <h3 class="chart-title">知识点掌握度</h3>
            <div class="chart-placeholder">
              <el-icon><PieChart /></el-icon>
              <p>知识点掌握度雷达图</p>
              <small>各知识点的掌握情况分析</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import SwipeContainer from '@/components/SwipeContainer.vue'
import OverviewView from '@/components/dashboard/OverviewView.vue'
import DetailedView from '@/components/dashboard/DetailedView.vue'
import ProgressView from '@/components/dashboard/ProgressView.vue'

const userStore = useUserStore()

// 响应式数据
const chartPeriod = ref('week')
const currentView = ref('overview')
const swipeRef = ref(null)

// 计算属性
const currentDate = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})

// 模拟数据
const courses = ref([
  {
    id: 1,
    title: 'Python基础语法',
    description: '学习Python的基本语法和数据类型',
    progress: 100,
    status: 'completed',
    icon: 'Check'
  },
  {
    id: 2,
    title: '数据结构与算法',
    description: '掌握常用的数据结构和算法思想',
    progress: 75,
    status: 'in-progress',
    icon: 'Clock'
  },
  {
    id: 3,
    title: '面向对象编程',
    description: '深入理解面向对象编程概念',
    progress: 30,
    status: 'in-progress',
    icon: 'Box'
  },
  {
    id: 4,
    title: 'Web开发入门',
    description: '学习使用Python进行Web开发',
    progress: 0,
    status: 'locked',
    icon: 'Lock'
  }
])

const activities = ref([
  {
    id: 1,
    type: 'completed',
    icon: 'Check',
    title: '完成Python基础语法课程',
    description: '成功完成了所有章节的学习和练习',
    time: '2小时前'
  },
  {
    id: 2,
    type: 'practice',
    icon: 'EditPen',
    title: '完成编程练习',
    description: '解决了3道数据结构相关的编程题',
    time: '5小时前'
  },
  {
    id: 3,
    type: 'achievement',
    icon: 'Trophy',
    title: '获得新徽章',
    description: '恭喜获得"Python新手"徽章',
    time: '1天前'
  },
  {
    id: 4,
    type: 'forum',
    icon: 'ChatDotRound',
    title: '参与讨论',
    description: '在论坛中回答了关于列表操作的问题',
    time: '2天前'
  }
])

// 仪表盘视图数据
const dashboardViews = computed(() => [
  {
    id: 'overview',
    component: OverviewView,
    data: {
      completedCourses: 8,
      completedPercentage: 67,
      inProgressCourses: 3,
      inProgressPercentage: 45,
      practiceCount: 24,
      practicePercentage: 80,
      achievements: 5
    }
  },
  {
    id: 'detailed',
    component: DetailedView,
    data: {
      todayStudyTime: '2小时30分',
      weekStudyTime: '12小时45分',
      totalStudyTime: '156小时',
      codeCompletionRate: 85,
      exerciseAccuracy: 92,
      knowledgeMastery: 78,
      recentAchievements: [
        {
          id: 1,
          name: 'Python新手',
          description: '完成第一个Python程序',
          date: '2天前',
          icon: 'Trophy'
        },
        {
          id: 2,
          name: '代码大师',
          description: '连续7天完成编程练习',
          date: '1周前',
          icon: 'Star'
        },
        {
          id: 3,
          name: '学习达人',
          description: '完成10个学习模块',
          date: '2周前',
          icon: 'Medal'
        }
      ]
    }
  },
  {
    id: 'progress',
    component: ProgressView,
    data: {
      overallProgress: 67,
      completedModules: 8,
      totalModules: 12,
      weeklyProgress: [
        { day: '周一', progress: 80, time: '2h' },
        { day: '周二', progress: 60, time: '1.5h' },
        { day: '周三', progress: 90, time: '2.5h' },
        { day: '周四', progress: 45, time: '1h' },
        { day: '周五', progress: 70, time: '1.8h' },
        { day: '周六', progress: 0, time: '0h' },
        { day: '周日', progress: 85, time: '2.2h' }
      ],
      modules: [
        {
          id: 1,
          name: 'Python基础语法',
          description: '学习Python的基本语法和数据类型',
          progress: 100,
          status: 'completed',
          icon: 'Check'
        },
        {
          id: 2,
          name: '数据结构与算法',
          description: '掌握常用的数据结构和算法思想',
          progress: 75,
          status: 'in-progress',
          icon: 'Clock'
        },
        {
          id: 3,
          name: '面向对象编程',
          description: '深入理解面向对象编程概念',
          progress: 30,
          status: 'in-progress',
          icon: 'Box'
        },
        {
          id: 4,
          name: 'Web开发入门',
          description: '学习使用Python进行Web开发',
          progress: 0,
          status: 'locked',
          icon: 'Lock'
        }
      ]
    }
  }
])

// 方法
const switchView = (view) => {
  currentView.value = view
  const viewIndex = dashboardViews.value.findIndex(v => v.id === view)
  if (swipeRef.value && viewIndex !== -1) {
    swipeRef.value.goToSlide(viewIndex)
  }
}

const onViewChange = (index) => {
  const view = dashboardViews.value[index]
  if (view) {
    currentView.value = view.id
  }
}

const startCourse = (course) => {
  console.log('开始课程:', course.title)
  // 跳转到课程详情页面
}

const viewCourseDetails = (course) => {
  console.log('查看课程详情:', course.title)
  // 跳转到课程详情页面
}

onMounted(() => {
  // 初始化数据
})
</script>

<style lang="scss" scoped>
.dashboard {
  padding: $spacing-xl;
  height: 100%;
  overflow-y: auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-xl;
  padding-bottom: $spacing-lg;
  border-bottom: 1px solid $border-color;
}

.page-title {
  font-size: 2rem;
  font-weight: bold;
  color: $text-primary;
  margin: 0;
}

.welcome-message {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: $spacing-xs;
}

.greeting {
  font-size: $font-size-lg;
  color: $text-primary;
  font-weight: 500;
}

.date {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-xxl;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
}

.section-actions {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.view-switcher {
  border-radius: $border-radius;
}

.dashboard-swipe {
  width: 100%;
  min-height: 400px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: $font-size-xl;
  font-weight: bold;
  color: $text-primary;
  margin: 0;
}

/* 学习概览 */
.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: $spacing-lg;
}

.overview-card {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  padding: $spacing-xl;
}

.card-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  
  &.completed {
    background: $success-color;
  }
  
  &.in-progress {
    background: $warning-color;
  }
  
  &.practice {
    background: $education-blue;
  }
  
  &.achievements {
    background: $education-purple;
  }
}

.card-content {
  flex: 1;
}

.card-title {
  font-size: $font-size-sm;
  color: $text-secondary;
  margin-bottom: $spacing-xs;
}

.card-value {
  font-size: 2rem;
  font-weight: bold;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.card-progress {
  width: 100%;
}

/* 课程进度 */
.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: $spacing-lg;
}

.course-card {
  padding: $spacing-xl;
}

.course-header {
  display: flex;
  align-items: flex-start;
  gap: $spacing-lg;
  margin-bottom: $spacing-lg;
}

.course-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: white;
  
  &.completed {
    background: $success-color;
  }
  
  &.in-progress {
    background: $warning-color;
  }
  
  &.locked {
    background: $text-light;
  }
}

.course-info {
  flex: 1;
}

.course-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-xs 0;
}

.course-desc {
  color: $text-secondary;
  font-size: $font-size-sm;
  margin: 0;
  line-height: 1.5;
}

.course-progress {
  margin-bottom: $spacing-lg;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-sm;
}

.progress-label {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.progress-percentage {
  font-size: $font-size-sm;
  font-weight: bold;
  color: $education-blue;
}

.course-actions {
  display: flex;
  gap: $spacing-sm;
}

/* 学习活动 */
.activity-timeline {
  position: relative;
  padding-left: $spacing-lg;
}

.activity-timeline::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: $border-color;
}

.timeline-item {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: $spacing-lg;
  margin-bottom: $spacing-xl;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.timeline-dot {
  position: absolute;
  left: -24px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  color: white;
  z-index: 1;
  
  &.completed {
    background: $success-color;
  }
  
  &.practice {
    background: $education-blue;
  }
  
  &.achievement {
    background: $education-purple;
  }
  
  &.forum {
    background: $education-green;
  }
}

.timeline-content {
  flex: 1;
  padding-top: $spacing-xs;
}

.activity-title {
  font-size: $font-size-md;
  font-weight: 500;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.activity-desc {
  font-size: $font-size-sm;
  color: $text-secondary;
  margin-bottom: $spacing-xs;
  line-height: 1.5;
}

.activity-time {
  font-size: $font-size-xs;
  color: $text-light;
}

/* 学习统计图表 */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: $spacing-lg;
}

.chart-card {
  padding: $spacing-xl;
}

.chart-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-lg 0;
  text-align: center;
}

.chart-placeholder {
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: $bg-secondary;
  border-radius: $border-radius;
  color: $text-secondary;
  
  .el-icon {
    font-size: 3rem;
    margin-bottom: $spacing-md;
  }
  
  p {
    font-size: $font-size-md;
    margin: 0 0 $spacing-xs 0;
  }
  
  small {
    font-size: $font-size-xs;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dashboard {
    padding: $spacing-lg;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
  
  .section-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .overview-cards,
  .courses-grid,
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .overview-card {
    flex-direction: column;
    text-align: center;
  }
  
  .course-header {
    flex-direction: column;
    text-align: center;
  }
  
  .activity-timeline {
    padding-left: $spacing-md;
  }
  
  .timeline-dot {
    left: -16px;
    width: 32px;
    height: 32px;
  }
  
  .dashboard-swipe {
    min-height: 300px;
  }
}

@media (max-width: 480px) {
  .section-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .view-switcher {
    width: 100%;
    justify-content: center;
  }
}
</style>
