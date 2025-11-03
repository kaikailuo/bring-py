<template>
  <div class="question-analysis">
    <div class="analysis-header">
      <h1 class="page-title">学生问题智能分析</h1>
      <div class="header-actions">
        <el-button type="primary" @click="generateNewSummary">
          <el-icon><Magic /></el-icon>
          生成新总结
        </el-button>
        <el-button @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
      </div>
    </div>

    <div class="analysis-content">
      <!-- 时间范围选择 -->
      <div class="time-range-section education-card">
        <h3>选择分析时间范围</h3>
        <div class="time-controls">
          <el-radio-group v-model="selectedTimeRange" @change="onTimeRangeChange">
            <el-radio-button value="daily">今日</el-radio-button>
            <el-radio-button value="weekly">本周</el-radio-button>
            <el-radio-button value="monthly">本月</el-radio-button>
            <el-radio-button value="custom">自定义</el-radio-button>
          </el-radio-group>
          
          <el-date-picker
            v-if="selectedTimeRange === 'custom'"
            v-model="customDateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="onCustomDateChange"
          />
        </div>
      </div>

      <!-- 问题统计概览 -->
      <div class="stats-overview education-card">
        <h3>问题统计概览</h3>
        <div class="stats-grid">
          <div class="stat-card" v-for="stat in overviewStats" :key="stat.key">
            <div class="stat-icon" :class="stat.type">
              <el-icon><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
              <div class="stat-trend" :class="stat.trend">
                <el-icon><component :is="stat.trendIcon" /></el-icon>
                <span>{{ stat.change }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 问题分类分析 -->
      <div class="category-analysis education-card">
        <h3>问题分类分析</h3>
        <div class="category-chart">
          <div class="chart-container">
            <div class="category-item" v-for="category in categoryStats" :key="category.name">
              <div class="category-header">
                <span class="category-name">{{ category.name }}</span>
                <span class="category-count">{{ category.count }} 个问题</span>
              </div>
              <el-progress 
                :percentage="category.percentage" 
                :stroke-width="12"
                :color="getCategoryColor(category.name)"
              />
              <div class="category-details">
                <span>已解决: {{ category.resolved }}</span>
                <span>待处理: {{ category.pending }}</span>
                <span>解决率: {{ category.resolutionRate }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 常见问题分析 -->
      <div class="common-issues education-card">
        <h3>常见问题分析</h3>
        <div class="issues-list">
          <div class="issue-item" v-for="issue in commonIssues" :key="issue.category">
            <div class="issue-header">
              <div class="issue-icon">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="issue-info">
                <h4>{{ issue.category }}</h4>
                <p>{{ issue.description }}</p>
              </div>
              <div class="issue-stats">
                <el-tag :type="getIssuePriorityType(issue.count)">
                  {{ issue.count }} 次
                </el-tag>
                <span class="issue-percentage">{{ issue.percentage }}%</span>
              </div>
            </div>
            <div class="issue-examples">
              <h5>典型问题示例：</h5>
              <ul>
                <li v-for="example in issue.examples" :key="example">
                  {{ example }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- 智能建议 -->
      <div class="recommendations education-card">
        <h3>智能改进建议</h3>
        <div class="recommendations-list">
          <div class="recommendation-item" v-for="rec in recommendations" :key="rec.id">
            <div class="rec-header">
              <div class="rec-icon" :class="rec.priority">
                <el-icon><component :is="rec.icon" /></el-icon>
              </div>
              <div class="rec-content">
                <h4>{{ rec.title }}</h4>
                <p>{{ rec.description }}</p>
              </div>
              <el-tag :type="getPriorityType(rec.priority)">
                {{ getPriorityText(rec.priority) }}
              </el-tag>
            </div>
            <div class="rec-actions" v-if="rec.actions">
              <el-button 
                v-for="action in rec.actions" 
                :key="action.text"
                :type="action.type"
                size="small"
                @click="executeAction(action)"
              >
                {{ action.text }}
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 问题趋势分析 -->
      <div class="trend-analysis education-card">
        <h3>问题趋势分析</h3>
        <div class="trend-chart">
          <div class="chart-placeholder">
            <el-icon><TrendCharts /></el-icon>
            <p>问题数量趋势图</p>
            <div class="trend-stats">
              <div class="trend-item">
                <span class="trend-label">平均每日问题数</span>
                <span class="trend-value">{{ trendStats.dailyAverage }}</span>
              </div>
              <div class="trend-item">
                <span class="trend-label">问题增长趋势</span>
                <span class="trend-value" :class="trendStats.growthTrend">
                  {{ trendStats.growthRate }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 详细问题列表 -->
      <div class="questions-list education-card">
        <div class="list-header">
          <h3>详细问题列表</h3>
          <div class="list-filters">
            <el-select v-model="questionFilter.status" placeholder="状态筛选" style="width: 120px">
              <el-option label="全部" value="" />
              <el-option label="待处理" value="pending" />
              <el-option label="已回答" value="answered" />
              <el-option label="已解决" value="resolved" />
            </el-select>
            <el-select v-model="questionFilter.category" placeholder="分类筛选" style="width: 120px">
              <el-option label="全部" value="" />
              <el-option 
                v-for="category in categories" 
                :key="category.id" 
                :label="category.name" 
                :value="category.id" 
              />
            </el-select>
          </div>
        </div>
        
        <div class="questions-table">
          <div class="question-row" v-for="question in filteredQuestions" :key="question.id">
            <div class="question-info">
              <div class="question-title">{{ question.title }}</div>
              <div class="question-meta">
                <el-tag size="small" :type="getStatusType(question.status)">
                  {{ getStatusText(question.status) }}
                </el-tag>
                <el-tag size="small" :type="getPriorityType(question.priority)">
                  {{ getPriorityText(question.priority) }}
                </el-tag>
                <span class="question-time">{{ question.created_at }}</span>
              </div>
            </div>
            <div class="question-actions">
              <el-button size="small" @click="viewQuestion(question)">
                查看详情
              </el-button>
              <el-button size="small" type="primary" @click="answerQuestion(question)">
                回答问题
              </el-button>
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

const userStore = useUserStore()

// 响应式数据
const selectedTimeRange = ref('weekly')
const customDateRange = ref([])
const loading = ref(false)

// 统计数据
const overviewStats = ref([
  {
    key: 'total',
    label: '总问题数',
    value: 156,
    change: '+12',
    trend: 'up',
    trendIcon: 'ArrowUp',
    type: 'total',
    icon: 'QuestionFilled'
  },
  {
    key: 'pending',
    label: '待处理',
    value: 12,
    change: '-5',
    trend: 'down',
    trendIcon: 'ArrowDown',
    type: 'pending',
    icon: 'Clock'
  },
  {
    key: 'resolved',
    label: '已解决',
    value: 142,
    change: '+8',
    trend: 'up',
    trendIcon: 'ArrowUp',
    type: 'resolved',
    icon: 'Check'
  },
  {
    key: 'rate',
    label: '解决率',
    value: '91.0%',
    change: '+2.1%',
    trend: 'up',
    trendIcon: 'ArrowUp',
    type: 'rate',
    icon: 'TrendCharts'
  }
])

const categoryStats = ref([
  {
    name: 'Python基础',
    count: 45,
    resolved: 42,
    pending: 3,
    percentage: 28.8,
    resolutionRate: 93.3
  },
  {
    name: '数据结构',
    count: 38,
    resolved: 35,
    pending: 3,
    percentage: 24.4,
    resolutionRate: 92.1
  },
  {
    name: '算法',
    count: 32,
    resolved: 28,
    pending: 4,
    percentage: 20.5,
    resolutionRate: 87.5
  },
  {
    name: '环境配置',
    count: 25,
    resolved: 22,
    pending: 3,
    percentage: 16.0,
    resolutionRate: 88.0
  },
  {
    name: '其他',
    count: 16,
    resolved: 15,
    pending: 1,
    percentage: 10.3,
    resolutionRate: 93.8
  }
])

const commonIssues = ref([
  {
    category: '语法错误',
    count: 23,
    percentage: 14.7,
    description: '学生经常在Python语法使用上出现错误',
    examples: [
      '缩进错误导致IndentationError',
      '变量名拼写错误',
      '缺少冒号或括号'
    ]
  },
  {
    category: '逻辑问题',
    count: 18,
    percentage: 11.5,
    description: '算法逻辑理解不够深入',
    examples: [
      '循环条件设置错误',
      '递归终止条件不明确',
      '变量作用域理解不清'
    ]
  },
  {
    category: '环境配置',
    count: 15,
    percentage: 9.6,
    description: '开发环境配置和依赖安装问题',
    examples: [
      'Python版本不兼容',
      '第三方库安装失败',
      'IDE配置问题'
    ]
  }
])

const recommendations = ref([
  {
    id: 1,
    title: '加强语法基础教学',
    description: '建议在课程中增加更多语法练习，特别是缩进和变量命名规范',
    priority: 'high',
    icon: 'EditPen',
    actions: [
      { text: '创建语法练习', type: 'primary' },
      { text: '查看相关资源', type: 'default' }
    ]
  },
  {
    id: 2,
    title: '增加算法可视化工具',
    description: '使用可视化工具帮助学生理解算法执行过程',
    priority: 'medium',
    icon: 'DataAnalysis',
    actions: [
      { text: '推荐工具', type: 'primary' },
      { text: '制作教程', type: 'default' }
    ]
  },
  {
    id: 3,
    title: '完善环境配置指南',
    description: '制作详细的环境配置教程和常见问题解决方案',
    priority: 'medium',
    icon: 'Setting',
    actions: [
      { text: '更新文档', type: 'primary' },
      { text: '录制视频', type: 'default' }
    ]
  }
])

const trendStats = ref({
  dailyAverage: 5.2,
  growthRate: 12.5,
  growthTrend: 'up'
})

const categories = ref([
  { id: 1, name: 'Python基础' },
  { id: 2, name: '数据结构' },
  { id: 3, name: '算法' },
  { id: 4, name: '环境配置' },
  { id: 5, name: '其他' }
])

const questionFilter = ref({
  status: '',
  category: ''
})

const questions = ref([
  {
    id: 1,
    title: 'Python中如何优雅地处理异常？',
    status: 'resolved',
    priority: 'medium',
    category: 1,
    created_at: '2024-01-20 14:30'
  },
  {
    id: 2,
    title: '数据结构学习心得分享',
    status: 'answered',
    priority: 'low',
    category: 2,
    created_at: '2024-01-20 10:15'
  },
  {
    id: 3,
    title: '快速排序的实现原理',
    status: 'pending',
    priority: 'high',
    category: 3,
    created_at: '2024-01-19 16:45'
  }
])

// 计算属性
const filteredQuestions = computed(() => {
  let filtered = questions.value
  
  if (questionFilter.value.status) {
    filtered = filtered.filter(q => q.status === questionFilter.value.status)
  }
  
  if (questionFilter.value.category) {
    filtered = filtered.filter(q => q.category === questionFilter.value.category)
  }
  
  return filtered
})

// 方法
const onTimeRangeChange = (value) => {
  console.log('时间范围改变:', value)
  loadData()
}

const onCustomDateChange = (dates) => {
  console.log('自定义日期改变:', dates)
  loadData()
}

const generateNewSummary = async () => {
  loading.value = true
  try {
    console.log('生成新总结')
    // 这里应该调用API生成总结
    await new Promise(resolve => setTimeout(resolve, 2000))
    ElMessage.success('总结生成成功')
  } catch (error) {
    console.error('生成总结失败:', error)
    ElMessage.error('生成总结失败')
  } finally {
    loading.value = false
  }
}

const refreshData = async () => {
  loading.value = true
  try {
    console.log('刷新数据')
    await loadData()
    ElMessage.success('数据刷新成功')
  } catch (error) {
    console.error('刷新失败:', error)
    ElMessage.error('刷新失败')
  } finally {
    loading.value = false
  }
}

const loadData = async () => {
  // 这里应该根据时间范围加载数据
  console.log('加载数据')
}

const getCategoryColor = (categoryName) => {
  const colors = {
    'Python基础': '#67c23a',
    '数据结构': '#409eff',
    '算法': '#e6a23c',
    '环境配置': '#f56c6c',
    '其他': '#909399'
  }
  return colors[categoryName] || '#409eff'
}

const getIssuePriorityType = (count) => {
  if (count > 20) return 'danger'
  if (count > 10) return 'warning'
  return 'info'
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

const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    answered: 'info',
    resolved: 'success'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待处理',
    answered: '已回答',
    resolved: '已解决'
  }
  return texts[status] || '未知'
}

const executeAction = (action) => {
  console.log('执行操作:', action.text)
  ElMessage.success(`正在执行: ${action.text}`)
}

const viewQuestion = (question) => {
  console.log('查看问题:', question.title)
}

const answerQuestion = (question) => {
  console.log('回答问题:', question.title)
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
.question-analysis {
  padding: $spacing-xl;
  height: 100%;
  overflow-y: auto;
}

.analysis-header {
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
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-xl;
}

.time-range-section {
  padding: $spacing-xl;
}

.time-range-section h3 {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-lg 0;
}

.time-controls {
  display: flex;
  gap: $spacing-lg;
  align-items: center;
}

.stats-overview {
  padding: $spacing-xl;
}

.stats-overview h3 {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-lg 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: $spacing-lg;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  padding: $spacing-lg;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: white;
  
  &.total {
    background: $education-blue;
  }
  
  &.pending {
    background: $warning-color;
  }
  
  &.resolved {
    background: $success-color;
  }
  
  &.rate {
    background: $education-green;
  }
}

.stat-content {
  flex: 1;
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
  margin-bottom: $spacing-xs;
}

.stat-trend {
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

.category-analysis {
  padding: $spacing-xl;
}

.category-analysis h3 {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-lg 0;
}

.chart-container {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.category-item {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-name {
  font-weight: 500;
  color: $text-primary;
}

.category-count {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.category-details {
  display: flex;
  gap: $spacing-md;
  font-size: $font-size-sm;
  color: $text-secondary;
}

.common-issues {
  padding: $spacing-xl;
}

.common-issues h3 {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-lg 0;
}

.issues-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.issue-item {
  padding: $spacing-lg;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.issue-header {
  display: flex;
  align-items: flex-start;
  gap: $spacing-lg;
  margin-bottom: $spacing-md;
}

.issue-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: $warning-color;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.issue-info {
  flex: 1;
}

.issue-info h4 {
  font-size: $font-size-md;
  font-weight: 500;
  color: $text-primary;
  margin: 0 0 $spacing-xs 0;
}

.issue-info p {
  color: $text-secondary;
  margin: 0;
  line-height: 1.5;
}

.issue-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: $spacing-xs;
  flex-shrink: 0;
}

.issue-percentage {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.issue-examples h5 {
  font-size: $font-size-sm;
  font-weight: 500;
  color: $text-primary;
  margin: 0 0 $spacing-sm 0;
}

.issue-examples ul {
  margin: 0;
  padding-left: $spacing-lg;
}

.issue-examples li {
  font-size: $font-size-sm;
  color: $text-secondary;
  margin-bottom: $spacing-xs;
}

.recommendations {
  padding: $spacing-xl;
}

.recommendations h3 {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-lg 0;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.recommendation-item {
  padding: $spacing-lg;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.rec-header {
  display: flex;
  align-items: flex-start;
  gap: $spacing-lg;
  margin-bottom: $spacing-md;
}

.rec-icon {
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

.rec-content {
  flex: 1;
}

.rec-content h4 {
  font-size: $font-size-md;
  font-weight: 500;
  color: $text-primary;
  margin: 0 0 $spacing-xs 0;
}

.rec-content p {
  color: $text-secondary;
  margin: 0;
  line-height: 1.5;
}

.rec-actions {
  display: flex;
  gap: $spacing-sm;
  margin-top: $spacing-md;
}

.trend-analysis {
  padding: $spacing-xl;
}

.trend-analysis h3 {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-lg 0;
}

.chart-placeholder {
  height: 300px;
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
    margin: 0 0 $spacing-lg 0;
    font-size: $font-size-lg;
  }
}

.trend-stats {
  display: flex;
  gap: $spacing-xl;
}

.trend-item {
  text-align: center;
}

.trend-label {
  display: block;
  font-size: $font-size-sm;
  color: $text-secondary;
  margin-bottom: $spacing-xs;
}

.trend-value {
  display: block;
  font-size: $font-size-xl;
  font-weight: bold;
  color: $text-primary;
  
  &.up {
    color: $success-color;
  }
  
  &.down {
    color: $error-color;
  }
}

.questions-list {
  padding: $spacing-xl;
}

.questions-list h3 {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-lg 0;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
}

.list-filters {
  display: flex;
  gap: $spacing-md;
}

.questions-table {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.question-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-lg;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.question-info {
  flex: 1;
}

.question-title {
  font-size: $font-size-md;
  font-weight: 500;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.question-meta {
  display: flex;
  gap: $spacing-sm;
  align-items: center;
}

.question-time {
  font-size: $font-size-sm;
  color: $text-light;
}

.question-actions {
  display: flex;
  gap: $spacing-sm;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .question-analysis {
    padding: $spacing-lg;
  }
  
  .analysis-header {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
  
  .time-controls {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
  
  .question-row {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
  
  .trend-stats {
    flex-direction: column;
    gap: $spacing-lg;
  }
}
</style>
