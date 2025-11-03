<template>
  <div class="teacher-dashboard">
    <div class="dashboard-header">
      <h1 class="page-title">教学仪表盘</h1>
      <div class="header-actions">
        <el-date-picker
          v-model="selectedDateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          size="small"
        />
        <el-button type="primary" @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
      </div>
    </div>

    <div class="dashboard-content">
      <!-- 关键指标卡片 -->
      <div class="metrics-section">
        <div class="metrics-grid">
          <div class="metric-card education-card" v-for="metric in metrics" :key="metric.id">
            <div class="metric-icon" :class="metric.type">
              <el-icon><component :is="metric.icon" /></el-icon>
            </div>
            <div class="metric-content">
              <div class="metric-title">{{ metric.title }}</div>
              <div class="metric-value">{{ metric.value }}</div>
              <div class="metric-trend" :class="metric.trend">
                <el-icon><component :is="metric.trendIcon" /></el-icon>
                <span>{{ metric.change }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="charts-section">
        <div class="charts-grid">
          <!-- 学生学习进度 -->
          <div class="chart-card education-card">
            <div class="chart-header">
              <h3 class="chart-title">学生学习进度</h3>
              <el-radio-group v-model="progressTimeRange" size="small">
                <el-radio-button value="week">本周</el-radio-button>
                <el-radio-button value="month">本月</el-radio-button>
                <el-radio-button value="semester">本学期</el-radio-button>
              </el-radio-group>
            </div>
            <div class="chart-content">
              <div class="progress-summary">
                <div class="summary-item">
                  <span class="summary-label">完成率</span>
                  <span class="summary-value">{{ learningProgress.completionRate }}%</span>
                </div>
                <div class="summary-item">
                  <span class="summary-label">平均分数</span>
                  <span class="summary-value">{{ learningProgress.averageScore }}</span>
                </div>
                <div class="summary-item">
                  <span class="summary-label">活跃学生</span>
                  <span class="summary-value">{{ learningProgress.activeStudents }}</span>
                </div>
              </div>
              <div class="chart-placeholder">
                <el-icon><TrendCharts /></el-icon>
                <p>学习进度趋势图</p>
              </div>
            </div>
          </div>

          <!-- 课程完成情况 -->
          <div class="chart-card education-card">
            <div class="chart-header">
              <h3 class="chart-title">课程完成情况</h3>
            </div>
            <div class="chart-content">
              <div class="course-progress-list">
                <div class="course-item" v-for="course in courseProgress" :key="course.id">
                  <div class="course-info">
                    <div class="course-name">{{ course.name }}</div>
                    <div class="course-stats">
                      {{ course.completed }}/{{ course.total }} 学生完成
                    </div>
                  </div>
                  <div class="course-progress-bar">
                    <el-progress 
                      :percentage="course.progressPercentage" 
                      :stroke-width="8"
                      :color="getProgressColor(course.progressPercentage)"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 班级概览 -->
      <div class="classes-section">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><UserFilled /></el-icon>
            班级概览
          </h2>
          <el-button type="primary" @click="$router.push('/teacher/class-management')">
            管理班级
          </el-button>
        </div>
        
        <div class="classes-grid">
          <div class="class-card education-card" v-for="classItem in classes" :key="classItem.id">
            <div class="class-header">
              <div class="class-icon">
                <el-icon><UserFilled /></el-icon>
              </div>
              <div class="class-info">
                <h3 class="class-name">{{ classItem.name }}</h3>
                <p class="class-desc">{{ classItem.description }}</p>
              </div>
              <div class="class-status">
                <el-tag :type="classItem.status === 'active' ? 'success' : 'warning'">
                  {{ classItem.status === 'active' ? '进行中' : '已结束' }}
                </el-tag>
              </div>
            </div>
            
            <div class="class-stats">
              <div class="stat-row">
                <div class="stat-item">
                  <span class="stat-label">学生人数</span>
                  <span class="stat-value">{{ classItem.studentCount }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">完成率</span>
                  <span class="stat-value">{{ classItem.completionRate }}%</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">平均分</span>
                  <span class="stat-value">{{ classItem.averageScore }}</span>
                </div>
              </div>
            </div>
            
            <div class="class-actions">
              <el-button size="small" @click="viewClassDetails(classItem)">
                查看详情
              </el-button>
              <el-button size="small" type="primary" @click="manageClass(classItem)">
                管理班级
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 最新活动 -->
      <div class="activity-section">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><Clock /></el-icon>
            最新活动
          </h2>
          <el-button type="text" @click="$router.push('/teacher/analytics')">
            查看全部
          </el-button>
        </div>
        
        <div class="activity-timeline">
          <div class="timeline-item" v-for="activity in recentActivities" :key="activity.id">
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

      <!-- 学生问题总结 -->
      <div class="question-summary-section">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><DataAnalysis /></el-icon>
            学生问题智能总结
          </h2>
          <div class="summary-actions">
            <el-button type="primary" @click="generateSummary">
              <el-icon><Magic /></el-icon>
              生成智能总结
            </el-button>
            <el-button @click="$router.push('/teacher/question-analysis')">
              详细分析
            </el-button>
          </div>
        </div>
        
        <div class="summary-content">
          <div class="summary-cards">
            <div class="summary-card education-card" v-for="summary in questionSummaries" :key="summary.id">
              <div class="summary-header">
                <div class="summary-icon">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="summary-info">
                  <h3 class="summary-title">{{ summary.title }}</h3>
                  <p class="summary-period">{{ summary.period_start }} 至 {{ summary.period_end }}</p>
                </div>
                <div class="summary-stats">
                  <el-tag type="success">{{ summary.resolved_count }}/{{ summary.question_count }} 已解决</el-tag>
                </div>
              </div>
              
              <div class="summary-preview">
                <p>{{ summary.content.substring(0, 100) }}...</p>
              </div>
              
              <div class="summary-actions">
                <el-button size="small" @click="viewSummaryDetail(summary)">
                  查看详情
                </el-button>
                <el-button size="small" type="primary" @click="downloadSummary(summary)">
                  下载报告
                </el-button>
              </div>
            </div>
          </div>
          
          <!-- 问题统计概览 -->
          <div class="question-stats education-card">
            <div class="stats-header">
              <h3>问题统计概览</h3>
              <el-button size="small" @click="refreshQuestionStats">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </div>
            
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">{{ questionStats.total_questions || 0 }}</div>
                <div class="stat-label">总问题数</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ questionStats.pending_questions || 0 }}</div>
                <div class="stat-label">待处理</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ questionStats.resolved_questions || 0 }}</div>
                <div class="stat-label">已解决</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ questionStats.answered_questions || 0 }}</div>
                <div class="stat-label">已回答</div>
              </div>
            </div>
            
            <!-- 分类分布 -->
            <div class="category-distribution" v-if="questionStats.category_distribution">
              <h4>问题分类分布</h4>
              <div class="category-list">
                <div class="category-item" v-for="(count, category) in questionStats.category_distribution" :key="category">
                  <span class="category-name">{{ category }}</span>
                  <el-progress 
                    :percentage="(count / questionStats.total_questions) * 100" 
                    :stroke-width="8"
                    :show-text="false"
                  />
                  <span class="category-count">{{ count }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 待处理事项 -->
      <div class="pending-section">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><Warning /></el-icon>
            待处理事项
          </h2>
          <el-button type="primary" @click="handleAllPending">
            批量处理
          </el-button>
        </div>
        
        <div class="pending-grid">
          <div class="pending-card education-card" v-for="pending in pendingItems" :key="pending.id">
            <div class="pending-header">
              <div class="pending-icon" :class="pending.priority">
                <el-icon><component :is="pending.icon" /></el-icon>
              </div>
              <div class="pending-info">
                <h4 class="pending-title">{{ pending.title }}</h4>
                <p class="pending-desc">{{ pending.description }}</p>
              </div>
              <div class="pending-meta">
                <el-tag size="small" :type="getPriorityType(pending.priority)">
                  {{ getPriorityText(pending.priority) }}
                </el-tag>
                <span class="pending-time">{{ pending.time }}</span>
              </div>
            </div>
            
            <div class="pending-actions">
              <el-button size="small" type="primary" @click="handlePending(pending)">
                立即处理
              </el-button>
              <el-button size="small" @click="viewPendingDetails(pending)">
                查看详情
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 问题总结生成对话框 -->
    <QuestionSummaryDialog 
      v-model="showSummaryDialog" 
      @generate="handleSummaryGenerate"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import QuestionSummaryDialog from '@/components/QuestionSummaryDialog.vue'

const userStore = useUserStore()

// 响应式数据
const selectedDateRange = ref([])
const progressTimeRange = ref('month')

// 问题总结相关数据
const questionSummaries = ref([])
const questionStats = ref({})
const summaryLoading = ref(false)
const showSummaryDialog = ref(false)

const metrics = ref([
  {
    id: 1,
    title: '总学生数',
    value: '156',
    change: '+12',
    trend: 'up',
    trendIcon: 'ArrowUp',
    type: 'students',
    icon: 'User'
  },
  {
    id: 2,
    title: '活跃课程',
    value: '8',
    change: '+2',
    trend: 'up',
    trendIcon: 'ArrowUp',
    type: 'courses',
    icon: 'Reading'
  },
  {
    id: 3,
    title: '平均完成率',
    value: '78%',
    change: '-3%',
    trend: 'down',
    trendIcon: 'ArrowDown',
    type: 'completion',
    icon: 'TrendCharts'
  },
  {
    id: 4,
    title: '待回答问题',
    value: '12',
    change: '-5',
    trend: 'down',
    trendIcon: 'ArrowDown',
    type: 'questions',
    icon: 'QuestionFilled'
  }
])

const learningProgress = ref({
  completionRate: 78,
  averageScore: 85.6,
  activeStudents: 142
})

const courseProgress = ref([
  {
    id: 1,
    name: 'Python基础语法',
    completed: 45,
    total: 52,
    progressPercentage: 87
  },
  {
    id: 2,
    name: '数据结构入门',
    completed: 38,
    total: 52,
    progressPercentage: 73
  },
  {
    id: 3,
    name: '算法基础',
    completed: 29,
    total: 52,
    progressPercentage: 56
  },
  {
    id: 4,
    name: '面向对象编程',
    completed: 15,
    total: 52,
    progressPercentage: 29
  }
])

const classes = ref([
  {
    id: 1,
    name: '高一(1)班',
    description: 'Python编程基础课程',
    status: 'active',
    studentCount: 52,
    completionRate: 87,
    averageScore: 88.5
  },
  {
    id: 2,
    name: '高一(2)班',
    description: '数据结构与算法',
    status: 'active',
    studentCount: 48,
    completionRate: 73,
    averageScore: 82.3
  },
  {
    id: 3,
    name: '高二(1)班',
    description: 'Python进阶编程',
    status: 'active',
    studentCount: 56,
    completionRate: 92,
    averageScore: 91.2
  }
])

const recentActivities = ref([
  {
    id: 1,
    type: 'assignment',
    icon: 'EditPen',
    title: '批改作业完成',
    description: '已完成高一(1)班Python基础作业批改',
    time: '2小时前'
  },
  {
    id: 2,
    type: 'question',
    icon: 'QuestionFilled',
    title: '回答学生问题',
    description: '解答了关于列表操作的编程问题',
    time: '4小时前'
  },
  {
    id: 3,
    type: 'resource',
    icon: 'Document',
    title: '上传新资源',
    description: '上传了数据结构课件到资源库',
    time: '1天前'
  },
  {
    id: 4,
    type: 'grade',
    icon: 'Trophy',
    title: '成绩统计完成',
    description: '完成了本月学习进度统计',
    time: '2天前'
  }
])

const pendingItems = ref([
  {
    id: 1,
    title: '批改作业',
    description: '高一(2)班数据结构作业待批改',
    priority: 'high',
    icon: 'EditPen',
    time: '3小时前'
  },
  {
    id: 2,
    title: '学生提问',
    description: '王同学关于递归算法的问题',
    priority: 'medium',
    icon: 'QuestionFilled',
    time: '5小时前'
  },
  {
    id: 3,
    title: '资源审核',
    description: '新上传的Python教程待审核',
    priority: 'low',
    icon: 'Document',
    time: '1天前'
  },
  {
    id: 4,
    title: '班级报告',
    description: '生成本月班级学习报告',
    priority: 'medium',
    icon: 'DataAnalysis',
    time: '2天前'
  }
])

// 计算属性
const getProgressColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#e6a23c'
  return '#f56c6c'
}

const getPriorityType = (priority) => {
  const types = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  }
  return types[priority] || 'info'
}

const getPriorityText = (priority) => {
  const texts = {
    high: '高优先级',
    medium: '中优先级',
    low: '低优先级'
  }
  return texts[priority] || '未知'
}

// 方法
const refreshData = () => {
  console.log('刷新数据')
  // 模拟数据刷新
}

const viewClassDetails = (classItem) => {
  console.log('查看班级详情:', classItem.name)
}

const manageClass = (classItem) => {
  console.log('管理班级:', classItem.name)
}

const handlePending = (pending) => {
  console.log('处理待办事项:', pending.title)
}

const viewPendingDetails = (pending) => {
  console.log('查看待办详情:', pending.title)
}

const handleAllPending = () => {
  console.log('批量处理待办事项')
}

// 问题总结相关方法
const generateSummary = () => {
  showSummaryDialog.value = true
}

const handleSummaryGenerate = async (summaryData) => {
  summaryLoading.value = true
  try {
    console.log('生成问题总结:', summaryData)
    // 这里应该调用API生成总结
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 刷新总结列表
    await loadQuestionSummaries()
    
    ElMessage.success('问题总结生成成功')
  } catch (error) {
    console.error('生成总结失败:', error)
    ElMessage.error('生成总结失败')
  } finally {
    summaryLoading.value = false
  }
}

const loadQuestionSummaries = async () => {
  try {
    // 这里应该调用API获取总结列表
    console.log('加载问题总结列表')
    // 模拟数据
    questionSummaries.value = [
      {
        id: 1,
        title: '本周问题总结',
        content: '本周共收到45个学生问题，主要集中在Python语法错误和算法理解方面。已解决38个问题，解决率为84.4%。',
        period_start: '2024-01-15',
        period_end: '2024-01-21',
        question_count: 45,
        resolved_count: 38
      },
      {
        id: 2,
        title: '本月问题总结',
        content: '本月共收到156个学生问题，问题分类分布较为均匀。已解决142个问题，解决率为91.0%。',
        period_start: '2024-01-01',
        period_end: '2024-01-31',
        question_count: 156,
        resolved_count: 142
      }
    ]
  } catch (error) {
    console.error('加载总结失败:', error)
  }
}

const loadQuestionStats = async () => {
  try {
    // 这里应该调用API获取问题统计
    console.log('加载问题统计')
    // 模拟数据
    questionStats.value = {
      total_questions: 156,
      pending_questions: 12,
      resolved_questions: 142,
      answered_questions: 145,
      category_distribution: {
        'Python基础': 45,
        '数据结构': 38,
        '算法': 32,
        '环境配置': 25,
        '其他': 16
      }
    }
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

const refreshQuestionStats = async () => {
  await loadQuestionStats()
  ElMessage.success('统计数据已刷新')
}

const viewSummaryDetail = (summary) => {
  console.log('查看总结详情:', summary.title)
  // 跳转到详细页面
  this.$router.push(`/teacher/question-analysis/${summary.id}`)
}

const downloadSummary = (summary) => {
  console.log('下载总结报告:', summary.title)
  // 实现下载功能
  ElMessage.success('报告下载已开始')
}

onMounted(() => {
  // 初始化数据
  loadQuestionSummaries()
  loadQuestionStats()
})
</script>

<style lang="scss" scoped>
.teacher-dashboard {
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

.header-actions {
  display: flex;
  gap: $spacing-md;
  align-items: center;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-xxl;
}

/* 关键指标 */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: $spacing-lg;
}

.metric-card {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  padding: $spacing-xl;
}

.metric-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  
  &.students {
    background: $education-blue;
  }
  
  &.courses {
    background: $education-green;
  }
  
  &.completion {
    background: $education-orange;
  }
  
  &.questions {
    background: $education-purple;
  }
}

.metric-content {
  flex: 1;
}

.metric-title {
  font-size: $font-size-sm;
  color: $text-secondary;
  margin-bottom: $spacing-xs;
}

.metric-value {
  font-size: 2rem;
  font-weight: bold;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.metric-trend {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  font-size: $font-size-sm;
  
  &.up {
    color: $success-color;
  }
  
  &.down {
    color: $error-color;
  }
}

/* 图表区域 */
.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: $spacing-lg;
}

.chart-card {
  padding: $spacing-xl;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
}

.chart-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0;
}

.chart-content {
  height: 300px;
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.progress-summary {
  display: flex;
  justify-content: space-around;
  padding: $spacing-lg;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.summary-item {
  text-align: center;
}

.summary-label {
  display: block;
  font-size: $font-size-sm;
  color: $text-secondary;
  margin-bottom: $spacing-xs;
}

.summary-value {
  display: block;
  font-size: $font-size-xl;
  font-weight: bold;
  color: $text-primary;
}

.chart-placeholder {
  flex: 1;
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
}

.course-progress-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.course-item {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.course-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-name {
  font-size: $font-size-md;
  font-weight: 500;
  color: $text-primary;
}

.course-stats {
  font-size: $font-size-sm;
  color: $text-secondary;
}

/* 班级概览 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
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

.classes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: $spacing-lg;
}

.class-card {
  padding: $spacing-xl;
}

.class-header {
  display: flex;
  align-items: flex-start;
  gap: $spacing-lg;
  margin-bottom: $spacing-lg;
}

.class-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: $education-green;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.class-info {
  flex: 1;
}

.class-name {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-xs 0;
}

.class-desc {
  color: $text-secondary;
  font-size: $font-size-sm;
  margin: 0;
  line-height: 1.5;
}

.class-status {
  flex-shrink: 0;
}

.class-stats {
  margin-bottom: $spacing-lg;
}

.stat-row {
  display: flex;
  justify-content: space-between;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: $font-size-xs;
  color: $text-secondary;
  margin-bottom: $spacing-xs;
}

.stat-value {
  display: block;
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
}

.class-actions {
  display: flex;
  gap: $spacing-sm;
}

/* 最新活动 */
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
  
  &.assignment {
    background: $education-blue;
  }
  
  &.question {
    background: $education-green;
  }
  
  &.resource {
    background: $education-orange;
  }
  
  &.grade {
    background: $education-purple;
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

/* 待处理事项 */
.pending-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: $spacing-lg;
}

.pending-card {
  padding: $spacing-xl;
}

.pending-header {
  display: flex;
  align-items: flex-start;
  gap: $spacing-lg;
  margin-bottom: $spacing-lg;
}

.pending-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  color: white;
  flex-shrink: 0;
  
  &.high {
    background: $error-color;
  }
  
  &.medium {
    background: $warning-color;
  }
  
  &.low {
    background: $info-color;
  }
}

.pending-info {
  flex: 1;
}

.pending-title {
  font-size: $font-size-md;
  font-weight: 500;
  color: $text-primary;
  margin: 0 0 $spacing-xs 0;
}

.pending-desc {
  color: $text-secondary;
  font-size: $font-size-sm;
  margin: 0;
  line-height: 1.5;
}

.pending-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: $spacing-xs;
  flex-shrink: 0;
}

.pending-time {
  font-size: $font-size-xs;
  color: $text-light;
}

.pending-actions {
  display: flex;
  gap: $spacing-sm;
}

/* 问题总结样式 */
.question-summary-section {
  margin-bottom: $spacing-xxl;
}

.summary-actions {
  display: flex;
  gap: $spacing-md;
}

.summary-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: $spacing-lg;
}

.summary-card {
  padding: $spacing-xl;
}

.summary-header {
  display: flex;
  align-items: flex-start;
  gap: $spacing-lg;
  margin-bottom: $spacing-lg;
}

.summary-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: $education-blue;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.summary-info {
  flex: 1;
}

.summary-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-xs 0;
}

.summary-period {
  color: $text-secondary;
  font-size: $font-size-sm;
  margin: 0;
}

.summary-stats {
  flex-shrink: 0;
}

.summary-preview {
  margin-bottom: $spacing-lg;
}

.summary-preview p {
  color: $text-secondary;
  line-height: 1.6;
  margin: 0;
}

.summary-actions {
  display: flex;
  gap: $spacing-sm;
}

.question-stats {
  padding: $spacing-xl;
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
}

.stats-header h3 {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: $spacing-lg;
  margin-bottom: $spacing-lg;
}

.stat-item {
  text-align: center;
  padding: $spacing-md;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.stat-label {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.category-distribution h4 {
  font-size: $font-size-md;
  font-weight: 500;
  color: $text-primary;
  margin: 0 0 $spacing-md 0;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.category-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.category-name {
  min-width: 80px;
  font-size: $font-size-sm;
  color: $text-primary;
}

.category-count {
  min-width: 30px;
  text-align: right;
  font-size: $font-size-sm;
  color: $text-secondary;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-cards {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .teacher-dashboard {
    padding: $spacing-lg;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .metrics-grid,
  .classes-grid,
  .pending-grid {
    grid-template-columns: 1fr;
  }
  
  .metric-card {
    flex-direction: column;
    text-align: center;
  }
  
  .class-header {
    flex-direction: column;
    text-align: center;
  }
  
  .stat-row {
    flex-direction: column;
    gap: $spacing-md;
  }
  
  .activity-timeline {
    padding-left: $spacing-md;
  }
  
  .timeline-dot {
    left: -16px;
    width: 32px;
    height: 32px;
  }
}
</style>
