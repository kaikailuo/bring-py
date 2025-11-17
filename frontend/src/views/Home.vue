<template>
  <div class="home-page">
    <!-- 头部导航 -->
    <header class="header">
      <div class="container">
        <div class="logo">
          <el-icon class="logo-icon"><School /></el-icon>
          <span class="logo-text">高中信息技术教学平台</span>
        </div>
        <nav class="nav">
          <a href="#features" class="nav-link">功能特色</a>
          <router-link to="/about-us" class="nav-link">关于我们</router-link>
          <router-link to="/contact" class="nav-link">联系我们</router-link>
          <router-link to="/feedback" class="nav-link">问题反馈</router-link>
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
      <!-- 英雄区域 -->
      <section class="hero">
        <div class="hero-bg">
          <div class="hero-content">
            <div class="hero-text">
              <h1 class="hero-title">
                <span class="text-gradient">Python编程学习</span>
                <br>让信息技术教育更智能
              </h1>
              <p class="hero-description">
                专为高中生设计的Python编程学习平台，集成AI智能辅导、个性化学习路径、
                实时学情分析等先进功能，让每一位学生都能享受优质的信息技术教育体验。
              </p>
              <div class="hero-buttons">
                <el-button type="primary" size="large" @click="$router.push('/login')">
                  <el-icon><Play /></el-icon>
                  开始学习
                </el-button>
                <el-button size="large" @click="scrollToFeatures">
                  <el-icon><InfoFilled /></el-icon>
                  了解更多
                </el-button>
              </div>
            </div>
            <div class="hero-image">
              <div class="code-preview">
                <div class="code-header">
                  <div class="code-dots">
                    <span class="dot red"></span>
                    <span class="dot yellow"></span>
                    <span class="dot green"></span>
                  </div>
                  <span class="code-title">python_demo.py</span>
                </div>
                <div class="code-content">
                  <pre><code># Python基础练习
def fibonacci(n):
    """计算斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 主程序
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")

# 输出结果
# F(0) = 0
# F(1) = 1
# F(2) = 1
# ...</code></pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 功能特色 -->
      <section id="features" class="features">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">核心功能模块</h2>
            <p class="section-description">
              四大核心模块，全面支持高中信息技术教学需求
            </p>
          </div>
          
          <div class="features-grid">
            <div class="feature-card education-card fade-in-up">
              <div class="feature-icon">
                <el-icon><FolderOpened /></el-icon>
              </div>
              <h3 class="feature-title">教学资源中心</h3>
              <p class="feature-description">
                丰富的Python学习资源，包括课件、视频、代码示例和交互式练习，
                支持智能推荐和分类管理。
              </p>
              <ul class="feature-list">
                <li>多格式资源支持</li>
                <li>智能内容推荐</li>
                <li>审核管理机制</li>
                <li>个性化学习路径</li>
              </ul>
            </div>

            <div class="feature-card education-card fade-in-up">
              <div class="feature-icon ai-icon">
                <el-icon><Magic /></el-icon>
              </div>
              <h3 class="feature-title">AI编程辅助系统</h3>
              <p class="feature-description">
                集成人工智能技术，提供智能问答、代码调试、知识点关联等
                个性化学习支持服务。
              </p>
              <ul class="feature-list">
                <li>自然语言编程问答</li>
                <li>实时错误检测修复</li>
                <li>知识点智能关联</li>
                <li>学习路径推荐</li>
              </ul>
            </div>

            <div class="feature-card education-card fade-in-up">
              <div class="feature-icon analytics-icon">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <h3 class="feature-title">学情分析仪表盘</h3>
              <p class="feature-description">
                全方位学习数据追踪分析，帮助教师了解学生学习情况，
                为学生提供个性化的学习建议。
              </p>
              <ul class="feature-list">
                <li>学习进度实时追踪</li>
                <li>知识点掌握度分析</li>
                <li>班级整体情况统计</li>
                <li>考试表现预测</li>
              </ul>
            </div>

            <div class="feature-card education-card fade-in-up">
              <div class="feature-icon community-icon">
                <el-icon><ChatDotRound /></el-icon>
              </div>
              <h3 class="feature-title">互动交流平台</h3>
              <p class="feature-description">
                构建学习社区，支持学生互助、教师答疑、代码分享和
                小组协作学习。
              </p>
              <ul class="feature-list">
                <li>问答论坛互动</li>
                <li>优秀作业展示</li>
                <li>小组协作项目</li>
                <li>实时在线答疑</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- 用户角色介绍 -->
      <section class="roles">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">多角色支持</h2>
            <p class="section-description">
              为不同用户群体提供专属功能体验
            </p>
          </div>
          
          <div class="roles-grid">
            <div class="role-card education-card">
              <div class="role-icon student-icon">
                <el-icon><User /></el-icon>
              </div>
              <h3 class="role-title">学生端</h3>
              <p class="role-description">
                个性化学习界面，集成代码编辑器、实时问答、学习进度追踪等功能，
                为学生提供沉浸式编程学习体验。
              </p>
              <div class="role-features">
                <span class="feature-tag">代码编辑器</span>
                <span class="feature-tag">实时问答</span>
                <span class="feature-tag">学习进度</span>
                <span class="feature-tag">资源库</span>
              </div>
            </div>

            <div class="role-card education-card">
              <div class="role-icon teacher-icon">
                <el-icon><UserFilled /></el-icon>
              </div>
              <h3 class="role-title">教师端</h3>
              <p class="role-description">
                强大的教学管理工具，支持班级管理、学情分析、资源审核、
                问题监控等教学全流程管理功能。
              </p>
              <div class="role-features">
                <span class="feature-tag">班级管理</span>
                <span class="feature-tag">学情分析</span>
                <span class="feature-tag">资源管理</span>
                <span class="feature-tag">问题监控</span>
              </div>
            </div>

            <div class="role-card education-card">
              <div class="role-icon admin-icon">
                <el-icon><Setting /></el-icon>
              </div>
              <h3 class="role-title">管理员</h3>
              <p class="role-description">
                系统级管理功能，支持用户管理、系统设置、数据分析等
                平台运营和管理功能。
              </p>
              <div class="role-features">
                <span class="feature-tag">用户管理</span>
                <span class="feature-tag">系统设置</span>
                <span class="feature-tag">数据分析</span>
                <span class="feature-tag">权限控制</span>
              </div>
            </div>
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
              <li><a href="#features">功能特色</a></li>
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

const scrollToFeatures = () => {
  document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
  // 添加滚动动画效果
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in-up')
      }
    })
  })
  
  document.querySelectorAll('.feature-card').forEach(card => {
    observer.observe(card)
  })
})
</script>

<style lang="scss" scoped>
.home-page {
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
  
  &:hover {
    color: $education-blue;
  }
}

.auth-buttons {
  display: flex;
  gap: $spacing-sm;
}

/* 英雄区域 */
.hero {
  padding-top: 64px;
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.hero-bg {
  background: $gradient-primary;
  width: 100%;
  padding: $spacing-xxl 0;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 $spacing-lg;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-xxl;
  align-items: center;
}

.hero-title {
  font-size: 3rem;
  font-weight: bold;
  line-height: 1.2;
  margin-bottom: $spacing-lg;
  color: white;
}

.hero-description {
  font-size: $font-size-lg;
  line-height: 1.6;
  margin-bottom: $spacing-xl;
  color: rgba(255, 255, 255, 0.9);
}

.hero-buttons {
  display: flex;
  gap: $spacing-md;
}

.hero-buttons .el-button {
  height: 48px;
  padding: 0 $spacing-lg;
  font-size: $font-size-md;
}

/* 代码预览 */
.code-preview {
  background: rgba(0, 0, 0, 0.8);
  border-radius: $border-radius;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.code-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: $spacing-sm $spacing-md;
  background: rgba(255, 255, 255, 0.1);
}

.code-dots {
  display: flex;
  gap: $spacing-xs;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  
  &.red { background: #ff5f56; }
  &.yellow { background: #ffbd2e; }
  &.green { background: #27ca3f; }
}

.code-title {
  color: rgba(255, 255, 255, 0.8);
  font-size: $font-size-sm;
}

.code-content {
  padding: $spacing-lg;
}

.code-content pre {
  color: #f8f8f2;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: $font-size-sm;
  line-height: 1.6;
  margin: 0;
}

/* 功能特色 */
.features {
  padding: $spacing-xxl 0;
  background: white;
}

.section-header {
  text-align: center;
  margin-bottom: $spacing-xxl;
}

.section-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: $spacing-md;
  color: $text-primary;
}

.section-description {
  font-size: $font-size-lg;
  color: $text-secondary;
  max-width: 600px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: $spacing-xl;
}

.feature-card {
  padding: $spacing-xl;
  text-align: center;
}

.feature-icon {
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
  
  &.ai-icon { background: $gradient-success; }
  &.analytics-icon { background: $gradient-warning; }
  &.community-icon { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
}

.feature-title {
  font-size: $font-size-xl;
  font-weight: bold;
  margin-bottom: $spacing-md;
  color: $text-primary;
}

.feature-description {
  color: $text-secondary;
  line-height: 1.6;
  margin-bottom: $spacing-lg;
}

.feature-list {
  list-style: none;
  text-align: left;
}

.feature-list li {
  padding: $spacing-xs 0;
  color: $text-secondary;
  position: relative;
  padding-left: $spacing-md;
  
  &::before {
    content: '✓';
    position: absolute;
    left: 0;
    color: $success-color;
    font-weight: bold;
  }
}

/* 用户角色 */
.roles {
  padding: $spacing-xxl 0;
  background: $bg-secondary;
}

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: $spacing-xl;
}

.role-card {
  padding: $spacing-xl;
  text-align: center;
}

.role-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto $spacing-lg;
  font-size: 2rem;
  color: white;
  
  &.student-icon { background: $education-blue; }
  &.teacher-icon { background: $education-green; }
  &.admin-icon { background: $education-purple; }
}

.role-title {
  font-size: $font-size-xl;
  font-weight: bold;
  margin-bottom: $spacing-md;
  color: $text-primary;
}

.role-description {
  color: $text-secondary;
  line-height: 1.6;
  margin-bottom: $spacing-lg;
}

.role-features {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-sm;
  justify-content: center;
}

.feature-tag {
  background: $education-blue;
  color: white;
  padding: $spacing-xs $spacing-sm;
  border-radius: 20px;
  font-size: $font-size-xs;
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
  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .header .container {
    padding: 0 $spacing-md;
  }
  
  .nav {
    display: none;
  }
  
  .features-grid,
  .roles-grid {
    grid-template-columns: 1fr;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
}
</style>
