<template>
  <div class="analytics-page">
    <div class="page-header">
      <h1 class="page-title">
        <el-icon><DataAnalysis /></el-icon>
        学情分析
      </h1>
      <div class="header-actions">
        <el-button type="primary" @click="loadData" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
      </div>
    </div>

    <div class="analytics-content">
      <!-- 统计卡片 -->
      <div class="stats-cards">
        <div class="stat-card education-card">
          <div class="stat-icon students">
            <el-icon><User /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">学生总数</div>
            <div class="stat-value">{{ stats.total_students || 0 }}</div>
          </div>
        </div>
        <div class="stat-card education-card">
          <div class="stat-icon attempts">
            <el-icon><EditPen /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">总答题次数</div>
            <div class="stat-value">{{ totalAttempts }}</div>
          </div>
        </div>
        <div class="stat-card education-card">
          <div class="stat-icon problems">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">平均答题数</div>
            <div class="stat-value">{{ averageAttempts }}</div>
          </div>
        </div>
        <div class="stat-card education-card">
          <div class="stat-icon pass-rate">
            <el-icon><CircleCheck /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">平均通过率</div>
            <div class="stat-value">{{ averagePassRate }}%</div>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="charts-section">
        <div class="chart-card education-card">
          <div class="chart-header">
            <h3 class="chart-title">学生答题数统计</h3>
            <div class="chart-controls">
              <el-radio-group v-model="chartType" size="small" @change="updateChart">
                <el-radio-button value="attempts">答题次数</el-radio-button>
                <el-radio-button value="problems">答题题目数</el-radio-button>
                <el-radio-button value="passed">通过题目数</el-radio-button>
              </el-radio-group>
            </div>
          </div>
          <div class="chart-container">
            <div ref="chartContainer" class="chart" style="width: 100%; height: 400px;"></div>
          </div>
        </div>
      </div>

      <!-- 数据表格 -->
      <div class="table-section">
        <div class="table-card education-card">
          <div class="table-header">
            <h3 class="table-title">学生答题详情</h3>
            <el-input
              v-model="searchKeyword"
              placeholder="搜索学生姓名"
              clearable
              style="width: 200px"
              @input="filterStudents"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
          <el-table
            :data="filteredStudents"
            style="width: 100%"
            stripe
            :loading="loading"
            empty-text="暂无数据"
          >
            <el-table-column prop="student_name" label="学生姓名" width="150" />
            <el-table-column prop="username" label="用户名" width="120" />
            <el-table-column prop="total_attempts" label="总答题次数" width="120" sortable>
              <template #default="{ row }">
                <el-tag type="info">{{ row.total_attempts }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="total_problems" label="答题题目数" width="120" sortable>
              <template #default="{ row }">
                <el-tag type="success">{{ row.total_problems }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="total_passed" label="通过题目数" width="120" sortable>
              <template #default="{ row }">
                <el-tag type="success">{{ row.total_passed }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="pass_rate" label="通过率" width="120" sortable>
              <template #default="{ row }">
                <el-progress
                  :percentage="row.pass_rate"
                  :color="getPassRateColor(row.pass_rate)"
                  :stroke-width="8"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  link
                  size="small"
                  @click="viewStudentDetail(row)"
                >
                  查看详情
                </el-button>
                <el-button
                  type="success"
                  link
                  size="small"
                  @click="analyzeStudent(row)"
                  :loading="analyzingStudentId === row.student_id"
                >
                  AI分析
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>

    <!-- 学生答题详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      :title="`${currentStudent?.student_name || ''} - 答题详情`"
      width="80%"
      @close="closeDetailDialog"
    >
      <div v-if="studentDetail" class="student-detail">
        <!-- 学生信息 -->
        <div class="detail-header">
          <div class="student-info">
            <h3>{{ studentDetail.student?.name }}</h3>
            <p>用户名: {{ studentDetail.student?.username }}</p>
          </div>
          <div class="detail-stats">
            <el-statistic title="总答题数" :value="studentDetail.results?.length || 0" />
            <el-statistic title="通过题目" :value="studentDetail.results?.filter(r => r.passed).length || 0" />
          </div>
        </div>

        <el-divider />

        <!-- 按课程分组显示 -->
        <div v-if="studentDetail.lesson_stats && studentDetail.lesson_stats.length > 0" class="lesson-stats">
          <h4>课程统计</h4>
          <el-table :data="studentDetail.lesson_stats" style="width: 100%; margin-bottom: 20px">
            <el-table-column prop="lesson" label="课程" />
            <el-table-column prop="total_problems" label="题目数" />
            <el-table-column prop="passed_problems" label="通过数" />
            <el-table-column prop="total_attempts" label="总尝试次数" />
            <el-table-column label="通过率">
              <template #default="{ row }">
                <el-progress
                  :percentage="Math.round((row.passed_problems / row.total_problems * 100) || 0)"
                  :color="getPassRateColor((row.passed_problems / row.total_problems * 100) || 0)"
                />
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 详细答题记录 -->
        <div class="detail-results">
          <h4>详细答题记录</h4>
          <el-table
            :data="studentDetail.results"
            style="width: 100%"
            stripe
            max-height="400"
          >
            <el-table-column prop="problem_title" label="题目" width="250" />
            <el-table-column prop="lesson" label="课程" width="120" />
            <el-table-column prop="problem" label="题号" width="100" />
            <el-table-column prop="attempts" label="尝试次数" width="120">
              <template #default="{ row }">
                <el-tag :type="row.attempts > 3 ? 'warning' : 'success'">
                  {{ row.attempts }} 次
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="passed" label="是否通过" width="120">
              <template #default="{ row }">
                <el-tag :type="row.passed ? 'success' : 'danger'">
                  {{ row.passed ? '通过' : '未通过' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="last_submitted_at" label="最后提交时间" width="180">
              <template #default="{ row }">
                {{ row.last_submitted_at ? new Date(row.last_submitted_at).toLocaleString('zh-CN') : '-' }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  link
                  size="small"
                  @click="viewProblemDetail(row)"
                  v-if="row.problem_path"
                >
                  查看题目
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
      <div v-else class="loading-placeholder">
        <el-icon class="is-loading"><Loading /></el-icon>
        <p>加载中...</p>
      </div>
    </el-dialog>

    <!-- AI分析结果对话框 -->
    <el-dialog
      v-model="showAnalysisDialog"
      :title="`${currentStudent?.student_name || ''} - AI分析结果`"
      width="70%"
    >
      <div v-if="analysisResult" class="analysis-content">
        <div v-html="formatAnalysis(analysisResult.analysis)"></div>
      </div>
      <div v-else class="loading-placeholder">
        <el-icon class="is-loading"><Loading /></el-icon>
        <p>分析中...</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import {
  DataAnalysis,
  Refresh,
  User,
  EditPen,
  Document,
  CircleCheck,
  Search,
  Loading
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { marked } from 'marked'

const loading = ref(false)
const chartContainer = ref(null)
const chartInstance = ref(null)
const chartType = ref('attempts')
const searchKeyword = ref('')
const stats = ref({
  students: [],
  total_students: 0
})
const showDetailDialog = ref(false)
const showAnalysisDialog = ref(false)
const currentStudent = ref(null)
const studentDetail = ref(null)
const analysisResult = ref(null)
const analyzingStudentId = ref(null)

// 计算属性
const totalAttempts = computed(() => {
  return stats.value.students.reduce((sum, s) => sum + s.total_attempts, 0)
})

const averageAttempts = computed(() => {
  if (stats.value.students.length === 0) return 0
  return Math.round(totalAttempts.value / stats.value.students.length)
})

const averagePassRate = computed(() => {
  if (stats.value.students.length === 0) return 0
  const totalRate = stats.value.students.reduce((sum, s) => sum + s.pass_rate, 0)
  return Math.round(totalRate / stats.value.students.length)
})

const filteredStudents = computed(() => {
  if (!searchKeyword.value) {
    return stats.value.students
  }
  const keyword = searchKeyword.value.toLowerCase()
  return stats.value.students.filter(
    s => s.student_name.toLowerCase().includes(keyword) ||
         s.username.toLowerCase().includes(keyword)
  )
})

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      ElMessage.error('请先登录')
      return
    }

    const res = await axios.get('http://127.0.0.1:8000/api/analytics/student-answer-stats', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (res.data && res.data.code === 200 && res.data.data) {
      stats.value = res.data.data
      await nextTick()
      updateChart()
      ElMessage.success('数据加载成功')
    } else {
      ElMessage.error(res.data?.message || '加载数据失败')
    }
  } catch (error) {
    console.error('加载数据失败:', error)
    const status = error?.response?.status
    if (status === 401) {
      ElMessage.error('未登录或登录已过期，请重新登录')
      localStorage.removeItem('token')
      window.location.href = '/login'
      return
    }
    ElMessage.error(error?.response?.data?.detail || error?.response?.data?.message || '加载数据失败')
  } finally {
    loading.value = false
  }
}

// 更新图表
const updateChart = () => {
  if (!chartContainer.value || !stats.value.students.length) return

  // 初始化或获取图表实例
  if (!chartInstance.value) {
    chartInstance.value = echarts.init(chartContainer.value)
  }

  // 准备数据
  const students = stats.value.students.slice(0, 20) // 只显示前20名学生
  const studentNames = students.map(s => s.student_name)
  
  let data = []
  let yAxisName = ''
  let seriesName = ''

  switch (chartType.value) {
    case 'attempts':
      data = students.map(s => s.total_attempts)
      yAxisName = '答题次数'
      seriesName = '答题次数'
      break
    case 'problems':
      data = students.map(s => s.total_problems)
      yAxisName = '题目数'
      seriesName = '答题题目数'
      break
    case 'passed':
      data = students.map(s => s.total_passed)
      yAxisName = '题目数'
      seriesName = '通过题目数'
      break
  }

  // 配置图表选项
  const option = {
    title: {
      text: `学生${seriesName}统计`,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function(params) {
        const param = params[0]
        const student = students[param.dataIndex]
        return `
          <div style="padding: 8px;">
            <div><strong>${param.name}</strong></div>
            <div>${seriesName}: ${param.value}</div>
            <div>总答题次数: ${student.total_attempts}</div>
            <div>答题题目数: ${student.total_problems}</div>
            <div>通过题目数: ${student.total_passed}</div>
            <div>通过率: ${student.pass_rate}%</div>
          </div>
        `
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: studentNames,
      axisLabel: {
        rotate: 45,
        interval: 0,
        fontSize: 12
      },
      axisTick: {
        alignWithLabel: true
      }
    },
    yAxis: {
      type: 'value',
      name: yAxisName,
      nameLocation: 'middle',
      nameGap: 50
    },
    series: [
      {
        name: seriesName,
        type: 'bar',
        data: data,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#2378f7' },
              { offset: 0.7, color: '#2378f7' },
              { offset: 1, color: '#83bff6' }
            ])
          }
        },
        animationDelay: function (idx) {
          return idx * 10
        }
      }
    ],
    animationEasing: 'elasticOut',
    animationDelayUpdate: function (idx) {
      return idx * 5
    }
  }

  chartInstance.value.setOption(option, true)

  // 响应式调整
  window.addEventListener('resize', () => {
    if (chartInstance.value) {
      chartInstance.value.resize()
    }
  })
}

// 获取通过率颜色
const getPassRateColor = (rate) => {
  if (rate >= 80) return '#67c23a'
  if (rate >= 60) return '#e6a23c'
  return '#f56c6c'
}

// 查看学生详情
const viewStudentDetail = async (student) => {
  currentStudent.value = student
  showDetailDialog.value = true
  studentDetail.value = null
  
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      ElMessage.error('请先登录')
      return
    }

    const res = await axios.get(
      `http://127.0.0.1:8000/api/analytics/student-answer-detail/${student.student_id}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    )

    if (res.data && res.data.code === 200 && res.data.data) {
      studentDetail.value = res.data.data
    } else {
      ElMessage.error(res.data?.message || '加载详情失败')
    }
  } catch (error) {
    console.error('加载学生详情失败:', error)
    ElMessage.error(error?.response?.data?.detail || '加载详情失败')
  }
}

// 关闭详情对话框
const closeDetailDialog = () => {
  showDetailDialog.value = false
  currentStudent.value = null
  studentDetail.value = null
}

// AI分析学生
const analyzeStudent = async (student) => {
  currentStudent.value = student
  showAnalysisDialog.value = true
  analysisResult.value = null
  analyzingStudentId.value = student.student_id
  
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      ElMessage.error('请先登录')
      return
    }

    const res = await axios.post(
      'http://127.0.0.1:8000/api/ai/analyze-student',
      {
        student_id: student.student_id
      },
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    )

    if (res.data && res.data.code === 200 && res.data.data) {
      analysisResult.value = res.data.data
      ElMessage.success('分析完成')
    } else {
      ElMessage.error(res.data?.message || '分析失败')
    }
  } catch (error) {
    console.error('AI分析失败:', error)
    ElMessage.error(error?.response?.data?.detail || '分析失败')
  } finally {
    analyzingStudentId.value = null
  }
}

// 格式化分析结果（Markdown转HTML）
const formatAnalysis = (text) => {
  if (!text) return ''
  try {
    return marked.parse(text)
  } catch (e) {
    return text.replace(/\n/g, '<br>')
  }
}

// 查看题目详情
const viewProblemDetail = (result) => {
  if (result.problem_path) {
    // 可以打开新窗口或对话框显示题目详情
    ElMessage.info(`查看题目: ${result.problem_title}`)
    // TODO: 可以调用题目API获取详细内容
  }
}

// 过滤学生
const filterStudents = () => {
  // 过滤逻辑已在 computed 中实现
}

// 组件挂载时加载数据
onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.analytics-page {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

  .page-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 24px;
    font-weight: bold;
    color: #303133;
    margin: 0;
  }

  .header-actions {
    display: flex;
    gap: 12px;
  }
}

.analytics-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 24px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  }

  .stat-icon {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    color: white;
    margin-right: 16px;

    &.students {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    &.attempts {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    &.problems {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }

    &.pass-rate {
      background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
  }

  .stat-content {
    flex: 1;

    .stat-label {
      font-size: 14px;
      color: #909399;
      margin-bottom: 8px;
    }

    .stat-value {
      font-size: 28px;
      font-weight: bold;
      color: #303133;
    }
  }
}

.charts-section {
  .chart-card {
    padding: 24px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;

      .chart-title {
        font-size: 18px;
        font-weight: bold;
        color: #303133;
        margin: 0;
      }

      .chart-controls {
        display: flex;
        gap: 12px;
      }
    }

    .chart-container {
      .chart {
        min-height: 400px;
      }
    }
  }
}

.table-section {
  .table-card {
    padding: 24px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    .table-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;

      .table-title {
        font-size: 18px;
        font-weight: bold;
        color: #303133;
        margin: 0;
      }
    }
  }
}

.education-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 学生详情对话框样式 */
.student-detail {
  .detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    .student-info {
      h3 {
        margin: 0 0 8px 0;
        font-size: 20px;
        color: #303133;
      }

      p {
        margin: 0;
        color: #909399;
        font-size: 14px;
      }
    }

    .detail-stats {
      display: flex;
      gap: 24px;
    }
  }

  .lesson-stats {
    margin-bottom: 24px;

    h4 {
      margin: 0 0 12px 0;
      font-size: 16px;
      color: #303133;
    }
  }

  .detail-results {
    h4 {
      margin: 0 0 12px 0;
      font-size: 16px;
      color: #303133;
    }
  }
}

.analysis-content {
  padding: 16px;
  line-height: 1.8;
  color: #303133;

  :deep(h2) {
    font-size: 18px;
    margin-top: 20px;
    margin-bottom: 12px;
    color: #303133;
  }

  :deep(h3) {
    font-size: 16px;
    margin-top: 16px;
    margin-bottom: 8px;
    color: #606266;
  }

  :deep(ul) {
    margin: 8px 0;
    padding-left: 24px;
  }

  :deep(li) {
    margin: 4px 0;
  }

  :deep(strong) {
    font-weight: 600;
    color: #303133;
  }
}

.loading-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #909399;

  .el-icon {
    font-size: 32px;
    margin-bottom: 12px;
  }
}
</style>
