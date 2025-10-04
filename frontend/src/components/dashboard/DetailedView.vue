<template>
  <div class="detailed-view">
    <div class="detailed-stats">
      <div class="stat-section">
        <h3 class="stat-title">学习时长统计</h3>
        <div class="time-stats">
          <div class="time-item">
            <div class="time-label">今日学习</div>
            <div class="time-value">{{ data.todayStudyTime }}</div>
          </div>
          <div class="time-item">
            <div class="time-label">本周学习</div>
            <div class="time-value">{{ data.weekStudyTime }}</div>
          </div>
          <div class="time-item">
            <div class="time-label">总学习时长</div>
            <div class="time-value">{{ data.totalStudyTime }}</div>
          </div>
        </div>
      </div>
      
      <div class="stat-section">
        <h3 class="stat-title">学习效率分析</h3>
        <div class="efficiency-stats">
          <div class="efficiency-item">
            <div class="efficiency-label">代码完成率</div>
            <div class="efficiency-progress">
              <el-progress :percentage="data.codeCompletionRate" :stroke-width="8" />
              <span class="progress-text">{{ data.codeCompletionRate }}%</span>
            </div>
          </div>
          <div class="efficiency-item">
            <div class="efficiency-label">练习正确率</div>
            <div class="efficiency-progress">
              <el-progress :percentage="data.exerciseAccuracy" :stroke-width="8" />
              <span class="progress-text">{{ data.exerciseAccuracy }}%</span>
            </div>
          </div>
          <div class="efficiency-item">
            <div class="efficiency-label">知识点掌握度</div>
            <div class="efficiency-progress">
              <el-progress :percentage="data.knowledgeMastery" :stroke-width="8" />
              <span class="progress-text">{{ data.knowledgeMastery }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="achievement-showcase">
      <h3 class="achievement-title">最新成就</h3>
      <div class="achievements-grid">
        <div class="achievement-item" v-for="achievement in data.recentAchievements" :key="achievement.id">
          <div class="achievement-icon">
            <el-icon><component :is="achievement.icon" /></el-icon>
          </div>
          <div class="achievement-content">
            <div class="achievement-name">{{ achievement.name }}</div>
            <div class="achievement-desc">{{ achievement.description }}</div>
            <div class="achievement-date">{{ achievement.date }}</div>
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
.detailed-view {
  width: 100%;
}

.detailed-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-xl;
  margin-bottom: $spacing-xl;
}

.stat-section {
  background: white;
  border-radius: $border-radius;
  padding: $spacing-lg;
  box-shadow: $box-shadow;
}

.stat-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin-bottom: $spacing-lg;
  border-bottom: 2px solid $education-blue;
  padding-bottom: $spacing-sm;
}

.time-stats {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.time-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-sm $spacing-md;
  background: $bg-secondary;
  border-radius: $border-radius;
}

.time-label {
  color: $text-secondary;
  font-size: $font-size-sm;
}

.time-value {
  font-weight: bold;
  color: $education-blue;
  font-size: $font-size-lg;
}

.efficiency-stats {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.efficiency-item {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.efficiency-label {
  color: $text-secondary;
  font-size: $font-size-sm;
}

.efficiency-progress {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.progress-text {
  font-weight: bold;
  color: $education-blue;
  min-width: 40px;
}

.achievement-showcase {
  background: white;
  border-radius: $border-radius;
  padding: $spacing-lg;
  box-shadow: $box-shadow;
}

.achievement-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin-bottom: $spacing-lg;
  border-bottom: 2px solid $education-purple;
  padding-bottom: $spacing-sm;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: $spacing-md;
}

.achievement-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-md;
  background: $bg-secondary;
  border-radius: $border-radius;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: $box-shadow-hover;
  }
}

.achievement-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: $education-purple;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.achievement-content {
  flex: 1;
}

.achievement-name {
  font-weight: bold;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.achievement-desc {
  font-size: $font-size-sm;
  color: $text-secondary;
  margin-bottom: $spacing-xs;
}

.achievement-date {
  font-size: $font-size-xs;
  color: $text-light;
}

@media (max-width: 768px) {
  .detailed-stats {
    grid-template-columns: 1fr;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
  }
  
  .achievement-item {
    flex-direction: column;
    text-align: center;
  }
}
</style>

