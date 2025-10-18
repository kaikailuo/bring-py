<template>
  <div class="about-us-page">
    <!-- 头部导航 -->
    <header class="header">
      <div class="container">
        <div class="logo">
          <el-icon class="logo-icon"><School /></el-icon>
          <span class="logo-text">高中信息技术教学平台</span>
        </div>
        <nav class="nav">
          <router-link to="/home#features" class="nav-link">功能特色</router-link>
          <router-link to="/about-us" class="nav-link active">关于我们</router-link>
          <router-link to="/contact" class="nav-link">联系我们</router-link>
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
          <h1 class="page-title">关于我们</h1>
          <p class="page-description">
            了解我们的使命、愿景和团队，共同推动信息技术教育的发展
          </p>
        </div>
      </section>

      <!-- 项目介绍 -->
      <section class="about-section">
        <div class="container">
          <div class="about-content">
            <div class="about-card education-card">
              <div class="about-icon">
                <el-icon><InfoFilled /></el-icon>
              </div>
              <h2 class="about-title">项目简介</h2>
              <p class="about-description">
                本项目是一个学生-教师互动平台，包含作业管理、论坛交流等功能。
                我们致力于为高中生提供优质的Python编程学习体验，通过技术创新推动信息技术教育发展。
              </p>
              <div class="about-features">
                <div class="feature-item">
                  <el-icon><Check /></el-icon>
                  <span>智能作业管理系统</span>
                </div>
                <div class="feature-item">
                  <el-icon><Check /></el-icon>
                  <span>实时论坛交流平台</span>
                </div>
                <div class="feature-item">
                  <el-icon><Check /></el-icon>
                  <span>个性化学习路径</span>
                </div>
                <div class="feature-item">
                  <el-icon><Check /></el-icon>
                  <span>AI智能辅导系统</span>
                </div>
              </div>
            </div>

            <div class="about-card education-card">
              <div class="about-icon mission-icon">
                <el-icon><Aim /></el-icon>
              </div>
              <h2 class="about-title">我们的使命</h2>
              <p class="about-description">
                通过先进的教育技术和创新的教学方法，为每一位学生提供个性化的学习体验，
                让编程学习变得更加有趣和高效。
              </p>
              <div class="mission-stats">
                <div class="stat-item">
                  <div class="stat-number">1000+</div>
                  <div class="stat-label">活跃学生</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">50+</div>
                  <div class="stat-label">合作教师</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">95%</div>
                  <div class="stat-label">满意度</div>
                </div>
              </div>
            </div>

            <div class="about-card education-card">
              <div class="about-icon vision-icon">
                <el-icon><View /></el-icon>
              </div>
              <h2 class="about-title">发展愿景</h2>
              <p class="about-description">
                成为国内领先的高中信息技术教育平台，通过持续的技术创新和教育理念更新，
                为培养未来的技术人才贡献力量。
              </p>
              <div class="vision-goals">
                <div class="goal-item">
                  <el-icon><Star /></el-icon>
                  <span>提升编程教育质量</span>
                </div>
                <div class="goal-item">
                  <el-icon><Star /></el-icon>
                  <span>促进师生互动交流</span>
                </div>
                <div class="goal-item">
                  <el-icon><Star /></el-icon>
                  <span>推动教育技术创新</span>
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
              <li><router-link to="/login">用户登录</router-link></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4 class="footer-title">技术支持</h4>
            <ul class="footer-links">
              <li><a href="#">使用帮助</a></li>
              <li><a href="#">技术文档</a></li>
              <li><a href="#">API接口</a></li>
              <li><a href="#">问题反馈</a></li>
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
  
  document.querySelectorAll('.about-card').forEach(card => {
    observer.observe(card)
  })
})
</script>

<style lang="scss" scoped>
@use '../styles/variables.scss' as *;

.about-us-page {
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

/* 关于我们内容 */
.about-section {
  padding: $spacing-xxl 0;
  background: white;
}

.about-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: $spacing-xl;
  margin-bottom: $spacing-xxl;
}

.about-card {
  padding: $spacing-xl;
  text-align: center;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
  }
}

.about-icon {
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
  
  &.mission-icon {
    background: $gradient-success;
  }
  
  &.vision-icon {
    background: $gradient-warning;
  }
}

.about-title {
  font-size: $font-size-xl;
  font-weight: bold;
  margin-bottom: $spacing-md;
  color: $text-primary;
}

.about-description {
  color: $text-secondary;
  line-height: 1.6;
  margin-bottom: $spacing-lg;
  text-align: left;
}

.about-features {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
  text-align: left;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  color: $text-secondary;
  
  .el-icon {
    color: $success-color;
    font-size: $font-size-md;
  }
}

.mission-stats {
  display: flex;
  justify-content: space-around;
  margin-top: $spacing-lg;
  padding-top: $spacing-lg;
  border-top: 1px solid $border-color;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: $font-size-xxl;
  font-weight: bold;
  color: $education-blue;
  margin-bottom: $spacing-xs;
}

.stat-label {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.vision-goals {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
  text-align: left;
}

.goal-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  color: $text-secondary;
  
  .el-icon {
    color: $warning-color;
    font-size: $font-size-md;
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
  
  .about-content {
    grid-template-columns: 1fr;
  }
  
  .mission-stats {
    flex-direction: column;
    gap: $spacing-md;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
}
</style>
