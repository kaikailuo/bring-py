<template>
  <div class="overview-view">
    <div class="overview-cards">
      <div class="overview-card education-card">
        <div class="card-icon completed">
          <el-icon><Check /></el-icon>
        </div>
        <div class="card-content">
          <div class="card-title">已完成课程</div>
          <div class="card-value">{{ data.completedCourses }}</div>
          <div class="card-progress">
            <el-progress :percentage="data.completedPercentage" :stroke-width="6" />
          </div>
        </div>
      </div>
      
      <div class="overview-card education-card">
        <div class="card-icon in-progress">
          <el-icon><Clock /></el-icon>
        </div>
        <div class="card-content">
          <div class="card-title">进行中课程</div>
          <div class="card-value">{{ data.inProgressCourses }}</div>
          <div class="card-progress">
            <el-progress :percentage="data.inProgressPercentage" :stroke-width="6" />
          </div>
        </div>
      </div>
      
      <div class="overview-card education-card">
        <div class="card-icon practice">
          <el-icon><EditPen /></el-icon>
        </div>
        <div class="card-content">
          <div class="card-title">编程练习</div>
          <div class="card-value">{{ data.practiceCount }}</div>
          <div class="card-progress">
            <el-progress :percentage="data.practicePercentage" :stroke-width="6" />
          </div>
        </div>
      </div>
      
      <div class="overview-card education-card">
        <div class="card-icon achievements">
          <el-icon><Trophy /></el-icon>
        </div>
        <div class="card-content">
          <div class="card-title">获得徽章</div>
          <div class="card-value">{{ data.achievements }}</div>
          <div class="card-progress">
            <el-progress :percentage="100" :stroke-width="6" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  data: {
    type: Object,
    default: () => ({})
  }
})
</script>

<style lang="scss" scoped>
.overview-view {
  width: 100%;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: $spacing-lg;
}

.overview-card {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  padding: $spacing-xl;
}

.card-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  
  &.completed {
    background: $success-color;
  }
  
  &.in-progress {
    background: $warning-color;
  }
  
  &.practice {
    background: $education-blue;
  }
  
  &.achievements {
    background: $education-purple;
  }
}

.card-content {
  flex: 1;
}

.card-title {
  font-size: $font-size-sm;
  color: $text-secondary;
  margin-bottom: $spacing-xs;
}

.card-value {
  font-size: 2rem;
  font-weight: bold;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.card-progress {
  width: 100%;
}

@media (max-width: 768px) {
  .overview-cards {
    grid-template-columns: 1fr;
  }
  
  .overview-card {
    flex-direction: column;
    text-align: center;
  }
}
</style>

