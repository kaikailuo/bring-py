<template>
  <div class="progress-view">
    <div class="progress-overview">
      <div class="overall-progress">
        <h3 class="progress-title">总体学习进度</h3>
        <div class="progress-circle">
          <div class="circle-progress">
            <el-progress 
              type="circle" 
              :percentage="data.overallProgress" 
              :width="120"
              :stroke-width="8"
              :color="progressColor"
            >
              <template #default="{ percentage }">
                <span class="progress-text">{{ percentage }}%</span>
              </template>
            </el-progress>
          </div>
          <div class="progress-info">
            <div class="progress-label">已完成</div>
            <div class="progress-detail">{{ data.completedModules }}/{{ data.totalModules }} 个模块</div>
          </div>
        </div>
      </div>
      
      <div class="weekly-progress">
        <h3 class="progress-title">本周学习进度</h3>
        <div class="week-stats">
          <div class="week-item" v-for="day in data.weeklyProgress" :key="day.day">
            <div class="day-label">{{ day.day }}</div>
            <div class="day-progress">
              <el-progress 
                :percentage="day.progress" 
                :stroke-width="4"
                :show-text="false"
                :color="day.progress > 50 ? '#52c41a' : day.progress > 20 ? '#faad14' : '#f5f5f5'"
              />
            </div>
            <div class="day-time">{{ day.time }}</div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="module-progress">
      <h3 class="progress-title">模块学习进度</h3>
      <div class="modules-list">
        <div class="module-item" v-for="module in data.modules" :key="module.id">
          <div class="module-info">
            <div class="module-icon" :class="module.status">
              <el-icon><component :is="module.icon" /></el-icon>
            </div>
            <div class="module-content">
              <div class="module-name">{{ module.name }}</div>
              <div class="module-desc">{{ module.description }}</div>
            </div>
          </div>
          <div class="module-progress-bar">
            <el-progress 
              :percentage="module.progress" 
              :stroke-width="6"
              :color="getModuleColor(module.progress)"
            />
            <div class="module-status">{{ getModuleStatus(module.status, module.progress) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  }
})

const progressColor = computed(() => {
  const progress = props.data.overallProgress || 0
  if (progress >= 80) return '#52c41a'
  if (progress >= 50) return '#faad14'
  if (progress >= 20) return '#1890ff'
  return '#f5f5f5'
})

const getModuleColor = (progress) => {
  if (progress >= 80) return '#52c41a'
  if (progress >= 50) return '#faad14'
  if (progress >= 20) return '#1890ff'
  return '#f5f5f5'
}

const getModuleStatus = (status, progress) => {
  if (status === 'completed') return '已完成'
  if (status === 'in-progress') return `进行中 ${progress}%`
  if (status === 'locked') return '未解锁'
  return '未开始'
}
</script>

<style lang="scss" scoped>
.progress-view {
  width: 100%;
}

.progress-overview {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: $spacing-xl;
  margin-bottom: $spacing-xl;
}

.overall-progress,
.weekly-progress {
  background: white;
  border-radius: $border-radius;
  padding: $spacing-lg;
  box-shadow: $box-shadow;
}

.progress-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin-bottom: $spacing-lg;
  border-bottom: 2px solid $education-blue;
  padding-bottom: $spacing-sm;
}

.progress-circle {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
}

.circle-progress {
  flex-shrink: 0;
}

.progress-text {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
}

.progress-info {
  flex: 1;
}

.progress-label {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.progress-detail {
  color: $text-secondary;
  font-size: $font-size-sm;
}

.week-stats {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.week-item {
  display: grid;
  grid-template-columns: 60px 1fr 60px;
  gap: $spacing-md;
  align-items: center;
}

.day-label {
  font-size: $font-size-sm;
  color: $text-secondary;
  text-align: center;
}

.day-progress {
  flex: 1;
}

.day-time {
  font-size: $font-size-xs;
  color: $text-light;
  text-align: right;
}

.module-progress {
  background: white;
  border-radius: $border-radius;
  padding: $spacing-lg;
  box-shadow: $box-shadow;
}

.modules-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.module-item {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  padding: $spacing-md;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.module-info {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  flex: 1;
}

.module-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: white;
  
  &.completed {
    background: $success-color;
  }
  
  &.in-progress {
    background: $warning-color;
  }
  
  &.locked {
    background: $text-light;
  }
  
  &.pending {
    background: $education-blue;
  }
}

.module-content {
  flex: 1;
}

.module-name {
  font-weight: bold;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.module-desc {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.module-progress-bar {
  width: 200px;
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
}

.module-status {
  font-size: $font-size-xs;
  color: $text-secondary;
  text-align: center;
}

@media (max-width: 768px) {
  .progress-overview {
    grid-template-columns: 1fr;
  }
  
  .progress-circle {
    flex-direction: column;
    text-align: center;
  }
  
  .module-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .module-info {
    width: 100%;
  }
  
  .module-progress-bar {
    width: 100%;
  }
  
  .week-item {
    grid-template-columns: 1fr;
    gap: $spacing-sm;
    text-align: center;
  }
}
</style>

