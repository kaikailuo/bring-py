<template>
  <div class="swipe-indicators" :class="indicatorClass">
    <div 
      v-for="(item, index) in items" 
      :key="index"
      class="indicator"
      :class="{ 
        active: currentIndex === index,
        'animate-in': shouldAnimate && currentIndex === index
      }"
      :style="getIndicatorStyle(index)"
      @click="goToSlide(index)"
    >
      <div class="indicator-inner"></div>
      <div class="indicator-progress" v-if="showProgress && currentIndex === index">
        <div class="progress-bar" :style="progressStyle"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted,watch, onUnmounted } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  currentIndex: {
    type: Number,
    default: 0
  },
  type: {
    type: String,
    default: 'dots', // 'dots', 'bars', 'numbers', 'thumbnails'
    validator: (value) => ['dots', 'bars', 'numbers', 'thumbnails'].includes(value)
  },
  showProgress: {
    type: Boolean,
    default: false
  },
  autoplay: {
    type: Boolean,
    default: false
  },
  autoplayDelay: {
    type: Number,
    default: 3000
  },
  color: {
    type: String,
    default: '#1890ff'
  },
  size: {
    type: String,
    default: 'medium', // 'small', 'medium', 'large'
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
})

const emit = defineEmits(['slide-change'])

// 响应式数据
const shouldAnimate = ref(false)
const progressWidth = ref(0)
const progressTimer = ref(null)

// 计算属性
const indicatorClass = computed(() => ({
  [`indicators-${props.type}`]: true,
  [`indicators-${props.size}`]: true,
  'indicators-with-progress': props.showProgress
}))

const progressStyle = computed(() => ({
  width: `${progressWidth.value}%`,
  backgroundColor: props.color,
  transition: 'width 0.1s linear'
}))

// 方法
const goToSlide = (index) => {
  emit('slide-change', index)
}

const getIndicatorStyle = (index) => {
  const isActive = props.currentIndex === index
  const baseStyle = {
    backgroundColor: isActive ? props.color : 'rgba(255, 255, 255, 0.5)'
  }

  if (props.type === 'thumbnails' && props.items[index]?.thumbnail) {
    return {
      ...baseStyle,
      backgroundImage: `url(${props.items[index].thumbnail})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center'
    }
  }

  return baseStyle
}

const startProgress = () => {
  if (!props.showProgress || !props.autoplay) return
  
  progressWidth.value = 0
  const startTime = Date.now()
  const duration = props.autoplayDelay
  
  const updateProgress = () => {
    const elapsed = Date.now() - startTime
    const progress = Math.min((elapsed / duration) * 100, 100)
    progressWidth.value = progress
    
    if (progress < 100) {
      progressTimer.value = requestAnimationFrame(updateProgress)
    }
  }
  
  progressTimer.value = requestAnimationFrame(updateProgress)
}

const stopProgress = () => {
  if (progressTimer.value) {
    cancelAnimationFrame(progressTimer.value)
    progressTimer.value = null
  }
  progressWidth.value = 0
}

// 监听当前索引变化
const handleIndexChange = () => {
  shouldAnimate.value = true
  setTimeout(() => {
    shouldAnimate.value = false
  }, 300)
  
  if (props.showProgress && props.autoplay) {
    stopProgress()
    startProgress()
  }
}

// 生命周期
onMounted(() => {
  if (props.showProgress && props.autoplay) {
    startProgress()
  }
})

onUnmounted(() => {
  stopProgress()
})

// 监听props变化
watch(() => props.currentIndex, handleIndexChange)
</script>

<style lang="scss" scoped>
.swipe-indicators {
  display: flex;
  gap: $spacing-sm;
  justify-content: center;
  align-items: center;
  z-index: 10;
  position: relative;
}

.indicator {
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.indicator-inner {
  width: 100%;
  height: 100%;
  border-radius: inherit;
  transition: all 0.3s ease;
}

.indicator-progress {
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: rgba(255, 255, 255, 0.2);
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: currentColor;
  transition: width 0.1s linear;
}

/* 点状指示器 */
.indicators-dots .indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.indicators-dots.indicators-small .indicator {
  width: 6px;
  height: 6px;
}

.indicators-dots.indicators-large .indicator {
  width: 12px;
  height: 12px;
}

.indicators-dots .indicator.active {
  transform: scale(1.2);
}

.indicators-dots .indicator.animate-in {
  animation: pulse 0.3s ease;
}

/* 条形指示器 */
.indicators-bars .indicator {
  width: 20px;
  height: 4px;
  border-radius: 2px;
}

.indicators-bars.indicators-small .indicator {
  width: 16px;
  height: 3px;
}

.indicators-bars.indicators-large .indicator {
  width: 24px;
  height: 6px;
}

.indicators-bars .indicator.active {
  transform: scaleX(1.2);
}

/* 数字指示器 */
.indicators-numbers .indicator {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: $font-size-sm;
  font-weight: bold;
  color: white;
  background: rgba(255, 255, 255, 0.3);
}

.indicators-numbers.indicators-small .indicator {
  width: 24px;
  height: 24px;
  font-size: $font-size-xs;
}

.indicators-numbers.indicators-large .indicator {
  width: 40px;
  height: 40px;
  font-size: $font-size-md;
}

.indicators-numbers .indicator.active {
  background: currentColor;
  transform: scale(1.1);
}

/* 缩略图指示器 */
.indicators-thumbnails .indicator {
  width: 48px;
  height: 32px;
  border-radius: $border-radius;
  border: 2px solid transparent;
  overflow: hidden;
}

.indicators-thumbnails.indicators-small .indicator {
  width: 36px;
  height: 24px;
}

.indicators-thumbnails.indicators-large .indicator {
  width: 64px;
  height: 40px;
}

.indicators-thumbnails .indicator.active {
  border-color: currentColor;
  transform: scale(1.05);
}

/* 悬停效果 */
.indicator:hover {
  opacity: 0.8;
  transform: scale(1.1);
}

.indicators-bars .indicator:hover {
  transform: scaleY(1.2);
}

.indicators-numbers .indicator:hover {
  background: rgba(255, 255, 255, 0.5);
}

.indicators-thumbnails .indicator:hover {
  border-color: rgba(255, 255, 255, 0.8);
}

/* 动画效果 */
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.3);
  }
  100% {
    transform: scale(1.2);
  }
}

@keyframes slideIn {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.indicator.animate-in {
  animation: slideIn 0.3s ease;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .indicators-thumbnails .indicator {
    width: 40px;
    height: 28px;
  }
  
  .indicators-numbers .indicator {
    width: 28px;
    height: 28px;
    font-size: $font-size-xs;
  }
}

@media (max-width: 480px) {
  .swipe-indicators {
    gap: $spacing-xs;
  }
  
  .indicators-thumbnails .indicator {
    width: 32px;
    height: 24px;
  }
  
  .indicators-numbers .indicator {
    width: 24px;
    height: 24px;
    font-size: 10px;
  }
}
</style>

