<template>
  <div
    class="badge-card"
    :class="{ 'obtained': badge.obtained, 'locked': !badge.obtained }"
    @click="handleClick"
  >
    <div class="badge-icon-wrapper">
      <div class="badge-icon" :class="{ 'grayscale': !badge.obtained }">
        <span class="icon-emoji">{{ badge.icon }}</span>
      </div>
      <div v-if="!badge.obtained" class="lock-overlay">
        <el-icon class="lock-icon"><Lock /></el-icon>
      </div>
    </div>
    <div class="badge-info">
      <h3 class="badge-name">{{ badge.name }}</h3>
      <p class="badge-description">{{ badge.description }}</p>
      <div v-if="badge.obtained && badge.date" class="badge-date">
        <el-icon><Calendar /></el-icon>
        <span>获得于 {{ formatDate(badge.date) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  badge: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click'])

const handleClick = () => {
  if (props.badge.obtained) {
    emit('click', props.badge)
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style lang="scss" scoped>
.badge-card {
  background: white;
  border-radius: $border-radius;
  padding: $spacing-lg;
  box-shadow: $box-shadow;
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  height: 100%;
  
  &.obtained {
    border: 2px solid transparent;
    
    &:hover {
      transform: translateY(-4px);
      box-shadow: $box-shadow-hover;
      border-color: $education-purple;
    }
  }
  
  &.locked {
    opacity: 0.6;
    cursor: not-allowed;
    filter: grayscale(0.3);
  }
}

.badge-icon-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: $spacing-md;
}

.badge-icon {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  transition: all 0.3s ease;
  
  &.grayscale {
    background: linear-gradient(135deg, #d9d9d9 0%, #bfbfbf 100%);
    filter: grayscale(0.5);
  }
}

.icon-emoji {
  display: block;
  line-height: 1;
}

.lock-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lock-icon {
  font-size: 1.5rem;
  color: white;
  z-index: 1;
}

.badge-info {
  flex: 1;
  width: 100%;
}

.badge-name {
  font-size: $font-size-md;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-xs 0;
}

.badge-description {
  font-size: $font-size-sm;
  color: $text-secondary;
  margin: 0 0 $spacing-sm 0;
  line-height: 1.5;
}

.badge-date {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: $spacing-xs;
  font-size: $font-size-xs;
  color: $education-purple;
  margin-top: $spacing-sm;
  
  .el-icon {
    font-size: $font-size-xs;
  }
}

.obtained .badge-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.locked .badge-icon {
  background: linear-gradient(135deg, #d9d9d9 0%, #bfbfbf 100%);
}
</style>

