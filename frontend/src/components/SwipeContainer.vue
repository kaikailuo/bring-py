<template>
  <div class="swipe-container" ref="containerRef">
    <!-- 滑动指示器 -->
    <SwipeIndicators
      v-if="showIndicators && items.length > 1"
      :items="items"
      :current-index="currentIndex"
      :type="indicatorType"
      :show-progress="showProgress"
      :autoplay="autoplay"
      :autoplay-delay="autoplayDelay"
      :color="indicatorColor"
      :size="indicatorSize"
      @slide-change="goToSlide"
    />

    <!-- 滑动内容区域 -->
    <div 
      class="swipe-content"
      :style="contentStyle"
      @touchstart="handleTouchStart"
      @touchmove="handleTouchMove"
      @touchend="handleTouchEnd"
      @mousedown="handleMouseDown"
      @mousemove="handleMouseMove"
      @mouseup="handleMouseUp"
      @mouseleave="handleMouseUp"
    >
      <div 
        v-for="(item, index) in items" 
        :key="index"
        class="swipe-item"
        :class="{ active: currentIndex === index }"
      >
        <slot :item="item" :index="index">
          {{ item }}
        </slot>
      </div>
    </div>

    <!-- 导航按钮 -->
    <div class="swipe-nav" v-if="showNavigation && items.length > 1">
      <button 
        class="nav-btn prev-btn" 
        @click="prevSlide"
        :disabled="!loop && currentIndex === 0"
      >
        <el-icon><ArrowLeft /></el-icon>
      </button>
      <button 
        class="nav-btn next-btn" 
        @click="nextSlide"
        :disabled="!loop && currentIndex === items.length - 1"
      >
        <el-icon><ArrowRight /></el-icon>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import SwipeIndicators from './SwipeIndicators.vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  autoplay: {
    type: Boolean,
    default: false
  },
  autoplayDelay: {
    type: Number,
    default: 3000
  },
  loop: {
    type: Boolean,
    default: true
  },
  showIndicators: {
    type: Boolean,
    default: true
  },
  showNavigation: {
    type: Boolean,
    default: true
  },
  itemsPerView: {
    type: Number,
    default: 1
  },
  gap: {
    type: Number,
    default: 16
  },
  transition: {
    type: String,
    default: 'slide' // 'slide', 'fade'
  },
  indicatorType: {
    type: String,
    default: 'dots' // 'dots', 'bars', 'numbers', 'thumbnails'
  },
  showProgress: {
    type: Boolean,
    default: false
  },
  indicatorColor: {
    type: String,
    default: '#1890ff'
  },
  indicatorSize: {
    type: String,
    default: 'medium' // 'small', 'medium', 'large'
  }
})

const emit = defineEmits(['slide-change', 'touch-start', 'touch-end'])

// 响应式数据
const containerRef = ref(null)
const currentIndex = ref(0)
const isDragging = ref(false)
const startX = ref(0)
const currentX = ref(0)
const translateX = ref(0)
const autoplayTimer = ref(null)

// 计算属性
const contentStyle = computed(() => {
  const itemWidth = 100 / props.itemsPerView
  const offset = -(currentIndex.value * itemWidth) + (translateX.value / containerRef.value?.offsetWidth * 100)
  
  if (props.transition === 'fade') {
    return {
      transform: `translateX(${offset}%)`,
      transition: isDragging.value ? 'none' : 'transform 0.3s ease'
    }
  }
  
  return {
    transform: `translateX(${offset}%)`,
    transition: isDragging.value ? 'none' : 'transform 0.3s ease',
    gap: `${props.gap}px`
  }
})

// 触摸事件处理
const handleTouchStart = (e) => {
  if (props.items.length <= 1) return
  
  isDragging.value = true
  startX.value = e.touches[0].clientX
  currentX.value = e.touches[0].clientX
  stopAutoplay()
  emit('touch-start', e)
}

const handleTouchMove = (e) => {
  if (!isDragging.value) return
  
  e.preventDefault()
  currentX.value = e.touches[0].clientX
  const diff = currentX.value - startX.value
  translateX.value = diff
}

const handleTouchEnd = () => {
  if (!isDragging.value) return
  
  const diff = currentX.value - startX.value
  const threshold = containerRef.value?.offsetWidth * 0.2
  
  if (Math.abs(diff) > threshold) {
    if (diff > 0) {
      prevSlide()
    } else {
      nextSlide()
    }
  }
  
  isDragging.value = false
  translateX.value = 0
  startAutoplay()
  emit('touch-end')
}

// 鼠标事件处理
const handleMouseDown = (e) => {
  if (props.items.length <= 1) return
  
  isDragging.value = true
  startX.value = e.clientX
  currentX.value = e.clientX
  stopAutoplay()
  e.preventDefault()
}

const handleMouseMove = (e) => {
  if (!isDragging.value) return
  
  currentX.value = e.clientX
  const diff = currentX.value - startX.value
  translateX.value = diff
}

const handleMouseUp = () => {
  if (!isDragging.value) return
  
  const diff = currentX.value - startX.value
  const threshold = containerRef.value?.offsetWidth * 0.2
  
  if (Math.abs(diff) > threshold) {
    if (diff > 0) {
      prevSlide()
    } else {
      nextSlide()
    }
  }
  
  isDragging.value = false
  translateX.value = 0
  startAutoplay()
}

// 滑动控制方法
const goToSlide = (index) => {
  if (index >= 0 && index < props.items.length) {
    currentIndex.value = index
    emit('slide-change', index)
  }
}

const nextSlide = () => {
  if (props.loop) {
    currentIndex.value = (currentIndex.value + 1) % props.items.length
  } else if (currentIndex.value < props.items.length - 1) {
    currentIndex.value++
  }
  emit('slide-change', currentIndex.value)
}

const prevSlide = () => {
  if (props.loop) {
    currentIndex.value = currentIndex.value === 0 ? props.items.length - 1 : currentIndex.value - 1
  } else if (currentIndex.value > 0) {
    currentIndex.value--
  }
  emit('slide-change', currentIndex.value)
}

// 自动播放
const startAutoplay = () => {
  if (props.autoplay && props.items.length > 1) {
    stopAutoplay()
    autoplayTimer.value = setInterval(() => {
      nextSlide()
    }, props.autoplayDelay)
  }
}

const stopAutoplay = () => {
  if (autoplayTimer.value) {
    clearInterval(autoplayTimer.value)
    autoplayTimer.value = null
  }
}

// 键盘事件
const handleKeydown = (e) => {
  if (e.key === 'ArrowLeft') {
    prevSlide()
  } else if (e.key === 'ArrowRight') {
    nextSlide()
  }
}

// 生命周期
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
  startAutoplay()
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  stopAutoplay()
})

// 暴露方法给父组件
defineExpose({
  goToSlide,
  nextSlide,
  prevSlide,
  currentIndex
})
</script>

<style lang="scss" scoped>
.swipe-container {
  position: relative;
  width: 100%;
  overflow: hidden;
  border-radius: $border-radius;
}

.swipe-content {
  display: flex;
  width: 100%;
  transition: transform 0.3s ease;
}

.swipe-item {
  flex: 0 0 100%;
  min-height: 200px;
  opacity: 0;
  transition: opacity 0.3s ease;
  
  &.active {
    opacity: 1;
  }
}

/* 指示器样式已移至 SwipeIndicators 组件 */

.swipe-nav {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  transform: translateY(-50%);
  display: flex;
  justify-content: space-between;
  pointer-events: none;
  z-index: 10;
}

.nav-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: $text-primary;
  transition: all 0.3s ease;
  pointer-events: auto;
  box-shadow: $box-shadow;
  
  &:hover:not(:disabled) {
    background: white;
    transform: scale(1.1);
    box-shadow: $box-shadow-hover;
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.prev-btn {
  margin-left: $spacing-md;
}

.next-btn {
  margin-right: $spacing-md;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-btn {
    width: 32px;
    height: 32px;
    font-size: 1rem;
  }
  
  .prev-btn {
    margin-left: $spacing-sm;
  }
  
  .next-btn {
    margin-right: $spacing-sm;
  }
  
  .indicator {
    width: 6px;
    height: 6px;
  }
}

/* 多项目显示样式 */
.swipe-container[data-items-per-view="2"] .swipe-item {
  flex: 0 0 50%;
}

.swipe-container[data-items-per-view="3"] .swipe-item {
  flex: 0 0 33.333%;
}

.swipe-container[data-items-per-view="4"] .swipe-item {
  flex: 0 0 25%;
}

@media (max-width: 768px) {
  .swipe-container[data-items-per-view="3"] .swipe-item,
  .swipe-container[data-items-per-view="4"] .swipe-item {
    flex: 0 0 50%;
  }
}

@media (max-width: 480px) {
  .swipe-container[data-items-per-view="2"] .swipe-item,
  .swipe-container[data-items-per-view="3"] .swipe-item,
  .swipe-container[data-items-per-view="4"] .swipe-item {
    flex: 0 0 100%;
  }
}
</style>
