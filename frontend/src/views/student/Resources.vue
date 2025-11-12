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
                <el-icon><View /></el-icon>
                {{ resource.views }}
              </span>
              <span class="stat-item">
                <el-icon><Download /></el-icon>
                {{ resource.downloads }}
              </span>
              <span class="stat-item">
                <el-icon><Star /></el-icon>
                {{ resource.rating }}
              </span>
            </div>
          </div>
          
          <div class="resource-actions">
            <el-button type="primary" size="small" @click="viewResource(resource)">
              <el-icon><View /></el-icon>
              查看
            </el-button>
            <el-button size="small" @click="downloadResource(resource)">
              <el-icon><Download /></el-icon>
              下载
            </el-button>
            <el-button size="small" @click="addToFavorites(resource)">
              <el-icon><Star /></el-icon>
              收藏
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 响应式数据
const searchKeyword = ref('')
const selectedCategory = ref('all')

// 模拟数据
const categories = ref([
  { id: 'all', name: '全部资源', icon: 'FolderOpened', count: 156 },
  { id: 'python-basic', name: 'Python基础', icon: 'Document', count: 45 },
  { id: 'data-structure', name: '数据结构', icon: 'Box', count: 38 },
  { id: 'algorithm', name: '算法', icon: 'TrendCharts', count: 42 },
  { id: 'oop', name: '面向对象', icon: 'Grid', count: 31 }
])

const resources = ref([
  {
    id: 1,
    title: 'Python基础语法教程',
    description: '详细介绍Python的基本语法、数据类型、控制结构等基础知识',
    type: 'video',
    format: 'MP4',
    category: 'python-basic',
    views: 1250,
    downloads: 456,
    rating: 4.8
  },
  {
    id: 2,
    title: '数据结构与算法课件',
    description: '包含数组、链表、栈、队列、树等数据结构的详细讲解',
    type: 'document',
    format: 'PDF',
    category: 'data-structure',
    views: 980,
    downloads: 234,
    rating: 4.6
  },
  {
    id: 3,
    title: '排序算法演示',
    description: '可视化演示各种排序算法的执行过程',
    type: 'interactive',
    format: 'HTML',
    category: 'algorithm',
    views: 756,
    downloads: 123,
    rating: 4.9
  }
])

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

// 方法
const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
}

const handleSearch = () => {
  // 搜索逻辑已在计算属性中处理
}

const getResourceIcon = (type) => {
  const icons = {
    video: 'VideoPlay',
    document: 'Document',
    interactive: 'StarFilled',
    code: 'EditPen'
  }
  return icons[type] || 'Document'
}

const getCategoryType = (category) => {
  const types = {
    'python-basic': 'primary',
    'data-structure': 'success',
    'algorithm': 'warning',
    'oop': 'danger'
  }
  return types[category] || 'info'
}

const getCategoryName = (category) => {
  const categoryObj = categories.value.find(c => c.id === category)
  return categoryObj ? categoryObj.name : '未知'
}

const viewResource = (resource) => {
  console.log('查看资源:', resource.title)
}

const downloadResource = (resource) => {
  console.log('下载资源:', resource.title)
}

const addToFavorites = (resource) => {
  console.log('收藏资源:', resource.title)
}
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
  gap: $spacing-sm;
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
