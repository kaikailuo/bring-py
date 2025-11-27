<template>
  <div class="assignment-manager">
    <div class="sidebar-header">
      <h3>作业管理</h3>
      <div style="display:flex; gap:8px; align-items:center">
        <el-select v-model="selectedCourse" placeholder="选择课程" size="small" style="min-width:220px" @change="fetchCourseProblems">
          <el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
        <el-button size="small" @click="openCreateCourse">添加课程</el-button>
        <el-button type="primary" @click="openCreateDialog">布置作业</el-button>
      </div>
    </div>

    <div class="problems-list">
      <el-card v-for="p in problems" :key="p.path" class="problem-card">
        <div class="problem-card-header">
          <div class="title">{{ p.title || p.path }}</div>
          <div class="actions">
            <el-button type="danger" size="small" @click="removeProblem(p)">删除</el-button>
          </div>
        </div>
        <div class="meta">路径：{{ p.path }}</div>
      </el-card>
    </div>

    <el-dialog title="布置新作业" v-model="createDialogVisible" width="60%">
      <div>
        <el-form :model="form">
          <el-form-item label="题目标题" :label-width="'100px'">
            <el-input v-model="form.title" />
          </el-form-item>
          <el-form-item label="题面 (README.md)" :label-width="'100px'">
            <el-input type="textarea" :rows="6" v-model="form.description" />
          </el-form-item>
          <el-form-item label="参考答案 (solution.md)" :label-width="'100px'">
            <el-input type="textarea" :rows="6" v-model="form.solution" />
          </el-form-item>
          <el-form-item label="测试用例" :label-width="'100px'">
            <div v-for="(t, idx) in form.tests" :key="idx" class="test-row">
              <div>测试 {{ idx + 1 }}</div>
              <el-input type="textarea" :rows="3" placeholder="输入" v-model="t.input" />
              <el-input type="textarea" :rows="3" placeholder="期望输出" v-model="t.output" />
              <el-button type="danger" @click="removeTest(idx)">移除</el-button>
            </div>
            <el-button type="primary" @click="addTest">添加测试用例</el-button>
            <div style="margin-top:12px">
              <div>其他资源（图片等）：</div>
              <input type="file" multiple @change="onFilesSelected" />
              <div v-if="form.resources && form.resources.length>0" style="margin-top:8px">
                <div v-for="(r, i) in form.resources" :key="i">{{ r.filename }} <el-button type="text" @click="removeResource(i)">移除</el-button></div>
              </div>
            </div>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createProblem">提交并创建</el-button>
      </template>
    </el-dialog>

    <!-- 添加课程对话框 -->
    <el-dialog title="添加课程" v-model="createCourseVisible" width="40%">
      <el-form :model="courseForm">
        <el-form-item label="课程 id" :label-width="'100px'">
          <el-input v-model="courseForm.id" placeholder="例如 lesson_05" />
        </el-form-item>
        <el-form-item label="课程名称" :label-width="'100px'">
          <el-input v-model="courseForm.name" placeholder="例如 课程五" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createCourseVisible = false">取消</el-button>
        <el-button type="primary" @click="createCourse">创建</el-button>
      </template>
    </el-dialog>

        <!-- 删除课程按钮（右下角） -->
    <div class="delete-course-btn">
      <el-button type="danger" size="small" v-if="selectedCourse" @click="confirmDeleteCourse">删除课程</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { problemsAPI } from '@/utils/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const courses = ref([])
const selectedCourse = ref('')
const problems = ref([])

const createDialogVisible = ref(false)
const form = ref({ title: '', description: '', solution: '', tests: [], resources: [] })

const createCourseVisible = ref(false)
const courseForm = ref({ id: '', name: '' })

const fetchCourses = async () => {
  try {
    const res = await problemsAPI.getCourses()
    courses.value = res.courses || []
    if (courses.value.length > 0 && !selectedCourse.value) {
      selectedCourse.value = courses.value[0].id
      await fetchCourseProblems(selectedCourse.value)
    }
  } catch (e) {
    console.error(e)
  }
}

const fetchCourseProblems = async (courseId) => {
  try {
    const res = await problemsAPI.getCourseProblems(courseId)
    problems.value = res.problems || []
  } catch (e) {
    console.error(e)
    problems.value = []
  }
}

const openCreateDialog = () => {
  if (!selectedCourse.value) {
    ElMessage.warning('请先选择课程')
    return
  }
  form.value = { title: '', description: '', solution: '', tests: [] }
  createDialogVisible.value = true
}

const addTest = () => {
  form.value.tests.push({ input: '', output: '' })
}
const removeTest = (i) => {
  form.value.tests.splice(i, 1)
}

const onFilesSelected = (e) => {
  const files = Array.from(e.target.files || [])
  const readerPromises = files.map(f => new Promise((resolve) => {
    const fr = new FileReader()
    fr.onload = () => {
      // result is base64 data URL like data:...;base64,XXXX
      const result = fr.result
      let b64 = ''
      if (typeof result === 'string') {
        const idx = result.indexOf(',')
        b64 = idx >= 0 ? result.slice(idx + 1) : result
      }
      resolve({ filename: f.name, content_b64: b64 })
    }
    fr.readAsDataURL(f)
  }))
  Promise.all(readerPromises).then(items => {
    form.value.resources = (form.value.resources || []).concat(items)
  })
}

const removeResource = (i) => {
  form.value.resources.splice(i, 1)
}

const createProblem = async () => {
  if (!form.value.title.trim()) {
    ElMessage.warning('请填写题目标题')
    return
  }
  try {
    const res = await problemsAPI.createProblem(selectedCourse.value, {
      title: form.value.title,
      description: form.value.description,
      solution: form.value.solution,
      tests: form.value.tests,
      resources: form.value.resources
    })
    ElMessage.success('创建成功')
    createDialogVisible.value = false
    await fetchCourseProblems(selectedCourse.value)
  } catch (err) {
    console.error(err)
    ElMessage.error(err.message || '创建失败')
  }
}

const openCreateCourse = () => {
  courseForm.value = { id: '', name: '' }
  createCourseVisible.value = true
}

const createCourse = async () => {
  if (!courseForm.value.id.trim() || !courseForm.value.name.trim()) {
    ElMessage.warning('请填写课程 id 和名称')
    return
  }
  try {
    await problemsAPI.createCourse({ id: courseForm.value.id, name: courseForm.value.name })
    ElMessage.success('课程已创建')
    createCourseVisible.value = false
    await fetchCourses()
  } catch (err) {
    console.error(err)
    ElMessage.error(err.message || '创建课程失败')
  }
}

const confirmDeleteCourse = async () => {
  if (!selectedCourse.value) return
  try {
    await ElMessageBox.confirm('确定删除此课程及其所有题目？该操作不可恢复', '删除课程', { type: 'warning' })
    await problemsAPI.deleteCourse(selectedCourse.value)
    ElMessage.success('已删除课程')
    // refresh course list
    await fetchCourses()
    problems.value = []
    selectedCourse.value = ''
  } catch (err) {
    // cancel or error
  }
}

const removeProblem = async (p) => {
  try {
    await ElMessageBox.confirm('确定删除此题？该操作不可恢复', '确认删除', { type: 'warning' })
    await problemsAPI.deleteProblem(selectedCourse.value, p.problem || p.path.split('/').pop())
    ElMessage.success('已删除')
    await fetchCourseProblems(selectedCourse.value)
  } catch (err) {
    // 用户取消或出错
  }
}

onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
.assignment-manager {
  
  padding: 16px;
}
.sidebar-header {
  display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;
}
.delete-course-btn {
  display: flex;
  justify-content: flex-end;
  padding-right: 12px;
  margin-top: 16px;
}
.problems-list { display:flex; flex-direction:column; gap:12px; }
.problem-card { padding:12px; }
.problem-card-header { display:flex; justify-content:space-between; align-items:center; }
.test-row { display:flex; gap:8px; align-items:flex-start; margin-bottom:8px; }
</style>
