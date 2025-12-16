<template>
  <div class="class-management">
    <div class="management-header">
      <h1 class="page-title">班级管理</h1>
      <div class="header-actions">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索班级或学生..."
          prefix-icon="Search"
          style="width: 300px"
          @input="handleSearch"
        />
        <el-button type="primary" @click="showCreateClassDialog = true">
          <el-icon><Plus /></el-icon>
          创建班级
        </el-button>
      </div>
    </div>

    <div class="management-content">
      <!-- 学生管理（整体列表） -->
      <div class="students-section">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><User /></el-icon>
            学生管理
          </h2>
          <div class="student-actions">
            <el-button @click="showAddStudentDialog = true">
              <el-icon><Plus /></el-icon>
              添加学生
            </el-button>
            <el-button @click="exportStudents">
              <el-icon><Download /></el-icon>
              导出名单
            </el-button>
          </div>
        </div>

        <div class="students-table">
          <el-table :data="students" style="width: 100%">
            <el-table-column prop="id" label="#" width="80" />
            <el-table-column prop="username" label="用户名" width="160" />
            <el-table-column prop="name" label="姓名" width="140" />
            <el-table-column prop="email" label="邮箱" />
            <el-table-column prop="is_active" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.is_active ? 'success' : 'warning'">
                  {{ scope.row.is_active ? '活跃' : '停用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="260">
              <template #default="scope">
                <el-button size="small" @click="viewStudentDetail(scope.row)">详情</el-button>
                <el-button size="small" type="primary" @click="editStudent(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="removeStudent(scope.row)">移除</el-button>
                <el-button size="small" type="warning" @click="toggleMute(scope.row)">{{ scope.row.is_muted ? '解禁' : '禁言' }}</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>

    <!-- 创建班级对话框 -->
    <el-dialog
      v-model="showCreateClassDialog"
      title="创建班级"
      width="600px"
      :before-close="handleCreateClassClose"
    >
      <el-form ref="createClassFormRef" :model="createClassForm" :rules="classRules" label-width="100px">
        <el-form-item label="班级名称" prop="name">
          <el-input v-model="createClassForm.name" placeholder="请输入班级名称" />
        </el-form-item>
        <el-form-item label="班级描述" prop="description">
          <el-input
            v-model="createClassForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入班级描述"
          />
        </el-form-item>
        <el-form-item label="课程类型" prop="courseType">
          <el-select v-model="createClassForm.courseType" placeholder="选择课程类型">
            <el-option label="Python基础" value="python-basic" />
            <el-option label="数据结构" value="data-structure" />
            <el-option label="算法入门" value="algorithm" />
            <el-option label="面向对象" value="oop" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期" prop="startDate">
          <el-date-picker
            v-model="createClassForm.startDate"
            type="date"
            placeholder="选择开始日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束日期" prop="endDate">
          <el-date-picker
            v-model="createClassForm.endDate"
            type="date"
            placeholder="选择结束日期"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showCreateClassDialog = false">取消</el-button>
          <el-button type="primary" @click="createClass">创建</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 添加学生对话框 -->
    <el-dialog
      v-model="showAddStudentDialog"
      title="添加学生"
      width="500px"
      :before-close="handleAddStudentClose"
    >
      <el-form ref="addStudentFormRef" :model="addStudentForm" :rules="studentRules" label-width="80px">
        <el-form-item label="学号" prop="studentId">
          <el-input v-model="addStudentForm.studentId" placeholder="请输入学号" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="addStudentForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="addStudentForm.email" placeholder="请输入邮箱" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showAddStudentDialog = false">取消</el-button>
          <el-button type="primary" @click="addStudent">添加</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, User, Download } from '@element-plus/icons-vue'

// 响应式数据
const searchKeyword = ref('')
const statusFilter = ref('all')
// removed class selection; show global students list
const selectedClass = ref(null)
const showCreateClassDialog = ref(false)
const showAddStudentDialog = ref(false)
const students = ref([])

const createClassFormRef = ref()
const addStudentFormRef = ref()

const createClassForm = ref({
  name: '',
  description: '',
  courseType: '',
  startDate: '',
  endDate: ''
})

const addStudentForm = ref({
  studentId: '',
  name: '',
  email: ''
})

const classRules = {
  name: [{ required: true, message: '请输入班级名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入班级描述', trigger: 'blur' }],
  courseType: [{ required: true, message: '请选择课程类型', trigger: 'change' }],
  startDate: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  endDate: [{ required: true, message: '请选择结束日期', trigger: 'change' }]
}

const studentRules = {
  studentId: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

// 模拟数据
const classes = ref([
  {
    id: 1,
    name: '高一(1)班',
    description: 'Python编程基础课程',
    code: 'PYTHON001',
    status: 'active',
    studentCount: 52,
    completionRate: 87,
    averageScore: 88.5,
    activeDays: 45,
    overallProgress: 78
  },
  {
    id: 2,
    name: '高一(2)班',
    description: '数据结构与算法',
    code: 'DS001',
    status: 'active',
    studentCount: 48,
    completionRate: 73,
    averageScore: 82.3,
    activeDays: 38,
    overallProgress: 65
  },
  {
    id: 3,
    name: '高二(1)班',
    description: 'Python进阶编程',
    code: 'PYTHON201',
    status: 'ended',
    studentCount: 56,
    completionRate: 92,
    averageScore: 91.2,
    activeDays: 60,
    overallProgress: 95
  }
])

// students list will be loaded from backend
// fallback sample (empty)
students.value = []

// 计算属性
const filteredClasses = computed(() => {
  let filtered = classes.value
  
  // 按状态筛选
  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(classItem => classItem.status === statusFilter.value)
  }
  
  // 按关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(classItem => 
      classItem.name.toLowerCase().includes(keyword) ||
      classItem.description.toLowerCase().includes(keyword) ||
      classItem.code.toLowerCase().includes(keyword)
    )
  }
  
  return filtered
})

// 方法
const handleSearch = () => {
  // 搜索逻辑已在计算属性中处理
}

const handleClassAction = (command, classItem) => {
  switch (command) {
    case 'view':
      selectedClass.value = classItem
      break
    case 'edit':
      editClass(classItem)
      break
    case 'students':
      // switch to global students view (removed per-requested change)
      selectedClass.value = null
      break
    case 'assignments':
      manageAssignments(classItem)
      break
    case 'analytics':
      viewAnalytics(classItem)
      break
    case 'archive':
      archiveClass(classItem)
      break
  }
}

const editClass = (classItem) => {
  console.log('编辑班级:', classItem.name)
  ElMessage.info('编辑班级功能开发中...')
}

const manageAssignments = (classItem) => {
  console.log('管理作业:', classItem.name)
  ElMessage.info('作业管理功能开发中...')
}

const viewAnalytics = (classItem) => {
  console.log('查看分析:', classItem.name)
  ElMessage.info('数据分析功能开发中...')
}

const archiveClass = async (classItem) => {
  try {
    await ElMessageBox.confirm('确定要归档这个班级吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    classItem.status = 'ended'
    ElMessage.success('班级已归档')
  } catch {
    // 用户取消
  }
}

const handleCreateClassClose = () => {
  showCreateClassDialog.value = false
  // 重置表单
  Object.assign(createClassForm.value, {
    name: '',
    description: '',
    courseType: '',
    startDate: '',
    endDate: ''
  })
  createClassFormRef.value?.resetFields()
}

const createClass = async () => {
  if (!createClassFormRef.value) return
  
  try {
    await createClassFormRef.value.validate()
    
    // 模拟创建班级
    const newClass = {
      id: Date.now(),
      ...createClassForm.value,
      code: `CLASS${Date.now().toString().slice(-6)}`,
      status: 'active',
      studentCount: 0,
      completionRate: 0,
      averageScore: 0,
      activeDays: 0,
      overallProgress: 0
    }
    
    classes.value.unshift(newClass)
    showCreateClassDialog.value = false
    handleCreateClassClose()
    
    ElMessage.success('班级创建成功！')
  } catch (error) {
    console.error('创建失败:', error)
    ElMessage.error('创建失败，请检查输入信息')
  }
}

const handleAddStudentClose = () => {
  showAddStudentDialog.value = false
  // 重置表单
  Object.assign(addStudentForm.value, {
    studentId: '',
    name: '',
    email: ''
  })
  addStudentFormRef.value?.resetFields()
}

const addStudent = async () => {
  if (!addStudentFormRef.value) return
  
  try {
    await addStudentFormRef.value.validate()
    // 调用后端注册接口创建学生账号（使用默认密码，建议生产环境让学生自行设置或通过重置流程）
    const payload = {
      username: addStudentForm.value.studentId || `stu${Date.now()}`,
      password: 'Password123!',
      role: 'student',
      name: addStudentForm.value.name,
      email: addStudentForm.value.email
    }

    const res = await axios.post('http://127.0.0.1:8000/api/auth/register', payload)
    if (res.data && res.data.code === 200) {
      ElMessage.success('学生添加成功，已同步数据库')
      showAddStudentDialog.value = false
      handleAddStudentClose()
      // 重新从后端加载学生列表
      await loadStudents()
    } else {
      ElMessage.error(res.data?.message || '添加学生失败')
    }
  } catch (error) {
    console.error('添加失败:', error)
    ElMessage.error(error?.response?.data?.message || error?.message || '添加失败，请检查输入信息')
  }
}

const router = useRouter()

const viewStudentDetail = (student) => {
  if (!student || !student.id) {
    ElMessage.error('学生信息不完整')
    return
  }
  // 跳转到教师侧的用户个人主页路由，路由已定义为 TeacherUserProfile
  router.push({ name: 'TeacherUserProfile', params: { userId: student.id } })
}

const editStudent = (student) => {
  console.log('编辑学生:', student.name)
  ElMessage.info('编辑学生功能开发中...')
}

const removeStudent = async (student) => {
  try {
    await ElMessageBox.confirm('确定要移除这个学生吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const index = classStudents.value.findIndex(s => s.id === student.id)
    if (index > -1) {
      classStudents.value.splice(index, 1)
      ElMessage.success('学生已移除')
    }
  } catch {
    // 用户取消
  }
}

const exportStudents = () => {
  console.log('导出学生名单')
  ElMessage.info('导出功能开发中...')
}

const toggleMute = async (student) => {
  try {
    // 调用后端禁言接口（教师/管理员权限）
    const token = localStorage.getItem('token')
    if (!token) {
      ElMessage.error('请先登录')
      return
    }
    const res = await axios.put(`http://127.0.0.1:8000/api/auth/users/${student.id}/mute?mute=${!student.is_muted}`, {}, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.data && res.data.code === 200) {
      ElMessage.success('操作成功')
      student.is_muted = !student.is_muted
    } else {
      ElMessage.error(res.data?.message || '操作失败')
    }
  } catch (err) {
    console.error('禁言失败', err)
    ElMessage.error('禁言操作失败')
  }
}

// 从后端加载学生列表
const loadStudents = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/auth/students', {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
    if (res.data && res.data.code === 200 && res.data.data) {
      students.value = res.data.data.students || []
    } else {
      students.value = []
    }
  } catch (err) {
    console.error('加载学生列表失败', err)
    students.value = []
  }
}

onMounted(() => {
  // 初始化数据
  loadStudents()
})
</script>

<style lang="scss" scoped>
.class-management {
  padding: $spacing-xl;
  height: 100%;
  overflow-y: auto;
}

.management-header {
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

.management-content {
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

.section-title {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: $font-size-xl;
  font-weight: bold;
  color: $text-primary;
  margin: 0;
}

.filter-options {
  display: flex;
  gap: $spacing-md;
}

.classes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
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
  margin: 0 0 $spacing-sm 0;
  line-height: 1.5;
}

.class-meta {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.class-code {
  font-size: $font-size-xs;
  color: $text-light;
}

.class-actions {
  flex-shrink: 0;
}

.class-stats {
  margin-bottom: $spacing-lg;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-md;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.stat-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: $education-blue;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: $font-size-sm;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  line-height: 1;
}

.stat-label {
  font-size: $font-size-xs;
  color: $text-secondary;
}

.class-progress {
  margin-top: $spacing-lg;
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

/* 学生管理 */
.students-section {
  background: white;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  padding: $spacing-xl;
}

.student-actions {
  display: flex;
  gap: $spacing-sm;
}

.students-table {
  margin-top: $spacing-lg;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .class-management {
    padding: $spacing-lg;
  }
  
  .management-header {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .classes-grid {
    grid-template-columns: 1fr;
  }
  
  .class-header {
    flex-direction: column;
    text-align: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
  
  .student-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
