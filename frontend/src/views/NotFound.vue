<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <div class="error-illustration">
        <div class="error-number">404</div>
        <div class="error-icon">
          <el-icon><QuestionFilled /></el-icon>
        </div>
      </div>
      
      <div class="error-message">
        <h1 class="error-title">页面未找到</h1>
        <p class="error-description">
          抱歉，您访问的页面不存在或已被移动。
          <br>
          请检查URL是否正确，或返回首页继续浏览。
        </p>
        
        <div class="error-actions">
          <el-button type="primary" size="large" @click="goHome">
            <el-icon><House /></el-icon>
            返回首页
          </el-button>
          <el-button size="large" @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            返回上页
          </el-button>
        </div>
      </div>
    </div>
    
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
      <div class="floating-shape shape-4"></div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/home')
}

const goBack = () => {
  router.go(-1)
}
</script>

<style lang="scss" scoped>
.not-found-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.not-found-content {
  text-align: center;
  color: white;
  z-index: 10;
  position: relative;
}

.error-illustration {
  position: relative;
  margin-bottom: $spacing-xxl;
}

.error-number {
  font-size: 8rem;
  font-weight: bold;
  opacity: 0.1;
  position: absolute;
  top: -2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
}

.error-icon {
  font-size: 6rem;
  position: relative;
  z-index: 2;
}

.error-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 0 0 $spacing-lg 0;
}

.error-description {
  font-size: $font-size-lg;
  line-height: 1.6;
  margin: 0 0 $spacing-xxl 0;
  opacity: 0.9;
}

.error-actions {
  display: flex;
  gap: $spacing-md;
  justify-content: center;
}

.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.floating-shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 8s ease-in-out infinite;
}

.shape-1 {
  width: 100px;
  height: 100px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 80px;
  height: 80px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

.shape-4 {
  width: 120px;
  height: 120px;
  top: 10%;
  right: 30%;
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(180deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .error-number {
    font-size: 6rem;
  }
  
  .error-icon {
    font-size: 4rem;
  }
  
  .error-title {
    font-size: 2rem;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>
