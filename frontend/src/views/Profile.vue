<template>
  <div class="profile-container">
      <div class="profile-header">
      <h2 class="page-title">
        <el-icon><User /></el-icon>
        {{ isViewingOtherUser ? '用户主页' : '个人主页' }}
      </h2>
      <el-button v-if="isViewingOtherUser" @click="router.back()" plain>
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
    </div>

    <div class="profile-content">
      <!-- 基本信息卡片 -->
      <el-card class="profile-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">
              <el-icon><User /></el-icon>
              基本信息
            </span>
          </div>
        </template>

        <div class="basic-info">
          <!-- 头像区域 -->
          <div class="avatar-section">
            <el-avatar :src="profileForm.avatar" :size="120" class="user-avatar">
              <el-icon><UserFilled /></el-icon>
            </el-avatar>
            <el-button 
              type="primary" 
              size="small" 
              @click="handleAvatarClick"
              class="avatar-btn"
            >
              <el-icon><Camera /></el-icon>
              更换头像
            </el-button>
            <input
              ref="avatarInput"
              type="file"
              accept="image/*"
              style="display: none"
              @change="handleAvatarChange"
            />
          </div>

          <!-- 基本信息表单 -->
          <div class="info-form">
            <el-form
              ref="profileFormRef"
              :model="profileForm"
              :rules="profileRules"
              label-width="100px"
              label-position="left"
            >
              <el-form-item label="用户名">
                <el-input
                  v-model="userInfo.username"
                  disabled
                  class="disabled-input"
                />
              </el-form-item>

              <el-form-item label="昵称" prop="nickname">
                <el-input
                  v-model="profileForm.nickname"
                  placeholder="请输入昵称"
                  maxlength="20"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item label="真实姓名">
                <el-input
                  v-model="userInfo.name"
                  disabled
                  class="disabled-input"
                />
              </el-form-item>

              <el-form-item label="邮箱">
                <el-input
                  v-model="userInfo.email"
                  disabled
                  class="disabled-input"
                />
              </el-form-item>

              <el-form-item label="角色">
                <el-tag
                  :type="userInfo.role === 'teacher' ? 'success' : 'primary'"
                  size="large"
                >
                  {{ roleText }}
                </el-tag>
              </el-form-item>

              <el-form-item label="性别" prop="gender">
                <el-radio-group v-model="profileForm.gender">
                  <el-radio label="male">男</el-radio>
                  <el-radio label="female">女</el-radio>
                  <el-radio label="other">其他</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="手机号" prop="phone">
                <el-input
                  v-model="profileForm.phone"
                  placeholder="请输入手机号"
                  maxlength="11"
                />
              </el-form-item>

              <el-form-item label="个人简介" prop="bio">
                <el-input
                  v-model="profileForm.bio"
                  type="textarea"
                  :rows="4"
                  placeholder="介绍一下自己吧..."
                  maxlength="300"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item v-if="!isViewingOtherUser">
                <el-button
                  type="primary"
                  :loading="saving"
                  @click="handleSaveProfile"
                >
                  <el-icon><Check /></el-icon>
                  保存修改
                </el-button>
                <el-button @click="handleReset">
                  <el-icon><RefreshLeft /></el-icon>
                  重置
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </el-card>

      <!-- 修改密码卡片（仅自己可见） -->
      <el-card v-if="!isViewingOtherUser" class="profile-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">
              <el-icon><Lock /></el-icon>
              修改密码
            </span>
          </div>
        </template>

        <el-form
          ref="passwordFormRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-width="100px"
          label-position="left"
          class="password-form"
        >
          <el-form-item label="原密码" prop="oldPassword">
            <el-input
              v-model="passwordForm.oldPassword"
              type="password"
              placeholder="请输入原密码"
              show-password
            />
          </el-form-item>

          <el-form-item label="新密码" prop="newPassword">
            <el-input
              v-model="passwordForm.newPassword"
              type="password"
              placeholder="请输入新密码（6-20个字符）"
              show-password
            />
          </el-form-item>

          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="passwordForm.confirmPassword"
              type="password"
              placeholder="请再次输入新密码"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              :loading="changingPassword"
              @click="handleChangePassword"
            >
              <el-icon><Lock /></el-icon>
              修改密码
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 账户信息卡片 -->
      <el-card class="profile-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">
              <el-icon><InfoFilled /></el-icon>
              账户信息
            </span>
          </div>
        </template>

        <div class="account-info">
          <div class="info-item">
            <span class="info-label">注册时间：</span>
            <span class="info-value">{{ formatDate(userInfo.created_at) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">最后更新：</span>
            <span class="info-value">{{ formatDate(userInfo.updated_at) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">账户状态：</span>
            <el-tag :type="userInfo.is_active ? 'success' : 'danger'">
              {{ userInfo.is_active ? '已激活' : '已停用' }}
            </el-tag>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { authAPI } from '@/utils/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 判断是否查看其他用户
const userId = computed(() => {
  const routeUserId = route.params.userId
  return routeUserId ? parseInt(routeUserId) : null
})

const isViewingOtherUser = computed(() => {
  return userId.value !== null && userId.value !== userStore.user?.id
})

// 响应式数据
const loading = ref(false)
const saving = ref(false)
const changingPassword = ref(false)
const avatarInput = ref(null)
const profileFormRef = ref(null)
const passwordFormRef = ref(null)

// 用户基本信息（只读）
const userInfo = ref({
  id: null,
  username: '',
  name: '',
  email: '',
  role: '',
  created_at: null,
  updated_at: null,
  is_active: true
})

// 个人资料表单
const profileForm = reactive({
  avatar: '',
  nickname: '',
  gender: '',
  phone: '',
  bio: ''
})

// 原始个人资料（用于重置）
const originalProfile = ref({})

// 密码表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 表单验证规则
const profileRules = {
  nickname: [
    { max: 20, message: '昵称长度不能超过20个字符', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  bio: [
    { max: 300, message: '简介最多300字', trigger: 'blur' }
  ]
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为6-20个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 计算属性
const roleText = computed(() => {
  const roleMap = {
    student: '学生',
    teacher: '教师',
    admin: '管理员'
  }
  return roleMap[userInfo.value.role] || '未知'
})

// 方法
const loadProfile = async () => {
  try {
    loading.value = true
    const response = isViewingOtherUser.value 
      ? await authAPI.getUserProfile(userId.value)
      : await authAPI.getProfile()
    
    if (response.code === 200 && response.data && response.data.user) {
      const user = response.data.user
      
      // 更新用户基本信息
      userInfo.value = {
        id: user.id,
        username: user.username,
        name: user.name,
        email: user.email,
        role: user.role,
        created_at: user.created_at,
        updated_at: user.updated_at,
        is_active: user.is_active
      }
      
      // 更新个人资料表单
      profileForm.avatar = user.avatar || ''
      profileForm.nickname = user.nickname || ''
      profileForm.gender = user.gender || ''
      profileForm.phone = user.phone || ''
      profileForm.bio = user.bio || ''
      
      // 保存原始数据
      originalProfile.value = { ...profileForm }
      
      // 如果是查看自己的资料，更新 store 中的用户信息
      if (!isViewingOtherUser.value) {
        userStore.updateUser(user)
      }
    }
  } catch (error) {
    console.error('加载个人资料失败:', error)
    ElMessage.error(error.message || '加载个人资料失败')
  } finally {
    loading.value = false
  }
}

const handleSaveProfile = async () => {
  try {
    await profileFormRef.value.validate()
    
    saving.value = true
    
    const updateData = {
      avatar: profileForm.avatar || null,
      nickname: profileForm.nickname || null,
      gender: profileForm.gender || null,
      phone: profileForm.phone || null,
      bio: profileForm.bio || null
    }
    
    const response = await authAPI.updateProfile(updateData)
    
    if (response.code === 200) {
      ElMessage.success('个人资料更新成功')
      
      // 更新原始数据
      originalProfile.value = { ...profileForm }
      
      // 更新 store 中的用户信息
      if (response.data && response.data.user) {
        userStore.updateUser(response.data.user)
      }
    }
  } catch (error) {
    console.error('保存个人资料失败:', error)
    if (error.errors) {
      // 表单验证错误
      return
    }
    ElMessage.error(error.message || '保存个人资料失败')
  } finally {
    saving.value = false
  }
}

const handleReset = () => {
  Object.assign(profileForm, originalProfile.value)
  ElMessage.info('已重置为原始数据')
}

const handleAvatarClick = () => {
  avatarInput.value?.click()
}

const handleAvatarChange = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    ElMessage.error('请选择图片文件')
    return
  }
  
  // 验证文件大小（限制为 2MB）
  if (file.size > 2 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 2MB')
    return
  }
  
  // 读取文件并转换为 base64
  const reader = new FileReader()
  reader.onload = (e) => {
    profileForm.avatar = e.target.result
  }
  reader.readAsDataURL(file)
  
  // 清空 input 值，以便可以重复选择同一文件
  event.target.value = ''
}

const handleChangePassword = async () => {
  try {
    await passwordFormRef.value.validate()
    
    changingPassword.value = true
    
    const response = await authAPI.changePassword({
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword
    })
    
    if (response.code === 200) {
      ElMessage.success('密码修改成功，请重新登录')
      
      // 清空表单
      passwordForm.oldPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
      passwordFormRef.value.clearValidate()
      
      // 提示重新登录
      setTimeout(async () => {
        await ElMessageBox.confirm('密码已修改，需要重新登录', '提示', {
          confirmButtonText: '确定',
          showCancelButton: false,
          type: 'info'
        })
        userStore.logout()
        router.push('/login')
      }, 1000)
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    if (error.errors) {
      // 表单验证错误
      return
    }
    ElMessage.error(error.message || '修改密码失败')
  } finally {
    changingPassword.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 生命周期
onMounted(() => {
  loadProfile()
})
</script>

<style lang="scss" scoped>
.profile-container {
  min-height: 100%;
  padding: $spacing-lg;
  background: $bg-secondary;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
}

.page-title {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: $font-size-xl;
  font-weight: bold;
  color: $text-primary;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.profile-card {
  background: white;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: $font-size-md;
  font-weight: bold;
  color: $text-primary;
}

.basic-info {
  display: flex;
  gap: $spacing-xl;
  flex-wrap: wrap;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-md;
  min-width: 150px;
}

.user-avatar {
  border: 3px solid $border-color;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: $education-blue;
    transform: scale(1.05);
  }
}

.avatar-btn {
  width: 100%;
}

.info-form {
  flex: 1;
  min-width: 400px;
}

.disabled-input {
  :deep(.el-input__inner) {
    background-color: $bg-secondary;
    cursor: not-allowed;
  }
}

.password-form {
  max-width: 600px;
}

.account-info {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.info-item {
  display: flex;
  align-items: center;
  padding: $spacing-md;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.info-label {
  font-weight: 500;
  color: $text-secondary;
  min-width: 100px;
}

.info-value {
  color: $text-primary;
}

// 响应式设计
@media (max-width: 768px) {
  .basic-info {
    flex-direction: column;
  }
  
  .info-form {
    min-width: 100%;
  }
  
  .password-form {
    max-width: 100%;
  }
}
</style>

