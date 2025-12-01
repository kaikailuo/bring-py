<template>
  <div class="create-assignment-wizard">
    <div class="wizard-header">
      <el-button type="text" icon="" @click="onBack">返回</el-button>
      <div class="wizard-title">布置作业向导</div>
    </div>

    <div class="wizard-steps">
      <el-steps :active="activeStep" finish-status="success">
        <el-step title="上传资源"></el-step>
        <el-step title="题面与参考答案"></el-step>
        <el-step title="测试用例"></el-step>
        <el-step title="预览与确认"></el-step>
      </el-steps>
    </div>

    <div class="wizard-content">
      <div v-show="activeStep === 1" class="step-content">
        <h3>步骤 1：上传其他资源（图片等）</h3>
        <input type="file" multiple @change="onFilesSelected" />
        <div v-if="resources.length" class="resources-list">
          <div v-for="(r, i) in resources" :key="i" class="resource-item">
            <div>{{ r.filename }}</div>
            <div style="display:flex; gap:8px; margin-top:6px">
              <el-button size="small" @click="viewResource(r)">查看</el-button>
              <el-button size="small" type="danger" @click="removeResource(i)">移除</el-button>
            </div>
          </div>
        </div>
      </div>

      <div v-show="activeStep === 2" class="step-content">
        <h3>步骤 2：编辑题面与参考答案</h3>
        <div style="display:flex; gap:12px; margin-bottom:8px; align-items:center">
          <el-button :type="currentEdit === 'readme' ? 'primary' : 'default'" @click="currentEdit = 'readme'">编辑 README.md</el-button>
          <el-button :type="currentEdit === 'solution' ? 'primary' : 'default'" @click="currentEdit = 'solution'">编辑 solution.md</el-button>
          <el-switch v-model="showPreview" active-text="预览" inactive-text="编辑" />
        </div>

        <div v-if="!showPreview">
          <MonacoEditor v-model="currentContent" language="markdown" />
        </div>
        <div v-else class="markdown-preview" v-html="renderedCurrent"></div>
      </div>

      <div v-show="activeStep === 3" class="step-content">
        <h3>步骤 3：编写测试用例</h3>
        <div style="margin-bottom:8px; display:flex; align-items:center; gap:12px">
          <span>启用测评（has_test）</span>
          <el-switch v-model="hasTest" active-text="是" inactive-text="否" />
          <div style="margin-left:12px; color:#666">若关闭则不会为该题生成测评用例</div>
        </div>
        <div v-if="!hasTest" style="margin-bottom:12px;color:#666">当前题目不启用测评，跳过测试用例填写即可。</div>
        <div v-if="hasTest" class="tests-grid">
          <div v-for="(t, idx) in tests" :key="idx" class="test-unit">
            <div class="test-unit-header">测试 {{ idx + 1 }}</div>
            <div><label>输入：</label><textarea v-model="tests[idx].input" rows="3"></textarea></div>
            <div style="margin-top:6px"><label>期望输出：</label><textarea v-model="tests[idx].output" rows="3"></textarea></div>
            <div style="margin-top:6px">
              <el-tag v-if="lastCheck && lastCheck.raw && lastCheck.raw.testResults && lastCheck.raw.testResults[idx]" :type="lastCheck.raw.testResults[idx].passed ? 'success' : 'danger'">
                {{ lastCheck.raw.testResults[idx].passed ? '通过' : '失败' }}
              </el-tag>
            </div>
          </div>
        </div>

        <div style="margin-top:12px; display:flex; gap:8px; align-items:center">
          <el-button v-if="hasTest" type="primary" :loading="checkRunning" @click="runCheckTests">测评集检测（运行 solution.md）</el-button>
          <el-button v-if="hasTest" @click="resetTests">重置所有用例</el-button>
          <div style="margin-left:12px">测评状态：<strong v-if="lastCheck">{{ lastCheck.passed ? '全部通过' : '未全部通过' }}</strong><span v-else>未检测</span></div>
        </div>
      </div>

      <div v-show="activeStep === 4" class="step-content">
        <h3>步骤 4：预览与确认</h3>
        <div class="preview-block">
          <h4>资源</h4>
          <ul>
            <li v-for="(r,i) in resources" :key="i">{{ r.filename }}</li>
          </ul>

          <h4>题面 (README.md)</h4>
          <div class="markdown-preview" v-html="renderedPreview"></div>

          <h4>参考答案 (solution.md)</h4>
          <pre style="background:#f6f8fa;padding:12px;border-radius:6px">{{ solution }}</pre>

          <h4>测试用例（检测结果）</h4>
          <div v-if="lastCheck && lastCheck.raw">
            <div>通过：{{ lastCheck.raw.passed }}/{{ lastCheck.raw.total }}</div>
            <div class="test-list-preview">
              <div v-for="(r, i) in lastCheck.raw.testResults" :key="i" style="border-bottom:1px solid #eee;padding:8px 0">
                <div><strong>测试 {{ i+1 }}：</strong><el-tag :type="r.passed ? 'success' : 'danger'">{{ r.passed ? '通过' : '失败' }}</el-tag></div>
                <div><strong>输入：</strong><pre>{{ r.input }}</pre></div>
                <div><strong>期望：</strong><pre>{{ r.expected }}</pre></div>
                <div><strong>实际：</strong><pre>{{ r.actual }}</pre></div>
              </div>
            </div>
          </div>
          <div v-else>
            <p>尚未运行测评或测评未通过。</p>
          </div>

        </div>
      </div>
    </div>

    <div class="wizard-footer">
      <el-button @click="prevStep" :disabled="activeStep === 1">上一步</el-button>
      <el-button type="primary" @click="nextStep" v-if="activeStep < 4">下一步</el-button>
      <el-button type="success" @click="submitAndCreate" v-else>完成并创建</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MonacoEditor from '@/views/student/MonacoEditor.vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { renderMarkdown } from '@/utils/markdown'
import { problemsAPI } from '@/utils/api'

const route = useRoute()
const router = useRouter()

const activeStep = ref(1)
const resources = ref([])
const tests = ref([])
const hasTest = ref(true)
const lastCheck = ref(null)
const checkRunning = ref(false)
const currentEdit = ref('readme')
const readme = ref(route.query.title ? `# ${route.query.title}` : '')
const solution = ref('')
const showPreview = ref(false)

const sessionKey = 'create_assignment_draft'

onMounted(() => {
  // 读取草稿（若存在）
  try {
    const raw = sessionStorage.getItem(sessionKey)
    if (raw) {
      const d = JSON.parse(raw)
      resources.value = d.resources || []
      readme.value = d.readme || readme.value
      solution.value = d.solution || ''
      tests.value = d.tests || []
      hasTest.value = d.hasTest !== undefined ? !!d.hasTest : hasTest.value
    }
      // ensure tests array length is 20
      if (!tests.value || tests.value.length !== 20) {
        tests.value = Array.from({ length: 20 }).map(() => ({ input: '', output: '' }))
      }
  } catch (e) {
    console.warn('读取草稿失败', e)
  }
})

const renderedPreview = computed(() => {
  let md = readme.value || ''
  if (resources.value && resources.value.length) {
    resources.value.forEach(r => {
      const re = new RegExp(`(!\[[^\]]*\]\()${escapeRegExp(r.filename)}(\))`, 'g')
      md = md.replace(re, `$1${r.dataUrl}$2`)
    })
  }
  return renderMarkdown(md)
})

function saveDraft() {
  const d = { resources: resources.value, readme: readme.value, solution: solution.value, tests: tests.value, hasTest: hasTest.value }
  try { sessionStorage.setItem(sessionKey, JSON.stringify(d)) } catch (e) { console.warn(e) }
}

function resetTests() {
  tests.value = Array.from({ length: 20 }).map(() => ({ input: '', output: '' }))
  lastCheck.value = null
  saveDraft()
}

const currentContent = computed({
  get() {
    return currentEdit.value === 'readme' ? readme.value : solution.value
  },
  set(v) {
    if (currentEdit.value === 'readme') readme.value = v
    else solution.value = v
    saveDraft()
  }
})

const renderedCurrent = computed(() => {
  // 在预览时，将引用的文件名替换为 data URL（如果已上传）
  let md = currentEdit.value === 'readme' ? readme.value : solution.value
  if (resources.value && resources.value.length) {
    resources.value.forEach(r => {
      const re = new RegExp(`(!\[[^\]]*\]\()${escapeRegExp(r.filename)}(\))`, 'g')
      md = md.replace(re, `$1${r.dataUrl}$2`)
    })
  }
  return renderMarkdown(md)
})

function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function onFilesSelected(e) {
  const files = Array.from(e.target.files || [])
  const promises = files.map(f => new Promise((resolve) => {
    const fr = new FileReader()
    fr.onload = () => {
      const dataUrl = fr.result
      // extract base64 portion
      let b64 = ''
      if (typeof dataUrl === 'string') {
        const idx = dataUrl.indexOf('base64,')
        if (idx >= 0) b64 = dataUrl.slice(idx + 7)
      }
      resolve({ filename: f.name, content_b64: b64, dataUrl })
    }
    fr.readAsDataURL(f)
  }))
  Promise.all(promises).then(items => {
    resources.value = resources.value.concat(items)
    saveDraft()
  })
}

function viewResource(r) {
  openResourcePreview(r)
}

function removeResource(i) {
  resources.value.splice(i, 1)
  saveDraft()
}

function openResourcePreview(r) {
  if (!r || !r.dataUrl) return;

  const mime = r.dataUrl.split(";")[0].replace("data:", "");
  const win = window.open("", "_blank");

  // 基础样式
  win.document.write(`
    <html>
      <head>
        <title>${r.filename}</title>
        <style>
          body {
            margin: 0;
            padding: 0;
            background: #f2f2f2;
            font-family: sans-serif;
          }
          .container {
            padding: 20px;
            text-align: center;
          }
          img, video, audio, embed, iframe {
            max-width: 100%;
            max-height: 90vh;
          }
          pre {
            text-align: left;
            white-space: pre-wrap;
            background: #222;
            color: #eee;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
          }
          .download {
            margin-top: 20px;
            display: inline-block;
            padding: 10px 16px;
            background: #409eff;
            color: white;
            border-radius: 6px;
            text-decoration: none;
            font-size: 14px;
          }
        </style>
      </head>
      <body>
        <div class="container">
  `);

  // 🎨 不同类型文件分开渲染
  if (mime.startsWith("image/")) {
    win.document.write(`<img src="${r.dataUrl}" />`);
  }
  else if (mime === "application/pdf") {
    win.document.write(`
      <embed src="${r.dataUrl}" type="application/pdf" width="100%" height="90vh"/>
    `);
  }
  else if (mime.startsWith("text/") || mime === "application/json") {
    const text = atob(r.content_b64 || "");
    win.document.write(`<pre>${escapeHtml(text)}</pre>`);
  }
  else if (mime === "text/markdown" || r.filename.endsWith(".md")) {
    const text = atob(r.content_b64 || "");
    win.document.write(`
      <pre>${escapeHtml(text)}</pre>
    `);
  }
  else if (mime.startsWith("video/")) {
    win.document.write(`
      <video src="${r.dataUrl}" controls></video>
    `);
  }
  else if (mime.startsWith("audio/")) {
    win.document.write(`
      <audio src="${r.dataUrl}" controls></audio>
    `);
  }
  else {
    // 未知类型，提供下载
    win.document.write(`
      <p>无法直接预览此文件类型：${mime}</p>
      <a class="download" href="${r.dataUrl}" download="${r.filename}">点击下载</a>
    `);
  }

  win.document.write(`
        <br/>
        <a class="download" href="${r.dataUrl}" download="${r.filename}">下载 ${r.filename}</a>
        </div>
      </body>
    </html>
  `);

  win.document.close();
}

// HTML 转义，避免代码类文件污染页面
function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}


function prevStep() {
  if (activeStep.value > 1) activeStep.value -= 1
}

function nextStep() {
  if (activeStep.value === 1) {
    // ensure files processed
    saveDraft()
    activeStep.value = 2
    return
  }
  if (activeStep.value === 2) {
    saveDraft()
    activeStep.value = 3
    return
  }
  if (activeStep.value === 3) {
    // 在进入预览步骤之前，若启用了测评则要求测评通过；否则直接允许进入
    if (hasTest.value) {
      if (!lastCheck.value || lastCheck.value.passed !== true) {
        ElMessage.warning('请先运行“测评集检测”，并确保所有用例通过后再预览')
        return
      }
    }
    saveDraft()
    activeStep.value = 4
    return
  }
}

async function runCheckTests() {
  // 从 tests.value 中保证满 20 项并全部填写
  if (!solution.value || !solution.value.trim()) {
    ElMessage.warning('请先填写参考答案(solution.md)')
    return
  }
  // ensure 20 tests
  if (tests.value.length !== 20) {
    ElMessage.warning('请确保共有 20 个测试用例（可留空输入/输出需填写）')
    return
  }
  for (let i = 0; i < tests.value.length; i++) {
    const t = tests.value[i]
    if ((t.input === undefined) || (t.output === undefined) || t.input === null || t.output === null) {
      ElMessage.warning('请完整填写所有测试用例的输入与期望输出')
      return
    }
  }

  checkRunning.value = true
  lastCheck.value = null
  try {
    const res = await problemsAPI.checkTests(solution.value, tests.value)
    // 服务器返回 { total, passed, testResults }
    const passedAll = res.passed === res.total && res.total > 0
    lastCheck.value = { raw: res, passed: passedAll }
    if (passedAll) {
      ElMessage.success(`测评通过：${res.passed}/${res.total}`)
    } else {
      ElMessage.error(`测评未全部通过：${res.passed}/${res.total}`)
    }
  } catch (e) {
    console.error(e)
    ElMessage.error(e.message || '测评失败')
  } finally {
    checkRunning.value = false
  }
}

async function submitAndCreate() {
  // createProblem: courseId from route.query.course
  const courseId = route.query.course
  if (!courseId) {
    ElMessage.error('未指定所属课程')
    return
  }
  // 构造 payload
  const payload = {
    title: route.query.title || '未命名题目',
    description: readme.value,
    solution: solution.value,
    tests: hasTest.value ? tests.value : [],
    has_test: !!hasTest.value,
    resources: resources.value.map(r => ({ filename: r.filename, content_b64: r.content_b64 }))
  }

  try {
    const res = await problemsAPI.createProblem(courseId, payload)
    ElMessage.success('题目创建成功')
    sessionStorage.removeItem(sessionKey)
    router.push({ name: 'AssignmentManagement' })
  } catch (e) {
    console.error(e)
    ElMessage.error(e.message || '创建题目失败')
  }
}

async function onBack() {
  try {
    const ok = await ElMessageBox.confirm('是否放弃此次作业编辑？未保存的内容将丢失', '确认返回', { type: 'warning' })
    if (ok !== 'cancel') {
      sessionStorage.removeItem(sessionKey)
      router.push({ name: 'AssignmentManagement' })
    }
  } catch (e) {
    // cancel
  }
}

function finish() {
  ElMessage.info('完成提交的逻辑尚未实现（占位）')
}
</script>

<style scoped>
.create-assignment-wizard { padding: 20px }
.wizard-header { display:flex; align-items:center; gap:12px }
.wizard-title { font-size:18px; font-weight:600 }
.wizard-steps { margin:16px 0 }
.step-content { padding:12px; background:#fff; border-radius:6px; min-height:260px }
.resources-list { margin-top:12px }
.resource-item { display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #eee }
.markdown-preview { padding:12px; border:1px solid #eee; border-radius:6px; background:#fff; min-height:300px }
.wizard-footer { margin-top:12px; display:flex; justify-content:flex-end; gap:8px }
</style>
