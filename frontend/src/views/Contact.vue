<template>
  <div class="contact-page">
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
          <router-link to="/contact" class="nav-link ">联系我们</router-link>
          <router-link to="/feedback" class="nav-link ">问题反馈</router-link>
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
          <h1 class="page-title">联系我们</h1>
          <p class="page-description">
            如果您有任何问题或建议，欢迎通过以下方式与我们联系
          </p>
        </div>
      </section>

      <!-- 联系信息 -->
      <section class="contact-section">
        <div class="container">
          <div class="contact-content">
            <div class="contact-card education-card">
              <div class="contact-icon">
                <el-icon><Message /></el-icon>
              </div>
              <h3 class="contact-title">邮箱联系</h3>
              <p class="contact-description">
                发送邮件至我们的官方邮箱，我们会在24小时内回复您的问题
              </p>
              <a href="mailto:team@example.com" class="contact-link">
                <el-icon><Message /></el-icon>
                team@example.com
              </a>
            </div>

            <div class="contact-card education-card">
              <div class="contact-icon github-icon">
                <el-icon><Link /></el-icon>
              </div>
              <h3 class="contact-title">GitHub 项目</h3>
              <p class="contact-description">
                访问我们的 GitHub 仓库，查看项目源码和最新更新
              </p>
              <a href="https://github.com/kaikailuo/bring-py" target="_blank" class="contact-link">
                <el-icon><Link /></el-icon>
                访问 GitHub
              </a>
            </div>

            <div class="contact-card education-card">
              <div class="contact-icon support-icon">
                <el-icon><Service /></el-icon>
              </div>
              <h3 class="contact-title">技术支持</h3>
              <p class="contact-description">
                遇到技术问题？我们的技术团队随时为您提供专业支持
              </p>
              <a href="mailto:support@example.com" class="contact-link">
                <el-icon><Service /></el-icon>
                support@example.com
              </a>
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
              <li><router-link to="/login">用户登录</router-link></li>
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
import { onMounted } from 'vue'

onMounted(() => {
  // 添加滚动动画效果
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in-up')
      }
    })
  })
  
  document.querySelectorAll('.contact-card').forEach(card => {
    observer.observe(card)
  })
})
</script>

<style lang="scss" scoped>
@use '../styles/variables.scss' as *;

.contact-page {
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

/* 联系信息 */
.contact-section {
  padding: $spacing-xxl 0;
  background: white;
}

.contact-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: $spacing-xl;
  margin-bottom: $spacing-xxl;
}

.contact-card {
  padding: $spacing-xl;
  text-align: center;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
  }
}

.contact-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto $spacing-lg;
  font-size: 2rem;
  color: white;
  background: $gradient-primary;
  
  &.github-icon {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  &.support-icon {
    background: $gradient-success;
  }
}

.contact-title {
  font-size: $font-size-xl;
  font-weight: bold;
  margin-bottom: $spacing-md;
  color: $text-primary;
}

.contact-description {
  color: $text-secondary;
  line-height: 1.6;
  margin-bottom: $spacing-lg;
}

.contact-link {
  display: inline-flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-md $spacing-lg;
  background: $education-blue;
  color: white;
  text-decoration: none;
  border-radius: $border-radius;
  font-weight: 500;
  transition: all 0.3s ease;
  
  &:hover {
    background: darken($education-blue, 10%);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
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
  
  .contact-content {
    grid-template-columns: 1fr;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
}
</style>
