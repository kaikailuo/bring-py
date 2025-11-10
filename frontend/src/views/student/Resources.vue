<template>
  <div class="resources-page">
    <div class="resources-header">
      <h1 class="page-title">教学资源</h1>
      <div class="header-actions">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索资源..."
          prefix-icon="Search"
          style="width: 300px"
          @input="handleSearch"
        />
        <el-select v-model="selectedCourse" placeholder="选择课程" style="width: 150px" @change="handleSearch">
          <el-option label="全部课程" value="all" />
          <el-option label="全部" value="all_course" />
          <el-option label="第一课" value="lesson1" />
        </el-select>
        <el-select v-model="selectedCategory" placeholder="选择分类" style="width: 150px">
          <el-option label="全部" value="all" />
          <el-option label="Python基础" value="python-basic" />
          <el-option label="数据结构" value="data-structure" />
          <el-option label="算法" value="algorithm" />
          <el-option label="面向对象" value="oop" />
        </el-select>
      </div>
    </div>

    <div class="resources-content">
      <!-- 资源分类导航 -->
      <div class="category-nav">
        <div class="nav-item" 
             v-for="category in categories" 
             :key="category.id"
             :class="{ active: selectedCategory === category.id }"
             @click="selectCategory(category.id)">
          <div class="nav-icon">
            <el-icon><component :is="category.icon" /></el-icon>
          </div>
          <span class="nav-label">{{ category.name }}</span>
          <span class="nav-count">{{ category.count }}</span>
        </div>
      </div>

      <!-- 资源列表 -->
      <div class="resources-grid">
        <div class="resource-card education-card" v-for="resource in filteredResources" :key="resource.id">
          <div class="resource-header">
            <div class="resource-icon" :class="resource.type">
              <el-icon><component :is="getResourceIcon(resource.type)" /></el-icon>
            </div>
            <div class="resource-meta">
              <el-tag size="small" :type="getCategoryType(resource.category)">
                {{ getCategoryName(resource.category) }}
              </el-tag>
              <el-tag size="small" type="info">{{ resource.format }}</el-tag>
            </div>
          </div>
          
          <div class="resource-content">
            <h3 class="resource-title">{{ resource.title }}</h3>
            <p class="resource-description">{{ resource.description }}</p>
            <div class="resource-stats">
              <span class="stat-item">
                <el-icon><Download /></el-icon>
                {{ resource.downloads }} 次下载
              </span>
              <span class="stat-item">
                <el-icon><Clock /></el-icon>
                {{ formatFileSize(resource.size) }}
              </span>
            </div>
          </div>
          
          <div class="resource-actions">
            <el-button type="primary" size="small" @click="downloadResource(resource)" class="download-btn">
              <el-icon><Download /></el-icon>
              下载资源
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
// 在script setup的顶部导入API
import { resourceAPI } from '@/utils/api'

// 响应式数据 - 只声明一次
const searchKeyword = ref('')
const selectedCategory = ref('all')
const selectedCourse = ref('all') // 添加课程选择
// 初始化空数组，通过API获取真实数据
const categories = ref([])
const resources = ref([])

// 计算属性
const filteredResources = computed(() => {
  let filtered = resources.value
  
  // 按分类筛选
  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(resource => resource.category === selectedCategory.value)
  }
  
  // 按关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(resource => 
      resource.title.toLowerCase().includes(keyword) ||
      resource.description.toLowerCase().includes(keyword)
    )
  }
  
  return filtered
})

// 在组件加载时获取资源数据
async function fetchResources() {
  try {
    const params = {
      search: searchKeyword.value,
      category_filter: selectedCategory.value !== 'all' ? selectedCategory.value : undefined,
      page: 1,
      page_size: 100 // 获取足够多的资源
    }
    
    // 添加课程筛选
    if (selectedCourse.value && selectedCourse.value !== 'all') {
      // 如果选择的是"全部"课程（all_course），筛选course_id为"all"的资源
      // 如果选择的是"第一课"（lesson1），筛选course_id为"lesson1"的资源
      params.course_id_filter = selectedCourse.value === 'all_course' ? 'all' : selectedCourse.value
    }
    
    const response = await resourceAPI.getResources(params)
    if (response.code === 200) {
      resources.value = response.data.items || []
      // 动态生成分类数据
      generateCategories()
    }
  } catch (error) {
    console.error('获取资源列表错误:', error)
    // 显示错误提示（如果有消息组件）
    if (typeof window !== 'undefined' && window.$message) {
      window.$message.error('获取资源列表失败')
    }
  }
}

// 生成分类数据
function generateCategories() {
  const categoryMap = new Map()
  
  // 统计每个分类的资源数量
  resources.value.forEach(resource => {
    const category = resource.category || 'other'
    const count = categoryMap.get(category) || 0
    categoryMap.set(category, count + 1)
  })
  
  // 构建分类列表
  const categoryList = [
    { id: 'all', name: '全部资源', icon: 'FolderOpened', count: resources.value.length }
  ]
  
  categoryMap.forEach((count, id) => {
    // 根据分类ID设置图标和名称
    const categoryInfo = {
      id,
      name: getCategoryName(id),
      icon: getCategoryIcon(id),
      count
    }
    categoryList.push(categoryInfo)
  })
  
  categories.value = categoryList
}

// 获取分类图标 - 使用后端支持的枚举值
function getCategoryIcon(category) {
  const icons = {
    'courseware': 'Document',
    'reference': 'Reading',
    'assignment': 'EditPen',
    'other': 'Folder'
  }
  return icons[category] || 'Document'
}

// 获取资源图标
function getResourceIcon(type) {
  const icons = {
    video: 'VideoPlay',
    document: 'Document',
    interactive: 'Magic',
    code: 'EditPen'
  }
  return icons[type] || 'Document'
}

// 获取分类类型 - 使用后端支持的枚举值
const getCategoryType = (category) => {
  const types = {
    'courseware': 'primary',
    'reference': 'success',
    'assignment': 'warning',
    'other': 'info'
  }
  return types[category] || 'info'
}

// 获取分类名称 - 将后端枚举值映射到中文名称
const getCategoryName = (category) => {
  const categoryNames = {
    'courseware': '课件',
    'reference': '参考资料',
    'assignment': '作业',
    'other': '其他'
  }
  // 先从映射表中查找，如果找不到再从categories中查找
  if (categoryNames[category]) {
    return categoryNames[category]
  }
  const categoryObj = categories.value.find(c => c.id === category)
  return categoryObj ? categoryObj.name : '未知'
}

// 文件大小格式化函数
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 下载资源函数 - 只保留一个与后端API通信的版本
function downloadResource(resource) {
  try {
    // 使用resource对象中的file_name作为文件名（如果存在）
    // 优先使用file_name，因为它包含完整的文件名和扩展名
    const filename = resource.file_name || resource.title || null;
    // 调用API方法，传递resourceId和文件名
    resourceAPI.downloadResource(resource.id, filename)
    if (typeof window !== 'undefined' && window.$message) {
      window.$message.success(`正在下载: ${resource.title || resource.file_name || '文件'}`)
    }
  } catch (error) {
    console.error('下载资源错误:', error)
    if (typeof window !== 'undefined' && window.$message) {
      window.$message.error('下载失败')
    }
  }
}

// 修改搜索和分类选择方法，重新获取资源
const handleSearch = () => {
  fetchResources()
}

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  fetchResources()
}

// 初始加载资源
fetchResources()
</script>

<style lang="scss" scoped>
.resources-page {
  padding: $spacing-xl;
  height: 100%;
  overflow-y: auto;
}

.resources-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-xl;
  padding-bottom: $spacing-lg;
  border-bottom: 1px solid $border-color;
}

.page-title {
  font-size: 2rem;
  font-weight: bold;
  color: $text-primary;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: $spacing-md;
}

.resources-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-xl;
}

.category-nav {
  display: flex;
  gap: $spacing-md;
  padding: $spacing-lg;
  background: white;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-md;
  border-radius: $border-radius;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: $bg-hover;
  }
  
  &.active {
    background: $education-blue;
    color: white;
  }
}

.nav-icon {
  font-size: 1.2rem;
}

.nav-label {
  font-weight: 500;
}

.nav-count {
  font-size: $font-size-xs;
  opacity: 0.8;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: $spacing-lg;
}

.resource-card {
  padding: $spacing-lg;
}

.resource-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: $spacing-md;
}

.resource-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: white;
  
  &.video {
    background: $education-blue;
  }
  
  &.document {
    background: $education-green;
  }
  
  &.interactive {
    background: $education-purple;
  }
  
  &.code {
    background: $education-orange;
  }
}

.resource-meta {
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
  align-items: flex-end;
}

.resource-content {
  margin-bottom: $spacing-lg;
}

.resource-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-sm 0;
}

.resource-description {
  color: $text-secondary;
  line-height: 1.6;
  margin: 0 0 $spacing-md 0;
}

.resource-stats {
  display: flex;
  gap: $spacing-md;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  font-size: $font-size-sm;
  color: $text-secondary;
}

.resource-actions {
  display: flex;
  justify-content: flex-end;
}

.download-btn {
  width: 120px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .resources-page {
    padding: $spacing-lg;
  }
  
  .resources-header {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .category-nav {
    flex-wrap: wrap;
  }
  
  .resources-grid {
    grid-template-columns: 1fr;
  }
}
</style>