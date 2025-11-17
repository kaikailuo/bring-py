<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="updateModelValue"
    title="徽章详情"
    width="500px"
    :close-on-click-modal="true"
  >
    <div class="badge-modal-content" v-if="badge">
      <div class="modal-badge-icon">
        <div class="icon-circle">
          <span class="icon-emoji">{{ badge.icon }}</span>
        </div>
      </div>
      
      <div class="modal-badge-info">
        <h2 class="modal-badge-name">{{ badge.name }}</h2>
        <p class="modal-badge-description">{{ badge.description }}</p>
        
        <div class="modal-badge-details">
          <div class="detail-item">
            <el-icon><Folder /></el-icon>
            <span class="detail-label">分类：</span>
            <span class="detail-value">{{ badge.category }}</span>
          </div>
          
          <div class="detail-item" v-if="badge.date">
            <el-icon><Calendar /></el-icon>
            <span class="detail-label">获得时间：</span>
            <span class="detail-value">{{ formatDate(badge.date) }}</span>
          </div>
          
          <div class="detail-item">
            <el-icon><Trophy /></el-icon>
            <span class="detail-label">获得条件：</span>
            <span class="detail-value">{{ badge.requirement }}</span>
          </div>
        </div>
        
        <div class="modal-badge-status">
          <el-tag type="success" size="large">
            <el-icon><Check /></el-icon>
            已获得
          </el-tag>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  badge: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const updateModelValue = (value) => {
  emit('update:modelValue', value)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style lang="scss" scoped>
.badge-modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: $spacing-lg;
}

.modal-badge-icon {
  margin-bottom: $spacing-xl;
}

.icon-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.icon-emoji {
  display: block;
  line-height: 1;
}

.modal-badge-info {
  width: 100%;
  text-align: center;
}

.modal-badge-name {
  font-size: $font-size-xxl;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-md 0;
}

.modal-badge-description {
  font-size: $font-size-md;
  color: $text-secondary;
  margin: 0 0 $spacing-xl 0;
  line-height: 1.6;
}

.modal-badge-details {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
  margin-bottom: $spacing-xl;
  padding: $spacing-lg;
  background: $bg-secondary;
  border-radius: $border-radius;
  text-align: left;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: $font-size-sm;
  
  .el-icon {
    color: $education-purple;
    font-size: $font-size-md;
  }
}

.detail-label {
  color: $text-secondary;
  min-width: 80px;
}

.detail-value {
  color: $text-primary;
  font-weight: 500;
}

.modal-badge-status {
  display: flex;
  justify-content: center;
  
  .el-tag {
    padding: $spacing-sm $spacing-lg;
    font-size: $font-size-md;
    
    .el-icon {
      margin-right: $spacing-xs;
    }
  }
}
</style>

