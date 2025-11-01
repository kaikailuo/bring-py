<template>
  <div class="feedback-page">
    <!-- 头部导航 -->
    <header class="header">
      <div class="container">
        <div class="logo">
          <el-icon class="logo-icon"><School /></el-icon>
          <span class="logo-text">高中信息技术教学平台</span>
        </div>
        <nav class="nav">
          <router-link to="/home#features" class="nav-link">功能特色</router-link>
          <router-link to="/about-us" class="nav-link">关于我们</router-link>
          <router-link to="/contact" class="nav-link">联系我们</router-link>
          <router-link to="/feedback" class="nav-link active">问题反馈</router-link>
        </nav>
        <div class="auth-buttons">
          <el-button type="primary" @click="$router.push('/login')">
            <el-icon><User /></el-icon>
            登录
          </el-button>
        </div>
      </div>
    </header>

    <!-- 主要内容 -->
    <main class="main-content">
      <!-- 页面标题区域 -->
      <section class="page-header">
        <div class="container">
          <h1 class="page-title">问题反馈</h1>
          <p class="page-description">
            您的反馈对我们很重要，请告诉我们您遇到的问题或建议
          </p>
        </div>
      </section>

      <!-- 反馈表单 -->
      <section class="feedback-section">
        <div class="container">
          <div class="feedback-content">
            <div class="feedback-form-card education-card">
              <div class="form-header">
                <div class="form-icon">
                  <el-icon><Edit /></el-icon>
                </div>
                <h2 class="form-title">提交反馈</h2>
                <p class="form-description">
                  请填写以下信息，我们会认真处理您的反馈
                </p>
              </div>

              <el-form
                ref="feedbackFormRef"
                :model="feedbackForm"
                :rules="formRules"
                label-width="80px"
                class="feedback-form"
                @submit.prevent="submitFeedback"
              >
                <el-form-item label="姓名" prop="name">
                  <el-input
                    v-model="feedbackForm.name"
                    placeholder="请输入您的姓名"
                    clearable
                  />
                </el-form-item>

                <el-form-item label="邮箱" prop="email">
                  <el-input
                    v-model="feedbackForm.email"
                    placeholder="请输入您的邮箱"
                    clearable
                  />
                </el-form-item>

                <el-form-item label="反馈类型" prop="type">
                  <el-select
                    v-model="feedbackForm.type"
                    placeholder="请选择反馈类型"
                    style="width: 100%"
                  >
                    <el-option label="功能建议" value="suggestion" />
                    <el-option label="问题报告" value="bug" />
                    <el-option label="使用咨询" value="question" />
                    <el-option label="其他" value="other" />
                  </el-select>
                </el-form-item>

                <el-form-item label="反馈内容" prop="content">
                  <el-input
                    v-model="feedbackForm.content"
                    type="textarea"
                    :rows="6"
                    placeholder="请详细描述您的问题或建议..."
                    maxlength="1000"
                    show-word-limit
                  />
                </el-form-item>

                <el-form-item>
                  <div class="form-actions">
                    <el-button @click="resetForm">重置</el-button>
                    <el-button
                      type="primary"
                      :loading="isSubmitting"
                      @click="submitFeedback"
                    >
                      <el-icon><Send /></el-icon>
                      提交反馈
                    </el-button>
                  </div>
                </el-form-item>
              </el-form>
            </div>

            <div class="feedback-info-card education-card">
              <div class="info-header">
                <div class="info-icon">
                  <el-icon><InfoFilled /></el-icon>
                </div>
                <h3 class="info-title">反馈说明</h3>
              </div>
              
              <div class="info-content">
                <div class="info-item">
                  <el-icon><Clock /></el-icon>
                  <div class="info-text">
                    <h4>处理时间</h4>
                    <p>我们会在1-3个工作日内回复您的反馈</p>
                  </div>
                </div>
                
                <div class="info-item">
                  <el-icon><Message /></el-icon>
                  <div class="info-text">
                    <h4>联系方式</h4>
                    <p>重要问题我们会通过邮件与您联系</p>
                  </div>
                </div>
                
                <div class="info-item">
                  <el-icon><Star /></el-icon>
                  <div class="info-text">
                    <h4>感谢反馈</h4>
                    <p>您的建议帮助我们不断改进产品</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 返回首页按钮 -->
          <div class="back-to-home">
            <el-button type="primary" size="large" @click="$router.push('/')">
              <el-icon><HomeFilled /></el-icon>
              返回首页
            </el-button>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <div class="footer-logo">
              <el-icon><School /></el-icon>
              <span>高中信息技术教学平台</span>
            </div>
            <p class="footer-description">
              致力于为高中生提供优质的Python编程学习体验，
              通过技术创新推动信息技术教育发展。
            </p>
          </div>
          <div class="footer-section">
            <h4 class="footer-title">快速链接</h4>
            <ul class="footer-links">
              <li><router-link to="/home#features">功能特色</router-link></li>
              <li><router-link to="/about-us">关于我们</router-link></li>
              <li><router-link to="/contact">联系我们</router-link></li>
              <li><router-link to="/feedback">问题反馈</router-link></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4 class="footer-title">技术支持</h4>
            <ul class="footer-links">
              <li><a href="#">使用帮助</a></li>
              <li><a href="#">技术文档</a></li>
              <li><a href="#">API接口</a></li>
              <li><router-link to="/feedback">问题反馈</router-link></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2024 高中信息技术教学平台. 保留所有权利.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

// 表单数据
const feedbackForm = reactive({
  name: '',
  email: '',
  type: '',
  content: ''
})

// 表单引用
const feedbackFormRef = ref()

// 提交状态
const isSubmitting = ref(false)

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入您的姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择反馈类型', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入反馈内容', trigger: 'blur' },
    { min: 10, max: 1000, message: '反馈内容长度在 10 到 1000 个字符', trigger: 'blur' }
  ]
}

// 提交反馈
const submitFeedback = async () => {
  if (!feedbackFormRef.value) return
  
  try {
    const valid = await feedbackFormRef.value.validate()
    if (!valid) return
    
    isSubmitting.value = true
    
    // 模拟提交过程
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('反馈提交成功！我们会尽快处理您的反馈。')
    
    // 重置表单
    resetForm()
    
  } catch (error) {
    ElMessage.error('提交失败，请重试')
    console.error('提交反馈失败:', error)
  } finally {
    isSubmitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  if (feedbackFormRef.value) {
    feedbackFormRef.value.resetFields()
  }
}
</script>

<style lang="scss" scoped>
@use '../styles/variables.scss' as *;

.feedback-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 头部导航 */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid $border-color;
}

.header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 $spacing-lg;
  height: 64px;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: $font-size-lg;
  font-weight: bold;
  color: $education-blue;
}

.logo-icon {
  font-size: $font-size-xl;
}

.nav {
  display: flex;
  gap: $spacing-lg;
}

.nav-link {
  text-decoration: none;
  color: $text-primary;
  font-weight: 500;
  transition: color 0.3s ease;
  
  &:hover,
  &.active {
    color: $education-blue;
  }
}

.auth-buttons {
  display: flex;
  gap: $spacing-sm;
}

/* 页面标题区域 */
.page-header {
  padding-top: 64px;
  padding-bottom: $spacing-xxl;
  background: $gradient-primary;
  color: white;
  text-align: center;
}

.page-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: $spacing-md;
  color: white;
}

.page-description {
  font-size: $font-size-lg;
  color: rgba(255, 255, 255, 0.9);
  max-width: 600px;
  margin: 0 auto;
}

/* 反馈表单 */
.feedback-section {
  padding: $spacing-xxl 0;
  background: white;
}

.feedback-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: $spacing-xl;
  margin-bottom: $spacing-xxl;
}

.feedback-form-card {
  padding: $spacing-xl;
}

.form-header {
  text-align: center;
  margin-bottom: $spacing-xl;
}

.form-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto $spacing-md;
  font-size: 1.5rem;
  color: white;
  background: $gradient-primary;
}

.form-title {
  font-size: $font-size-xl;
  font-weight: bold;
  margin-bottom: $spacing-sm;
  color: $text-primary;
}

.form-description {
  color: $text-secondary;
  line-height: 1.6;
}

.feedback-form {
  .el-form-item {
    margin-bottom: $spacing-lg;
  }
  
  .el-input,
  .el-select,
  .el-textarea {
    width: 100%;
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: $spacing-md;
}

.feedback-info-card {
  padding: $spacing-xl;
}

.info-header {
  text-align: center;
  margin-bottom: $spacing-xl;
}

.info-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto $spacing-md;
  font-size: 1.5rem;
  color: white;
  background: $gradient-success;
}

.info-title {
  font-size: $font-size-xl;
  font-weight: bold;
  color: $text-primary;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: $spacing-md;
  
  .el-icon {
    color: $education-blue;
    font-size: $font-size-lg;
    margin-top: $spacing-xs;
  }
}

.info-text {
  h4 {
    font-size: $font-size-md;
    font-weight: bold;
    margin-bottom: $spacing-xs;
    color: $text-primary;
  }
  
  p {
    color: $text-secondary;
    line-height: 1.5;
    margin: 0;
  }
}

.back-to-home {
  text-align: center;
}

.back-to-home .el-button {
  height: 48px;
  padding: 0 $spacing-lg;
  font-size: $font-size-md;
}

/* 页脚 */
.footer {
  background: $bg-dark;
  color: white;
  padding: $spacing-xxl 0 $spacing-lg;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: $spacing-xl;
  margin-bottom: $spacing-xl;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: $font-size-lg;
  font-weight: bold;
  margin-bottom: $spacing-md;
}

.footer-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

.footer-title {
  font-size: $font-size-md;
  font-weight: bold;
  margin-bottom: $spacing-md;
}

.footer-links {
  list-style: none;
}

.footer-links li {
  margin-bottom: $spacing-sm;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: color 0.3s ease;
  
  &:hover {
    color: white;
  }
}

.footer-bottom {
  text-align: center;
  padding-top: $spacing-lg;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .header .container {
    padding: 0 $spacing-md;
  }
  
  .nav {
    display: none;
  }
  
  .feedback-content {
    grid-template-columns: 1fr;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .form-actions {
    flex-direction: column;
    
    .el-button {
      width: 100%;
    }
  }
}
</style>
