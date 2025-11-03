<template>
  <el-dialog
    v-model="visible"
    title="生成问题智能总结"
    width="600px"
    :before-close="handleClose"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
      <el-form-item label="总结类型" prop="summaryType">
        <el-radio-group v-model="form.summaryType">
          <el-radio value="daily">日总结</el-radio>
          <el-radio value="weekly">周总结</el-radio>
          <el-radio value="monthly">月总结</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item label="时间范围" prop="timeRange">
        <el-date-picker
          v-model="form.timeRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      
      <el-form-item label="分析选项">
        <el-checkbox-group v-model="form.analysisOptions">
          <el-checkbox value="category">问题分类分析</el-checkbox>
          <el-checkbox value="trend">趋势分析</el-checkbox>
          <el-checkbox value="keywords">关键词提取</el-checkbox>
          <el-checkbox value="recommendations">智能建议</el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      
      <el-form-item label="总结标题" prop="title">
        <el-input v-model="form.title" placeholder="请输入总结标题" />
      </el-form-item>
      
      <el-form-item label="备注">
        <el-input
          v-model="form.notes"
          type="textarea"
          :rows="3"
          placeholder="可选：添加备注信息"
        />
      </el-form-item>
    </el-form>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleGenerate" :loading="loading">
          <el-icon><Magic /></el-icon>
          生成总结
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'generate'])

// 响应式数据
const formRef = ref()
const loading = ref(false)
const form = ref({
  summaryType: 'weekly',
  timeRange: [],
  analysisOptions: ['category', 'trend', 'keywords', 'recommendations'],
  title: '',
  notes: ''
})

// 表单验证规则
const rules = {
  summaryType: [
    { required: true, message: '请选择总结类型', trigger: 'change' }
  ],
  timeRange: [
    { required: true, message: '请选择时间范围', trigger: 'change' }
  ],
  title: [
    { required: true, message: '请输入总结标题', trigger: 'blur' }
  ]
}

// 计算属性
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 监听总结类型变化，自动设置时间范围
watch(() => form.value.summaryType, (newType) => {
  const today = new Date()
  let startDate, endDate
  
  switch (newType) {
    case 'daily':
      startDate = new Date(today)
      endDate = new Date(today)
      break
    case 'weekly':
      startDate = new Date(today.setDate(today.getDate() - today.getDay()))
      endDate = new Date(today.setDate(today.getDate() - today.getDay() + 6))
      break
    case 'monthly':
      startDate = new Date(today.getFullYear(), today.getMonth(), 1)
      endDate = new Date(today.getFullYear(), today.getMonth() + 1, 0)
      break
  }
  
  form.value.timeRange = [
    startDate.toISOString().split('T')[0],
    endDate.toISOString().split('T')[0]
  ]
  
  // 自动生成标题
  const typeText = { daily: '日总结', weekly: '周总结', monthly: '月总结' }
  form.value.title = `${typeText[newType]} - ${form.value.timeRange[0]} 至 ${form.value.timeRange[1]}`
}, { immediate: true })

// 方法
const handleClose = () => {
  visible.value = false
  resetForm()
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  form.value = {
    summaryType: 'weekly',
    timeRange: [],
    analysisOptions: ['category', 'trend', 'keywords', 'recommendations'],
    title: '',
    notes: ''
  }
}

const handleGenerate = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    loading.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 发送生成事件
    emit('generate', {
      ...form.value,
      startDate: form.value.timeRange[0],
      endDate: form.value.timeRange[1]
    })
    
    ElMessage.success('问题总结生成成功！')
    handleClose()
    
  } catch (error) {
    console.error('生成总结失败:', error)
    ElMessage.error('生成总结失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: $spacing-md;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-radio-group) {
  display: flex;
  gap: $spacing-lg;
}

:deep(.el-checkbox-group) {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $spacing-sm;
}
</style>
