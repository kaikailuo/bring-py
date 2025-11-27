<template>
  <div class="assignment-manager">
    <div class="sidebar-header">
      <h3>作业管理</h3>
      <div style="display:flex; gap:8px; align-items:center">
        <el-select v-model="selectedCourse" placeholder="选择课程" size="small" style="min-width:220px" @change="fetchCourseProblems">
          <el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
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
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createProblem">提交并创建</el-button>
      </template>
    </el-dialog>
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
const form = ref({ title: '', description: '', solution: '', tests: [] })

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
      tests: form.value.tests
    })
    ElMessage.success('创建成功')
    createDialogVisible.value = false
    await fetchCourseProblems(selectedCourse.value)
  } catch (err) {
    console.error(err)
    ElMessage.error(err.message || '创建失败')
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
.problems-list { display:flex; flex-direction:column; gap:12px; }
.problem-card { padding:12px; }
.problem-card-header { display:flex; justify-content:space-between; align-items:center; }
.test-row { display:flex; gap:8px; align-items:flex-start; margin-bottom:8px; }
</style>
