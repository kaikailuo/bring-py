<template>
  <div class="swipe-test">
    <div class="test-header">
      <h1>滑动功能测试页面</h1>
      <p>测试不同配置的滑动组件</p>
    </div>

    <div class="test-section">
      <h2>基础滑动测试</h2>
      <SwipeContainer
        :items="basicItems"
        :items-per-view="1"
        :autoplay="true"
        :autoplay-delay="3000"
        :show-indicators="true"
        :show-navigation="true"
        :loop="true"
        :indicator-type="'dots'"
        @slide-change="onSlideChange"
      >
        <template #default="{ item }">
          <div class="test-slide" :style="{ backgroundColor: item.color }">
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
          </div>
        </template>
      </SwipeContainer>
    </div>

    <div class="test-section">
      <h2>多项目显示测试</h2>
      <SwipeContainer
        :items="multiItems"
        :items-per-view="3"
        :autoplay="false"
        :show-indicators="true"
        :show-navigation="true"
        :loop="false"
        :indicator-type="'bars'"
        :indicator-color="'#52c41a'"
      >
        <template #default="{ item }">
          <div class="test-card">
            <div class="card-icon" :style="{ backgroundColor: item.color }">
              <el-icon><component :is="item.icon" /></el-icon>
            </div>
            <h4>{{ item.title }}</h4>
            <p>{{ item.description }}</p>
          </div>
        </template>
      </SwipeContainer>
    </div>

    <div class="test-section">
      <h2>进度指示器测试</h2>
      <SwipeContainer
        :items="progressItems"
        :items-per-view="1"
        :autoplay="true"
        :autoplay-delay="5000"
        :show-indicators="true"
        :show-navigation="false"
        :loop="true"
        :indicator-type="'bars'"
        :show-progress="true"
        :indicator-color="'#faad14'"
        :indicator-size="'large'"
      >
        <template #default="{ item }">
          <div class="progress-slide">
            <div class="slide-content">
              <el-icon class="slide-icon" :style="{ color: item.color }">
                <component :is="item.icon" />
              </el-icon>
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
            </div>
          </div>
        </template>
      </SwipeContainer>
    </div>

    <div class="test-section">
      <h2>数字指示器测试</h2>
      <SwipeContainer
        :items="numberItems"
        :items-per-view="1"
        :autoplay="false"
        :show-indicators="true"
        :show-navigation="true"
        :loop="false"
        :indicator-type="'numbers'"
        :indicator-color="'#722ed1'"
        :indicator-size="'large'"
      >
        <template #default="{ item }">
          <div class="number-slide">
            <div class="slide-number">{{ item.number }}</div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
          </div>
        </template>
      </SwipeContainer>
    </div>

    <div class="test-info">
      <h3>测试说明</h3>
      <ul>
        <li>支持触摸滑动和鼠标拖拽</li>
        <li>支持键盘左右箭头键控制</li>
        <li>支持自动播放和手动控制</li>
        <li>支持多种指示器样式</li>
        <li>支持进度条显示</li>
        <li>响应式设计，适配移动端</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SwipeContainer from '@/components/SwipeContainer.vue'

// 基础滑动测试数据
const basicItems = ref([
  {
    title: '第一张幻灯片',
    description: '这是第一张测试幻灯片，展示了基础的滑动功能。',
    color: '#667eea'
  },
  {
    title: '第二张幻灯片',
    description: '这是第二张测试幻灯片，展示了循环滑动效果。',
    color: '#764ba2'
  },
  {
    title: '第三张幻灯片',
    description: '这是第三张测试幻灯片，展示了自动播放功能。',
    color: '#f093fb'
  }
])

// 多项目显示测试数据
const multiItems = ref([
  {
    title: 'Python基础',
    description: '学习Python的基本语法',
    color: '#1890ff',
    icon: 'Document'
  },
  {
    title: '数据结构',
    description: '掌握常用数据结构',
    color: '#52c41a',
    icon: 'Box'
  },
  {
    title: '算法设计',
    description: '学习算法设计思想',
    color: '#faad14',
    icon: 'TrendCharts'
  },
  {
    title: 'Web开发',
    description: 'Python Web开发入门',
    color: '#f5222d',
    icon: 'Monitor'
  },
  {
    title: '数据分析',
    description: '使用Python分析数据',
    color: '#722ed1',
    icon: 'DataAnalysis'
  },
  {
    title: '机器学习',
    description: 'Python机器学习基础',
    color: '#13c2c2',
    icon: 'Magic'
  }
])

// 进度指示器测试数据
const progressItems = ref([
  {
    title: '学习阶段一',
    description: 'Python基础语法学习，包括变量、数据类型、控制流等基本概念。',
    color: '#1890ff',
    icon: 'Document'
  },
  {
    title: '学习阶段二',
    description: '面向对象编程，学习类、对象、继承、多态等高级概念。',
    color: '#52c41a',
    icon: 'Box'
  },
  {
    title: '学习阶段三',
    description: '数据结构与算法，掌握列表、字典、集合等数据结构的应用。',
    color: '#faad14',
    icon: 'TrendCharts'
  }
])

// 数字指示器测试数据
const numberItems = ref([
  {
    number: '01',
    title: '第一步：环境搭建',
    description: '安装Python解释器和开发环境，配置必要的工具和插件。'
  },
  {
    number: '02',
    title: '第二步：基础语法',
    description: '学习Python的基本语法规则，包括变量、函数、类等概念。'
  },
  {
    number: '03',
    title: '第三步：实践项目',
    description: '通过实际项目练习，巩固所学知识，提升编程能力。'
  },
  {
    number: '04',
    title: '第四步：进阶学习',
    description: '学习高级特性，包括装饰器、生成器、异步编程等。'
  }
])

const onSlideChange = (index) => {
  console.log('幻灯片切换到:', index)
}
</script>

<style lang="scss" scoped>
.swipe-test {
  padding: $spacing-xl;
  max-width: 1200px;
  margin: 0 auto;
}

.test-header {
  text-align: center;
  margin-bottom: $spacing-xxl;
}

.test-header h1 {
  font-size: 2.5rem;
  color: $text-primary;
  margin-bottom: $spacing-md;
}

.test-header p {
  font-size: $font-size-lg;
  color: $text-secondary;
}

.test-section {
  margin-bottom: $spacing-xxl;
}

.test-section h2 {
  font-size: $font-size-xl;
  color: $text-primary;
  margin-bottom: $spacing-lg;
  border-bottom: 2px solid $education-blue;
  padding-bottom: $spacing-sm;
}

.test-slide {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
  padding: $spacing-xl;
}

.test-slide h3 {
  font-size: $font-size-xl;
  margin-bottom: $spacing-md;
}

.test-slide p {
  font-size: $font-size-lg;
  opacity: 0.9;
}

.test-card {
  background: white;
  border-radius: $border-radius;
  padding: $spacing-lg;
  text-align: center;
  box-shadow: $box-shadow;
  margin: 0 $spacing-sm;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto $spacing-md;
  color: white;
  font-size: 1.5rem;
}

.test-card h4 {
  font-size: $font-size-lg;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.test-card p {
  color: $text-secondary;
  font-size: $font-size-sm;
}

.progress-slide {
  height: 250px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
}

.slide-content {
  text-align: center;
  color: $text-primary;
}

.slide-icon {
  font-size: 3rem;
  margin-bottom: $spacing-lg;
}

.slide-content h3 {
  font-size: $font-size-xl;
  margin-bottom: $spacing-md;
}

.slide-content p {
  font-size: $font-size-md;
  color: $text-secondary;
  max-width: 500px;
}

.number-slide {
  height: 300px;
  background: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: $spacing-xl;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
}

.slide-number {
  font-size: 4rem;
  font-weight: bold;
  color: $education-blue;
  margin-bottom: $spacing-lg;
}

.number-slide h3 {
  font-size: $font-size-xl;
  color: $text-primary;
  margin-bottom: $spacing-md;
}

.number-slide p {
  font-size: $font-size-md;
  color: $text-secondary;
  max-width: 400px;
}

.test-info {
  background: white;
  border-radius: $border-radius;
  padding: $spacing-xl;
  box-shadow: $box-shadow;
  margin-top: $spacing-xxl;
}

.test-info h3 {
  font-size: $font-size-lg;
  color: $text-primary;
  margin-bottom: $spacing-md;
}

.test-info ul {
  list-style: none;
  padding: 0;
}

.test-info li {
  padding: $spacing-sm 0;
  color: $text-secondary;
  position: relative;
  padding-left: $spacing-lg;
}

.test-info li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: $success-color;
  font-weight: bold;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .swipe-test {
    padding: $spacing-lg;
  }
  
  .test-header h1 {
    font-size: 2rem;
  }
  
  .test-slide {
    height: 200px;
    padding: $spacing-lg;
  }
  
  .test-slide h3 {
    font-size: $font-size-lg;
  }
  
  .test-slide p {
    font-size: $font-size-md;
  }
  
  .progress-slide {
    height: 200px;
  }
  
  .slide-icon {
    font-size: 2rem;
  }
  
  .number-slide {
    height: 250px;
  }
  
  .slide-number {
    font-size: 3rem;
  }
}
</style>

