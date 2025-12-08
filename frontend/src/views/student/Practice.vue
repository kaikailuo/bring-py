<template>
  <div class="practice-page">

    <!-- 顶部标题栏 -->
    <div class="practice-header">
      <h1 class="page-title">
        <el-button
          v-if="mode === 'practice'"
          type="text"
          icon="ArrowLeft"
          @click="goBack"
          style="margin-right: 8px;"
        ></el-button>
        编程练习
      </h1>

      <!-- header-actions 已移除：不再显示难度与主题选择 -->
    </div>

    <!-- 题目选择界面 -->
    <div v-if="mode === 'select'" class="problems-sidebar full">
      <div class="sidebar-header">
        <h3>选择一个题目开始练习</h3>
        <div style="display:flex; gap:8px; align-items:center">
          <el-select v-model="selectedCourse" placeholder="选择课程" size="small" style="min-width:180px" @change="fetchCourseProblems">
            <el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
          <el-button size="small" @click="refreshProblems">
            <el-icon><Refresh /></el-icon>
          </el-button>
        </div>
      </div>
      <div class="problems-list">
        <div class="problem-item" v-for="problem in filteredProblems" :key="problem.id" @click="loadProblem(problem)">
          <div class="problem-info">
            <div class="problem-title">
              {{ problem.title }}
              <el-icon v-if="isProblemPassed(problem)" class="passed-icon" color="#67c23a">
                <Check />
              </el-icon>
            </div>
            <div class="problem-meta">
              <el-tag size="small" :type="getDifficultyType(problem.difficulty)">{{ getDifficultyText(problem.difficulty) }}</el-tag>
              <el-tag size="small" type="info">{{ problem.topic }}</el-tag>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 练习界面（题目和输出 + 编辑器） -->
    <div v-if="mode === 'practice'" class="practice-content">
      <!-- 左侧：题目描述 + 输出 + AI助手（复合面板） -->
      <div class="content-section">
        <el-tabs v-model="activeTab" class="content-tabs">
          <el-tab-pane label="题目描述" name="problem">
            <div class="problem-content">
              <div class="problem-description" v-if="currentProblem">
                <div class="description-section">
                  <!-- 使用 v-html 安全渲染后端返回的 Markdown -->
                  <div v-html="renderedDescription" class="markdown-body"></div>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="运行结果" name="output">
            <div class="output-content">
              <div class="output-header">
                <h3>运行结果</h3>
                <el-button size="small" @click="clearOutput">
                  <el-icon><Delete /></el-icon>
                  清空
                </el-button>
                <el-button size="small" type="primary" @click="goToAI" style="margin-left:8px;">
                  求助AI
                </el-button>
              </div>
              <div class="output-area">
                <div v-if="output.length === 0" class="empty-output">
                  <el-icon><Document /></el-icon>
                  <p>点击"运行代码"查看输出结果</p>
                </div>
                <div v-else class="output-text">
                  <pre v-for="(line, index) in output" :key="index">{{ line }}</pre>
                </div>
              </div>

              <div v-if="testResults.length > 0" class="test-results">
                <div class="test-list">
                  <h4>测试结果</h4>
                  <div class="test-item" v-for="(result, index) in testResults" :key="index">
                    <div class="test-header">
                      <span class="test-name">测试用例 {{ index + 1 }}</span>
                      <el-tag :type="result.passed ? 'success' : 'danger'">{{ result.passed ? '通过' : '失败' }}</el-tag>
                    </div>
                    <div class="test-details">
                      <div class="test-input"><strong>输入：</strong><pre>{{ result.input }}</pre></div>
                      <div class="test-expected"><strong>期望输出：</strong><pre>{{ result.expected }}</pre></div>
                      <div class="test-actual"><strong>实际输出：</strong><pre>{{ result.actual }}</pre></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="AI助手" name="ai">
            <div class="ai-assistant-content">
              <div class="ai-chat">
                <div class="chat-messages">
                  <div class="message ai-message">
                    <div class="message-avatar"><el-icon><StarFilled /></el-icon></div>
                    <div class="message-content">
                      <div class="message-text">
                        你好！我是你的AI编程助手。我可以帮你：
                        <ul>
                          <li>解答编程问题</li>
                          <li>调试代码错误</li>
                          <li>提供解题思路</li>
                          <li>优化代码性能</li>
                        </ul>
                        有什么问题可以随时问我！
                      </div>
                    </div>
                  </div>
                </div>

                <div class="chat-input">
                  <el-input v-model="aiMessage" placeholder="输入你的编程问题..." type="textarea" :rows="3" @keyup.ctrl.enter="sendAIMessage" />
                  <el-button type="primary" @click="sendAIMessage" :disabled="!aiMessage.trim()">发送 (Ctrl+Enter)</el-button>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>

      <!-- 右侧：代码编辑器 -->
      <div class="editor-section">
        <div class="editor-header">
          <h2 class="section-title">代码编辑器</h2>
          <div class="editor-actions">
            <el-button type="primary" @click="runCode" :loading="running"><el-icon><VideoPlay /></el-icon> 运行代码</el-button>
            <el-button @click="resetCode"><el-icon><Refresh /></el-icon> 重置</el-button>
            <el-button @click="submitSolution" type="success" :disabled="!canSubmit"><el-icon><Check /></el-icon> 提交答案</el-button>
          </div>
        </div>

        <div class="editor-container">
          <div class="code-editor">
            <div class="editor-toolbar">
              <div class="language-info"><el-icon><Document /></el-icon><span>Python</span></div>
              <!-- 编辑器选项已移除：不再显示主题切换与格式化按钮 -->
            </div>

            <div class="editor-content">
              <MonacoEditor v-model="currentCode" language="python" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import MonacoEditor from '../components/MonacoEditor.vue'
import { problemsAPI, API_BASE_URL as _API_BASE_URL } from '../../utils/api.js'
import { renderMarkdown } from '../../utils/markdown.js'

const mode = ref('select') // 'select' 表示题目选择界面，'practice' 表示练习界面

// 后端数据
const courses = ref([])
const selectedCourse = ref('')
const courseProblems = ref([])
const problemStatus = ref({}) // 存储题目通过状态 { "lesson/problem": { passed: bool, attempts: int } }

const enterPractice = (problem) => {
  // 兼容旧入口：若需要快速进入练习，可直接选中已有 problem 对象
  loadProblem(problem)
}

const goBack = () => {
  mode.value = 'select'
  currentProblem.value = null
  currentCode.value = ''
  output.value = []
  testResults.value = []
}

// 响应式数据
const activeTab = ref('problem')
const currentCode = ref('')
const output = ref([])
const testResults = ref([])
const running = ref(false)
const currentProblem = ref(null)
const aiMessage = ref('')
// 将后端返回的 Markdown 渲染为安全 HTML
const renderedDescription = computed(() => {
  const md = currentProblem.value?.description || ''
  if (!md) return ''
  // 当前题目的 path 形如 lesson_xx/problem_yy
  const path = currentProblem.value?.path || ''
  if (!path) return renderMarkdown(md)
  const parts = path.split('/')
  const lesson = parts[0]
  const problem = parts[1]
  // 后端暴露的静态资源路由： `${API_BASE_URL}/problems/${lesson}/${problem}/assets/...`
  const assetBase = `${_API_BASE_URL}/problems/${lesson}/${problem}/assets`
  return renderMarkdown(md, { assetBase })
})

// 模拟题目数据（作为回退或示例）
const problems = ref([
  {
    id: 1,
    title: '两数之和',
    description: '给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出和为目标值的那两个整数，并返回它们的数组下标。',
    difficulty: 'easy',
    topic: 'Python基础',
    inputFormat: '第一行输入数组长度n\n第二行输入n个整数\n第三行输入目标值target',
    outputFormat: '输出两个数的下标，用空格分隔',
    exampleInput: '4\n2 7 11 15\n9',
    exampleOutput: '0 1',
    hint: '可以使用字典来存储已遍历的数字及其下标',
    status: 'completed'
  },
  {
    id: 2,
    title: '反转链表',
    description: '给你单链表的头节点 head，请你反转链表，并返回反转后的链表。',
    difficulty: 'medium',
    topic: '数据结构',
    inputFormat: '第一行输入链表长度n\n第二行输入n个整数',
    outputFormat: '输出反转后的链表',
    exampleInput: '5\n1 2 3 4 5',
    exampleOutput: '5 4 3 2 1',
    hint: '使用三个指针：prev, curr, next',
    status: 'attempted'
  },
  {
    id: 3,
    title: '最长公共子序列',
    description: '给定两个字符串 text1 和 text2，返回这两个字符串的最长公共子序列的长度。',
    difficulty: 'hard',
    topic: '算法',
    inputFormat: '第一行输入字符串text1\n第二行输入字符串text2',
    outputFormat: '输出最长公共子序列的长度',
    exampleInput: 'abcde\nace',
    exampleOutput: '3',
    hint: '使用动态规划，dp[i][j]表示text1前i个字符和text2前j个字符的最长公共子序列长度',
    status: 'not-started'
  }
])

// 计算属性：优先使用后端获取的 courseProblems，否则使用本地模拟 problems
const filteredProblems = computed(() => {
  // 不再支持按难度/主题过滤，直接显示后端或本地的题目列表
  return courseProblems.value.length > 0 ? courseProblems.value : problems.value
})

const canSubmit = computed(() => {
  return currentCode.value.trim().length > 0 && currentProblem.value
})

// 方法
const getDifficultyType = (difficulty) => {
  const types = {
    easy: 'success',
    medium: 'warning',
    hard: 'danger'
  }
  return types[difficulty] || 'info'
}

const getDifficultyText = (difficulty) => {
  const texts = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return texts[difficulty] || '未知'
}

const selectProblem = (problem) => {
  currentProblem.value = problem
  // 根据题目设置初始代码模板
  currentCode.value = `# ${problem.title || problem.problem}\n# 请在这里编写你的解决方案\n\ndef solution():\n    pass\n\n# 测试代码\nif __name__ == "__main__":\n    solution()`
  activeTab.value = 'problem'
}

// 加载题目详情（从后端获取 markdown）
const loadProblem = async (item) => {
  try {
    // item 可能包含 path 字段：lesson_xx/problem_yy
    const path = item.path || `${selectedCourse.value}/${item.problem}`
    const parts = path.split('/')
    const lesson = parts[0]
    const problemName = parts[1]
    let md = ''
    try {
      md = await problemsAPI.getProblemMarkdown(lesson, problemName)
    } catch (e) {
      md = ''
      console.error('获取题面失败，使用空内容作为描述', e)
    }

    const problemObj = {
      id: item.id || `${lesson}-${problemName}`,
      title: item.title || problemName,
      description: md || item.description || '',
      difficulty: item.difficulty || 'easy',
      topic: item.topic || '',
      inputFormat: item.inputFormat || '',
      outputFormat: item.outputFormat || '',
      exampleInput: item.exampleInput || '',
      exampleOutput: item.exampleOutput || '',
      hint: item.hint || '',
      path: path
    }

    selectProblem(problemObj)
    mode.value = 'practice'
  } catch (err) {
    console.error('loadProblem error', err)
  }
}

const runCode = async () => {
  if (!currentCode.value.trim()) {
    return
  }
  
  running.value = true
  output.value = []
  testResults.value = []
  
  try {
    // 如果 currentProblem 有 path，优先调用后端 run 接口
    if (currentProblem.value && currentProblem.value.path) {
      const parts = currentProblem.value.path.split('/')
      const lesson = parts[0]
      const problemName = parts[1]
      const res = await problemsAPI.run(lesson, problemName, currentCode.value)
      // 优化前端展示：如果后端返回 testResults，则展示为测试点列表，不显示原始 JSON
      if (res && Array.isArray(res.testResults) && res.testResults.length > 0) {
        testResults.value = res.testResults
        // 如果后端还返回 output 字段且非空，可展示为单行信息；否则保持输出区空
        output.value = res.result ? (typeof res.result === 'string' ? res.result.split('\n') : [String(res.result)]) : []
      } else {
        output.value = res.result ? (typeof res.result === 'string' ? res.result.split('\n') : [JSON.stringify(res)]) : []
        testResults.value = res.testResults || []
      }
    } else {
      // 本地模拟执行（回退）
      await new Promise(resolve => setTimeout(resolve, 1000))
      output.value = [
        '代码执行成功（本地模拟）！',
        '输出结果：',
        '1 2 3 4 5'
      ]
      if (currentProblem.value) {
        testResults.value = [
          { passed: true, input: '示例输入', expected: '示例输出', actual: '示例输出' }
        ]
      }
    }
    activeTab.value = 'output'
  } catch (error) {
    output.value = ['代码执行出错：', error.message]
  } finally {
    running.value = false
  }
}

const resetCode = () => {
  if (currentProblem.value) {
    selectProblem(currentProblem.value)
  } else {
    currentCode.value = ''
  }
}

const submitSolution = async () => {
  if (!canSubmit.value) return
  
  try {
    if (currentProblem.value && currentProblem.value.path) {
      const parts = currentProblem.value.path.split('/')
      const lesson = parts[0]
      const problemName = parts[1]
      const res = await problemsAPI.submit(lesson, problemName, currentCode.value)
      // 处理返回的测评结果（mock 格式也可兼容）
      console.log('提交结果：', res)
      // 如果后端返回 testResults，则展示所有测试点；否则使用兼容的 result 文本
      if (res && Array.isArray(res.testResults) && res.testResults.length > 0) {
        testResults.value = res.testResults
        output.value = res.result ? [res.result] : []
      } else {
        output.value = res.result ? [res.result] : []
        testResults.value = res.testResults || []
      }
      activeTab.value = 'output'
      
      // 提交后刷新题目通过状态
      if (selectedCourse.value) {
        await fetchProblemStatus(selectedCourse.value)
      }
    } else {
      // 本地模拟提交
      await new Promise(resolve => setTimeout(resolve, 500))
      output.value = ['本地模拟：提交已接收']
    }
  } catch (err) {
    console.error('提交失败', err)
    output.value = ['提交失败：', err.message]
  }
}

const clearOutput = () => {
  output.value = []
  testResults.value = []
}

const goToAI = () => {
  activeTab.value = 'ai'
}

// 删除不再需要的演示功能：toggleTheme 和 formatCode

const onCodeChange = () => {
  // 代码变化时的处理
}

const sendAIMessage = () => {
  if (!aiMessage.value.trim()) return
  
  // 模拟AI回复
  console.log('发送AI消息:', aiMessage.value)
  aiMessage.value = ''
}

const refreshProblems = () => {
  fetchCourses()
}

// 获取课程列表并自动加载第一个课程的题目
const fetchCourses = async () => {
    try {
    const res = await problemsAPI.getCourses()
    courses.value = res.courses || []
    if (courses.value.length > 0) {
      // courses 为 [{id,name}]，默认选择第一个的 id
      selectedCourse.value = courses.value[0].id
      await fetchCourseProblems(selectedCourse.value)
    }
  } catch (err) {
    console.error('fetchCourses error', err)
  }
}

const fetchCourseProblems = async (courseId) => {
  try {
    const res = await problemsAPI.getCourseProblems(courseId)
    // res.problems 可能为 [{ problem, title, path }, ...]
    courseProblems.value = (res.problems || []).map((p, idx) => ({
      id: p.problem || idx,
      title: p.title || p.problem || `题目 ${idx + 1}`,
      description: '',
      difficulty: 'easy',
      topic: '',
      path: p.path || `${courseId}/${p.problem}`
    }))
    
    // 获取题目通过状态
    await fetchProblemStatus(courseId)
  } catch (err) {
    console.error('fetchCourseProblems error', err)
    courseProblems.value = []
  }
}

// 获取题目通过状态
const fetchProblemStatus = async (courseId) => {
  try {
    const res = await problemsAPI.getCourseProblemStatus(courseId)
    if (res && res.status) {
      problemStatus.value = res.status || {}
    }
  } catch (err) {
    console.error('fetchProblemStatus error', err)
    problemStatus.value = {}
  }
}

// 检查题目是否通过
const isProblemPassed = (problem) => {
  if (!problem || !problem.path) return false
  const status = problemStatus.value[problem.path]
  return status && status.passed === true
}

onMounted(() => {
  // 优先从后端加载课程和题目
  fetchCourses().then(() => {
    if (courseProblems.value.length > 0) {
      // 默认选择第一题（不进入练习界面，只填充右侧）
      selectProblem(courseProblems.value[0])
    } else if (problems.value.length > 0) {
      selectProblem(problems.value[0])
    }
  })
})
</script>

<style lang="scss" scoped>
.practice-page {
  /* 使用视口高度，避免父元素没有高度导致子元素无法伸展的问题 */
  height: 100%;
  display: grid;
  /* 使用单列布局，让内容区占满整个页面宽度；左右面板的相对宽度在 .practice-content 中控制 */
  grid-template-columns: 1fr;
  grid-template-rows: auto 1fr;
  gap: $spacing-lg;
  padding: $spacing-xl;
  /* 防止页面整体滚动，保证左右面板独立滚动 */
  overflow: hidden;
}

.practice-header {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.practice-content {
  display: grid;
  /* 左侧为题目/结果复合面板，右侧为代码编辑器（右侧更宽） */
  /* 修改下面两个数值可以调整左右面板的相对宽度（例如 0.5fr 1fr 或 0.7fr 1fr） */
  grid-template-columns: 0.9fr 1fr;
  gap: $spacing-lg;
  overflow: hidden;
  width: 100%; /* 确保占满父容器宽度 */
}

.practice-content {
  height: 100%;
}

/* 确保左右面板都能占满可用高度，从而内部的 .problem-content 能正确滚动 */
.practice-content,
.content-section,
.editor-section,
.content-tabs {
  height: 100%;
}

/* Element Plus tabs 内部结构的调整，确保选项卡内容区可伸展并允许内部滚动 */
.content-tabs .el-tabs__content {
  display: flex;
  flex: 1 1 auto;
  overflow: hidden; /* 外层隐藏，具体滚动由内部 .problem-content 控制 */
}

.content-tabs .el-tab-pane {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.editor-section {
  display: flex;
  flex-direction: column;
  overflow: auto; /* 右侧单独滚动 */
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-md;
}

.section-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0;
}

.editor-actions {
  display: flex;
  gap: $spacing-sm;
}

.editor-container {
  flex: 1;
  background: white;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  overflow: auto;
}

.code-editor {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-sm $spacing-md;
  background: $bg-secondary;
  border-bottom: 1px solid $border-color;
}

.language-info {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  font-size: $font-size-sm;
  color: $text-secondary;
}

.editor-options {
  display: flex;
  gap: $spacing-xs;
}

.editor-content {
  flex: 1;
  padding: $spacing-md;
}

.code-textarea {
  width: 100%;
  height: 100%;
  border: none;
  outline: none;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: $font-size-sm;
  line-height: 1.6;
  resize: none;
  background: transparent;
  color: $text-primary;
}

.content-section {
  display: flex;
  flex-direction: column;
  /* 让左侧面板在网格行中伸展 */
  flex: 1 1 auto;
  overflow: auto; /* 左侧单独滚动 */
}

.content-tabs {
  flex: 1;
  background: white;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  overflow: hidden;
  /* 使选项卡占满父容器高度，内部面板可滚动 */
  display: flex;
  flex-direction: column;
}

.problem-content {
  padding: $spacing-lg;
  height: 100%;
  overflow-y: auto;
  /* 确保在 flex 布局下可以正确缩放并滚动 */
  flex: 1 1 auto;
}

/* header removed: title and meta are no longer displayed */

.description-section {
  margin-bottom: $spacing-lg;
}

.description-section h4 {
  font-size: $font-size-md;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-sm 0;
}

.description-section p {
  color: $text-secondary;
  line-height: 1.6;
  margin: 0;
}

.description-section pre {
  background: $bg-secondary;
  padding: $spacing-md;
  border-radius: $border-radius;
  overflow-x: auto;
  margin: $spacing-sm 0;
}

.example {
  display: flex;
  gap: $spacing-lg;
}

.example-input,
.example-output {
  flex: 1;
}

.example h5 {
  font-size: $font-size-sm;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-sm 0;
}

.output-content {
  padding: $spacing-lg;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-md;
  padding-bottom: $spacing-sm;
  border-bottom: 1px solid $border-color;
}

.output-header h3 {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0;
}

.output-area {
  flex: 1;
  height: 200px;
  min-height: 240px;
  background: $bg-dark;
  border-radius: $border-radius;
  padding: $spacing-md;
  margin-bottom: $spacing-lg;
  overflow-y :hidden;
}

.empty-output {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: $text-light;
  
  .el-icon {
    font-size: 3rem;
    margin-bottom: $spacing-md;
  }
}

.output-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;   // 👍 垂直居中
  height: 100%;              // 👍 必须：让它填满 .output-area

  color: #f8f8f2;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: $font-size-sm;
  line-height: 1.6;

  pre {
    margin: 0;
    font-size: 40px;
    white-space: pre-wrap;
    text-align: center;       // 如果需要文字居中
  }
}


.test-results {
  border-top: 1px solid $border-color;
  padding-top: $spacing-lg;
  overflow-y : auto;
}

.test-results h4 {
  font-size: $font-size-md;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-md 0;
}

.test-item {
  margin-bottom: $spacing-lg;
  padding: $spacing-md;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.test-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-sm;
}

.test-name {
  font-weight: bold;
  color: $text-primary;
}

.test-details {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.test-details pre {
  background: white;
  padding: $spacing-sm;
  border-radius: $border-radius;
  font-size: $font-size-xs;
  margin: 0;
}

.ai-assistant-content {
  padding: $spacing-lg;
  height: 100%;
}

.ai-chat {
  height: 100%;
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
  line-height: 1.6;
}

.chat-input {
  display: flex;
  gap: $spacing-sm;
}

.problems-sidebar {
  background: white;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-lg;
  border-bottom: 1px solid $border-color;
}

.sidebar-header h3 {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0;
}

.problems-list {
  flex: 1;
  overflow-y: auto;
}

/* 测评结果与 AI 助手并排区域 */
.test-results {
  border-top: 1px solid $border-color;
  padding-top: $spacing-lg;
  display: flex;
  gap: $spacing-lg;
}

.test-results .test-list {
  flex: 1 1 auto;
  min-width: 0;
}

.ai-placeholder {
  padding: $spacing-sm;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.problem-item {
  display: flex;
  align-items: center;
  padding: $spacing-md;
  border-bottom: 1px solid $border-color;
  cursor: pointer;
  transition: background-color 0.3s ease;
  
  &:hover {
    background: $bg-hover;
  }
  
  &.active {
    background: rgba(24, 144, 255, 0.1);
    border-left: 3px solid $education-blue;
  }
  
  &:last-child {
    border-bottom: none;
  }
}

.problem-info {
  flex: 1;
}

.problem-info .problem-title {
  font-size: $font-size-sm;
  font-weight: 500;
  color: $text-primary;
  margin: 0 0 $spacing-xs 0;
  display: flex;
  align-items: center;
  gap: $spacing-xs;
}

.passed-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.problem-info .problem-meta {
  display: flex;
  gap: $spacing-xs;
}

.problem-status {
  margin-left: $spacing-sm;
}

.problem-status .completed {
  color: $success-color;
}

.problem-status .attempted {
  color: $warning-color;
}

.problem-status .not-started {
  color: $text-light;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .practice-page {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto;
  }
  
  .practice-content {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
  }
  
  .problems-sidebar {
    order: 3;
  }
}

@media (max-width: 768px) {
  .practice-page {
    padding: $spacing-lg;
  }
  
  .practice-header {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .example {
    flex-direction: column;
  }
}
.full {
  grid-column: 1 / -1;
  padding: 2rem;
}
</style>
