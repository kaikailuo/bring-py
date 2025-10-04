<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card education-card">
        <div class="login-header">
          <div class="logo">
            <el-icon class="logo-icon"><School /></el-icon>
            <span class="logo-text">高中信息技术教学平台</span>
          </div>
          <h2 class="login-title">欢迎登录</h2>
          <p class="login-subtitle">选择您的身份开始学习之旅</p>
        </div>

        <div class="login-form">
          <el-tabs v-model="activeTab" class="role-tabs">
            <el-tab-pane label="学生登录" name="student">
              <el-form
                ref="studentFormRef"
                :model="studentForm"
                :rules="studentRules"
                size="large"
                @submit.prevent="handleStudentLogin"
              >
                <el-form-item prop="username">
                  <el-input
                    v-model="studentForm.username"
                    placeholder="请输入学号"
                    prefix-icon="User"
                  />
                </el-form-item>
                <el-form-item prop="password">
                  <el-input
                    v-model="studentForm.password"
                    type="password"
                    placeholder="请输入密码"
                    prefix-icon="Lock"
                    show-password
                  />
                </el-form-item>
                <el-form-item>
                  <div class="form-options">
                    <el-checkbox v-model="rememberMe">记住我</el-checkbox>
                    <el-link type="primary">忘记密码？</el-link>
                  </div>
                </el-form-item>
                <el-form-item>
                  <el-button
                    type="primary"
                    size="large"
                    :loading="loading"
                    @click="handleStudentLogin"
                    class="login-button"
                  >
                    <el-icon><User /></el-icon>
                    学生登录
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>

            <el-tab-pane label="教师登录" name="teacher">
              <el-form
                ref="teacherFormRef"
                :model="teacherForm"
                :rules="teacherRules"
                size="large"
                @submit.prevent="handleTeacherLogin"
              >
                <el-form-item prop="username">
                  <el-input
                    v-model="teacherForm.username"
                    placeholder="请输入工号"
                    prefix-icon="User"
                  />
                </el-form-item>
                <el-form-item prop="password">
                  <el-input
                    v-model="teacherForm.password"
                    type="password"
                    placeholder="请输入密码"
                    prefix-icon="Lock"
                    show-password
                  />
                </el-form-item>
                <el-form-item>
                  <div class="form-options">
                    <el-checkbox v-model="rememberMe">记住我</el-checkbox>
                    <el-link type="primary">忘记密码？</el-link>
                  </div>
                </el-form-item>
                <el-form-item>
                  <el-button
                    type="success"
                    size="large"
                    :loading="loading"
                    @click="handleTeacherLogin"
                    class="login-button"
                  >
                    <el-icon><UserFilled /></el-icon>
                    教师登录
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>

            <el-tab-pane label="管理员登录" name="admin">
              <el-form
                ref="adminFormRef"
                :model="adminForm"
                :rules="adminRules"
                size="large"
                @submit.prevent="handleAdminLogin"
              >
                <el-form-item prop="username">
                  <el-input
                    v-model="adminForm.username"
                    placeholder="请输入管理员账号"
                    prefix-icon="User"
                  />
                </el-form-item>
                <el-form-item prop="password">
                  <el-input
                    v-model="adminForm.password"
                    type="password"
                    placeholder="请输入密码"
                    prefix-icon="Lock"
                    show-password
                  />
                </el-form-item>
                <el-form-item>
                  <div class="form-options">
                    <el-checkbox v-model="rememberMe">记住我</el-checkbox>
                    <el-link type="primary">忘记密码？</el-link>
                  </div>
                </el-form-item>
                <el-form-item>
                  <el-button
                    type="warning"
                    size="large"
                    :loading="loading"
                    @click="handleAdminLogin"
                    class="login-button"
                  >
                    <el-icon><Setting /></el-icon>
                    管理员登录
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </div>

        <div class="login-footer">
          <p class="register-link">
            还没有账号？
            <el-link type="primary" @click="showRegisterDialog">立即注册</el-link>
          </p>
        </div>
      </div>

      <!-- 背景装饰 -->
      <div class="login-bg">
        <div class="floating-shapes">
          <div class="shape shape-1"></div>
          <div class="shape shape-2"></div>
          <div class="shape shape-3"></div>
          <div class="shape shape-4"></div>
        </div>
      </div>
    </div>

    <!-- 注册对话框 -->
    <el-dialog
      v-model="registerDialogVisible"
      title="用户注册"
      width="500px"
      :before-close="handleRegisterClose"
    >
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="80px"
      >
        <el-form-item label="用户类型" prop="role">
          <el-radio-group v-model="registerForm.role">
            <el-radio value="student">学生</el-radio>
            <el-radio value="teacher">教师</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请确认密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="registerForm.name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerForm.email" placeholder="请输入邮箱地址" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="registerDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleRegister">注册</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

// 响应式数据
const activeTab = ref('student')
const loading = ref(false)
const rememberMe = ref(false)
const registerDialogVisible = ref(false)

// 表单引用
const studentFormRef = ref()
const teacherFormRef = ref()
const adminFormRef = ref()
const registerFormRef = ref()

// 学生表单
const studentForm = reactive({
  username: '',
  password: ''
})

const studentRules = {
  username: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { min: 3, max: 20, message: '学号长度应为3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为6-20个字符', trigger: 'blur' }
  ]
}

// 教师表单
const teacherForm = reactive({
  username: '',
  password: ''
})

const teacherRules = {
  username: [
    { required: true, message: '请输入工号', trigger: 'blur' },
    { min: 3, max: 20, message: '工号长度应为3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为6-20个字符', trigger: 'blur' }
  ]
}

// 管理员表单
const adminForm = reactive({
  username: '',
  password: ''
})

const adminRules = {
  username: [
    { required: true, message: '请输入管理员账号', trigger: 'blur' },
    { min: 3, max: 20, message: '账号长度应为3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为6-20个字符', trigger: 'blur' }
  ]
}

// 注册表单
const registerForm = reactive({
  role: 'student',
  username: '',
  password: '',
  confirmPassword: '',
  name: '',
  email: ''
})

const registerRules = {
  role: [{ required: true, message: '请选择用户类型', trigger: 'change' }],
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为6-20个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 10, message: '姓名长度应为2-10个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

// 登录处理函数
const handleLogin = async (formRef, formData, role) => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    // 模拟登录请求
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟用户数据
    const userData = {
      id: Date.now(),
      username: formData.username,
      name: role === 'student' ? '张同学' : role === 'teacher' ? '李老师' : '管理员',
      role: role,
      avatar: '',
      email: `${formData.username}@example.com`
    }
    
    const token = `token_${Date.now()}_${role}`
    
    // 保存用户信息
    userStore.login(userData, token)
    
    ElMessage.success(`${role === 'student' ? '学生' : role === 'teacher' ? '教师' : '管理员'}登录成功！`)
    
    // 根据角色跳转
    if (role === 'student') {
      router.push('/student')
    } else if (role === 'teacher') {
      router.push('/teacher')
    } else if (role === 'admin') {
      router.push('/admin')
    }
    
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error('登录失败，请检查输入信息')
  } finally {
    loading.value = false
  }
}

const handleStudentLogin = () => {
  handleLogin(studentFormRef, studentForm, 'student')
}

const handleTeacherLogin = () => {
  handleLogin(teacherFormRef, teacherForm, 'teacher')
}

const handleAdminLogin = () => {
  handleLogin(adminFormRef, adminForm, 'admin')
}

// 注册相关函数
const showRegisterDialog = () => {
  registerDialogVisible.value = true
}

const handleRegisterClose = () => {
  registerDialogVisible.value = false
  // 重置表单
  Object.assign(registerForm, {
    role: 'student',
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
    email: ''
  })
  registerFormRef.value?.resetFields()
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    
    // 模拟注册请求
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('注册成功！请使用新账号登录')
    registerDialogVisible.value = false
    handleRegisterClose()
    
  } catch (error) {
    console.error('注册失败:', error)
    ElMessage.error('注册失败，请检查输入信息')
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.login-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 500px;
  padding: $spacing-lg;
}

.login-card {
  padding: $spacing-xxl;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: $spacing-xl;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: $spacing-sm;
  margin-bottom: $spacing-lg;
  font-size: $font-size-lg;
  font-weight: bold;
  color: $education-blue;
}

.logo-icon {
  font-size: $font-size-xl;
}

.login-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: $spacing-sm;
  color: $text-primary;
}

.login-subtitle {
  color: $text-secondary;
  font-size: $font-size-md;
}

.login-form {
  margin-bottom: $spacing-lg;
}

.role-tabs {
  margin-bottom: $spacing-lg;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: $font-size-md;
  font-weight: bold;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.login-footer {
  text-align: center;
  padding-top: $spacing-lg;
  border-top: 1px solid $border-color;
}

.register-link {
  color: $text-secondary;
  margin: 0;
}

/* 背景装饰 */
.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.floating-shapes {
  position: relative;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 80px;
  height: 80px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 120px;
  height: 120px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 60px;
  height: 60px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

.shape-4 {
  width: 100px;
  height: 100px;
  top: 10%;
  right: 30%;
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    padding: $spacing-md;
  }
  
  .login-card {
    padding: $spacing-xl;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
}
</style>
