<template>
  <div class="practice-page">
    <div class="practice-header">
      <h1 class="page-title">编程练习</h1>
      <div class="header-actions">
        <el-select v-model="selectedDifficulty" placeholder="选择难度" style="width: 120px">
          <el-option label="全部" value="all" />
          <el-option label="简单" value="easy" />
          <el-option label="中等" value="medium" />
          <el-option label="困难" value="hard" />
        </el-select>
        <el-select v-model="selectedTopic" placeholder="选择主题" style="width: 150px">
          <el-option label="全部主题" value="all" />
          <el-option label="Python基础" value="python-basic" />
          <el-option label="数据结构" value="data-structure" />
          <el-option label="算法" value="algorithm" />
          <el-option label="面向对象" value="oop" />
        </el-select>
      </div>
    </div>

    <div class="practice-content">
      <!-- 代码编辑器区域 -->
      <div class="editor-section">
        <div class="editor-header">
          <h2 class="section-title">代码编辑器</h2>
          <div class="editor-actions">
            <el-button type="primary" @click="runCode" :loading="running">
              <el-icon><VideoPlay /></el-icon>
              运行代码
            </el-button>
            <el-button @click="resetCode">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
            <el-button @click="submitSolution" type="success" :disabled="!canSubmit">
              <el-icon><Check /></el-icon>
              提交答案
            </el-button>
          </div>
        </div>
        
        <div class="editor-container">
          <div class="code-editor">
            <div class="editor-toolbar">
              <div class="language-info">
                <el-icon><Document /></el-icon>
                <span>Python 3.9</span>
              </div>
              <div class="editor-options">
                <el-button size="small" @click="toggleTheme">
                  <el-icon><Moon /></el-icon>
                </el-button>
                <el-button size="small" @click="formatCode">
                  <el-icon><Magic /></el-icon>
                </el-button>
              </div>
            </div>
            <div class="editor-content">
              <textarea
                v-model="currentCode"
                class="code-textarea"
                placeholder="在这里编写你的Python代码..."
                @input="onCodeChange"
              ></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- 题目和输出区域 -->
      <div class="content-section">
        <el-tabs v-model="activeTab" class="content-tabs">
          <el-tab-pane label="题目描述" name="problem">
            <div class="problem-content">
              <div class="problem-header">
                <h3 class="problem-title">{{ currentProblem?.title || '选择一道题目开始练习' }}</h3>
                <div class="problem-meta">
                  <el-tag :type="getDifficultyType(currentProblem?.difficulty)">
                    {{ getDifficultyText(currentProblem?.difficulty) }}
                  </el-tag>
                  <el-tag type="info">{{ currentProblem?.topic || '' }}</el-tag>
                </div>
              </div>
              
              <div class="problem-description" v-if="currentProblem">
                <div class="description-section">
                  <h4>题目描述</h4>
                  <p>{{ currentProblem.description }}</p>
                </div>
                
                <div class="description-section">
                  <h4>输入格式</h4>
                  <pre><code>{{ currentProblem.inputFormat }}</code></pre>
                </div>
                
                <div class="description-section">
                  <h4>输出格式</h4>
                  <pre><code>{{ currentProblem.outputFormat }}</code></pre>
                </div>
                
                <div class="description-section">
                  <h4>示例</h4>
                  <div class="example">
                    <div class="example-input">
                      <h5>输入：</h5>
                      <pre><code>{{ currentProblem.exampleInput }}</code></pre>
                    </div>
                    <div class="example-output">
                      <h5>输出：</h5>
                      <pre><code>{{ currentProblem.exampleOutput }}</code></pre>
                    </div>
                  </div>
                </div>
                
                <div class="description-section">
                  <h4>提示</h4>
                  <p>{{ currentProblem.hint }}</p>
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
                <h4>测试结果</h4>
                <div class="test-item" v-for="(result, index) in testResults" :key="index">
                  <div class="test-header">
                    <span class="test-name">测试用例 {{ index + 1 }}</span>
                    <el-tag :type="result.passed ? 'success' : 'danger'">
                      {{ result.passed ? '通过' : '失败' }}
                    </el-tag>
                  </div>
                  <div class="test-details">
                    <div class="test-input">
                      <strong>输入：</strong>
                      <pre>{{ result.input }}</pre>
                    </div>
                    <div class="test-expected">
                      <strong>期望输出：</strong>
                      <pre>{{ result.expected }}</pre>
                    </div>
                    <div class="test-actual">
                      <strong>实际输出：</strong>
                      <pre>{{ result.actual }}</pre>
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
                    <div class="message-avatar">
                      <el-icon><Magic /></el-icon>
                    </div>
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
                  <el-input
                    v-model="aiMessage"
                    placeholder="输入你的编程问题..."
                    type="textarea"
                    :rows="3"
                    @keyup.ctrl.enter="sendAIMessage"
                  />
                  <el-button 
                    type="primary" 
                    @click="sendAIMessage"
                    :disabled="!aiMessage.trim()"
                  >
                    发送 (Ctrl+Enter)
                  </el-button>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>

    <!-- 题目列表侧边栏 -->
    <div class="problems-sidebar">
      <div class="sidebar-header">
        <h3>题目列表</h3>
        <el-button size="small" @click="refreshProblems">
          <el-icon><Refresh /></el-icon>
        </el-button>
      </div>
      
      <div class="problems-list">
        <div 
          class="problem-item"
          v-for="problem in filteredProblems"
          :key="problem.id"
          :class="{ active: currentProblem?.id === problem.id }"
          @click="selectProblem(problem)"
        >
          <div class="problem-info">
            <div class="problem-title">{{ problem.title }}</div>
            <div class="problem-meta">
              <el-tag size="small" :type="getDifficultyType(problem.difficulty)">
                {{ getDifficultyText(problem.difficulty) }}
              </el-tag>
              <el-tag size="small" type="info">{{ problem.topic }}</el-tag>
            </div>
          </div>
          <div class="problem-status">
            <el-icon v-if="problem.status === 'completed'" class="completed">
              <Check />
            </el-icon>
            <el-icon v-else-if="problem.status === 'attempted'" class="attempted">
              <Clock />
            </el-icon>
            <el-icon v-else class="not-started">
              <Circle />
            </el-icon>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// 响应式数据
const selectedDifficulty = ref('all')
const selectedTopic = ref('all')
const activeTab = ref('problem')
const currentCode = ref('')
const output = ref([])
const testResults = ref([])
const running = ref(false)
const currentProblem = ref(null)
const aiMessage = ref('')

// 模拟题目数据
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

// 计算属性
const filteredProblems = computed(() => {
  return problems.value.filter(problem => {
    const difficultyMatch = selectedDifficulty.value === 'all' || problem.difficulty === selectedDifficulty.value
    const topicMatch = selectedTopic.value === 'all' || problem.topic === selectedTopic.value
    return difficultyMatch && topicMatch
  })
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
  currentCode.value = `# ${problem.title}\n# 请在这里编写你的解决方案\n\ndef solution():\n    pass\n\n# 测试代码\nif __name__ == "__main__":\n    solution()`
  activeTab.value = 'problem'
}

const runCode = async () => {
  if (!currentCode.value.trim()) {
    return
  }
  
  running.value = true
  output.value = []
  testResults.value = []
  
  try {
    // 模拟代码执行
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟输出
    output.value = [
      '代码执行成功！',
      '输出结果：',
      '1 2 3 4 5',
      '',
      '执行时间: 0.001s',
      '内存使用: 12.5MB'
    ]
    
    // 模拟测试结果
    if (currentProblem.value) {
      testResults.value = [
        {
          passed: true,
          input: '4\n2 7 11 15\n9',
          expected: '0 1',
          actual: '0 1'
        },
        {
          passed: true,
          input: '3\n3 2 4\n6',
          expected: '1 2',
          actual: '1 2'
        },
        {
          passed: false,
          input: '2\n3 3\n6',
          expected: '0 1',
          actual: '无输出'
        }
      ]
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
  
  // 模拟提交
  await new Promise(resolve => setTimeout(resolve, 500))
  
  // 更新题目状态
  if (currentProblem.value) {
    const problem = problems.value.find(p => p.id === currentProblem.value.id)
    if (problem) {
      problem.status = 'completed'
    }
  }
  
  // 显示结果
  const passedTests = testResults.value.filter(t => t.passed).length
  const totalTests = testResults.value.length
  
  if (passedTests === totalTests) {
    console.log('恭喜！所有测试用例都通过了！')
  } else {
    console.log(`通过了 ${passedTests}/${totalTests} 个测试用例`)
  }
}

const clearOutput = () => {
  output.value = []
  testResults.value = []
}

const toggleTheme = () => {
  console.log('切换主题')
}

const formatCode = () => {
  console.log('格式化代码')
}

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
  console.log('刷新题目列表')
}

onMounted(() => {
  // 默认选择第一道题
  if (problems.value.length > 0) {
    selectProblem(problems.value[0])
  }
})
</script>

<style lang="scss" scoped>
.practice-page {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 300px;
  grid-template-rows: auto 1fr;
  gap: $spacing-lg;
  padding: $spacing-xl;
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
  grid-template-columns: 1fr 1fr;
  gap: $spacing-lg;
  overflow: hidden;
}

.editor-section {
  display: flex;
  flex-direction: column;
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
  overflow: hidden;
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
}

.content-tabs {
  flex: 1;
  background: white;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  overflow: hidden;
}

.problem-content {
  padding: $spacing-lg;
  height: 100%;
  overflow-y: auto;
}

.problem-header {
  margin-bottom: $spacing-lg;
  padding-bottom: $spacing-md;
  border-bottom: 1px solid $border-color;
}

.problem-title {
  font-size: $font-size-xl;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-md 0;
}

.problem-meta {
  display: flex;
  gap: $spacing-sm;
}

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
  background: $bg-dark;
  border-radius: $border-radius;
  padding: $spacing-md;
  margin-bottom: $spacing-lg;
  overflow-y: auto;
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
  color: #f8f8f2;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: $font-size-sm;
  line-height: 1.6;
}

.test-results {
  border-top: 1px solid $border-color;
  padding-top: $spacing-lg;
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
</style>
