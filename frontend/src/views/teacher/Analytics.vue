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
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  link
                  size="small"
                  @click="viewStudentDetail(row)"
                >
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>
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
  Search
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const loading = ref(false)
const chartContainer = ref(null)
const chartInstance = ref(null)
const chartType = ref('attempts')
const searchKeyword = ref('')
const stats = ref({
  students: [],
  total_students: 0
})

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
const viewStudentDetail = (student) => {
  ElMessage.info(`查看 ${student.student_name} 的详细答题情况`)
  // TODO: 可以打开一个对话框显示详细信息
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
</style>
