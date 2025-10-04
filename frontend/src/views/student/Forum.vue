<template>
  <div class="forum-page">
    <div class="forum-header">
      <h1 class="page-title">互动交流</h1>
      <el-button type="primary" @click="showNewPostDialog = true">
        <el-icon><Edit /></el-icon>
        发布新帖
      </el-button>
    </div>

    <div class="forum-content">
      <!-- 论坛分类 -->
      <div class="forum-categories">
        <div class="category-card education-card" 
             v-for="category in categories" 
             :key="category.id"
             @click="selectCategory(category.id)">
          <div class="category-icon">
            <el-icon><component :is="category.icon" /></el-icon>
          </div>
          <div class="category-info">
            <h3 class="category-title">{{ category.name }}</h3>
            <p class="category-desc">{{ category.description }}</p>
            <div class="category-stats">
              <span>{{ category.postCount }} 帖子</span>
              <span>{{ category.replyCount }} 回复</span>
            </div>
          </div>
          <div class="category-latest">
            <div class="latest-post" v-if="category.latestPost">
              <div class="latest-title">{{ category.latestPost.title }}</div>
              <div class="latest-meta">
                {{ category.latestPost.author }} · {{ category.latestPost.time }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 帖子列表 -->
      <div class="posts-section">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><ChatDotRound /></el-icon>
            {{ selectedCategoryName }}讨论区
          </h2>
          <div class="filter-options">
            <el-select v-model="sortBy" placeholder="排序方式" style="width: 120px">
              <el-option label="最新" value="latest" />
              <el-option label="最热" value="hot" />
              <el-option label="精华" value="featured" />
            </el-select>
          </div>
        </div>
        
        <div class="posts-list">
          <div class="post-item education-card" v-for="post in filteredPosts" :key="post.id">
            <div class="post-header">
              <div class="post-title">
                <h3>{{ post.title }}</h3>
                <div class="post-tags">
                  <el-tag size="small" v-for="tag in post.tags" :key="tag">
                    {{ tag }}
                  </el-tag>
                </div>
              </div>
              <div class="post-meta">
                <el-tag v-if="post.isFeatured" type="warning">精华</el-tag>
                <el-tag v-if="post.isPinned" type="danger">置顶</el-tag>
              </div>
            </div>
            
            <div class="post-content">
              <p>{{ post.content }}</p>
            </div>
            
            <div class="post-footer">
              <div class="post-author">
                <el-avatar :src="post.author.avatar" :size="24">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <span class="author-name">{{ post.author.name }}</span>
                <span class="post-time">{{ post.time }}</span>
              </div>
              
              <div class="post-stats">
                <span class="stat-item">
                  <el-icon><View /></el-icon>
                  {{ post.views }}
                </span>
                <span class="stat-item">
                  <el-icon><ChatDotRound /></el-icon>
                  {{ post.replies }}
                </span>
                <span class="stat-item">
                  <el-icon><Star /></el-icon>
                  {{ post.likes }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 发布新帖对话框 -->
    <el-dialog
      v-model="showNewPostDialog"
      title="发布新帖"
      width="600px"
      :before-close="handleNewPostClose"
    >
      <el-form ref="newPostFormRef" :model="newPost" :rules="postRules" label-width="80px">
        <el-form-item label="分类" prop="category">
          <el-select v-model="newPost.category" placeholder="选择分类">
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="newPost.title" placeholder="请输入帖子标题" />
        </el-form-item>
        <el-form-item label="标签" prop="tags">
          <el-input v-model="newPost.tags" placeholder="请输入标签，用逗号分隔" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="newPost.content"
            type="textarea"
            :rows="6"
            placeholder="请输入帖子内容..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showNewPostDialog = false">取消</el-button>
          <el-button type="primary" @click="submitNewPost">发布</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 响应式数据
const selectedCategory = ref('all')
const sortBy = ref('latest')
const showNewPostDialog = ref(false)
const newPostFormRef = ref()

const newPost = ref({
  category: '',
  title: '',
  tags: '',
  content: ''
})

const postRules = {
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

// 模拟数据
const categories = ref([
  {
    id: 'python-basic',
    name: 'Python基础',
    description: 'Python语法、数据类型、控制结构等基础问题讨论',
    icon: 'Document',
    postCount: 45,
    replyCount: 234,
    latestPost: {
      title: 'Python列表和元组的区别？',
      author: '张同学',
      time: '2小时前'
    }
  },
  {
    id: 'data-structure',
    name: '数据结构',
    description: '数组、链表、栈、队列等数据结构相关问题',
    icon: 'Box',
    postCount: 32,
    replyCount: 156,
    latestPost: {
      title: '如何实现一个简单的栈？',
      author: '李同学',
      time: '5小时前'
    }
  },
  {
    id: 'algorithm',
    name: '算法讨论',
    description: '排序、搜索、动态规划等算法问题',
    icon: 'TrendCharts',
    postCount: 28,
    replyCount: 189,
    latestPost: {
      title: '快速排序的实现原理',
      author: '王同学',
      time: '1天前'
    }
  }
])

const posts = ref([
  {
    id: 1,
    title: 'Python中如何优雅地处理异常？',
    content: '在学习Python的过程中，经常遇到各种异常情况，想了解一下有哪些优雅的处理方式...',
    category: 'python-basic',
    tags: ['Python', '异常处理', '最佳实践'],
    author: {
      name: '张同学',
      avatar: ''
    },
    time: '2小时前',
    views: 156,
    replies: 8,
    likes: 12,
    isFeatured: false,
    isPinned: false
  },
  {
    id: 2,
    title: '数据结构学习心得分享',
    content: '经过一段时间的学习，总结了一些数据结构的学习心得，希望对大家有帮助...',
    category: 'data-structure',
    tags: ['数据结构', '学习心得', '分享'],
    author: {
      name: '李同学',
      avatar: ''
    },
    time: '5小时前',
    views: 234,
    replies: 15,
    likes: 28,
    isFeatured: true,
    isPinned: false
  }
])

// 计算属性
const selectedCategoryName = computed(() => {
  const category = categories.value.find(c => c.id === selectedCategory.value)
  return category ? category.name : '全部'
})

const filteredPosts = computed(() => {
  let filtered = posts.value
  
  // 按分类筛选
  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(post => post.category === selectedCategory.value)
  }
  
  // 排序
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'hot':
        return (b.views + b.replies + b.likes) - (a.views + a.replies + a.likes)
      case 'featured':
        return b.isFeatured - a.isFeatured
      default:
        return new Date(b.time) - new Date(a.time)
    }
  })
  
  return filtered
})

// 方法
const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
}

const handleNewPostClose = () => {
  showNewPostDialog.value = false
  // 重置表单
  Object.assign(newPost.value, {
    category: '',
    title: '',
    tags: '',
    content: ''
  })
  newPostFormRef.value?.resetFields()
}

const submitNewPost = async () => {
  if (!newPostFormRef.value) return
  
  try {
    await newPostFormRef.value.validate()
    
    // 模拟发布
    console.log('发布新帖:', newPost.value)
    
    showNewPostDialog.value = false
    handleNewPostClose()
    
  } catch (error) {
    console.error('发布失败:', error)
  }
}
</script>

<style lang="scss" scoped>
.forum-page {
  padding: $spacing-xl;
  height: 100%;
  overflow-y: auto;
}

.forum-header {
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

.forum-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-xxl;
}

.forum-categories {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: $spacing-lg;
}

.category-card {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  padding: $spacing-xl;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: $box-shadow-hover;
  }
}

.category-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: $gradient-primary;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.category-info {
  flex: 1;
}

.category-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-xs 0;
}

.category-desc {
  color: $text-secondary;
  font-size: $font-size-sm;
  margin: 0 0 $spacing-sm 0;
  line-height: 1.5;
}

.category-stats {
  display: flex;
  gap: $spacing-md;
  font-size: $font-size-xs;
  color: $text-light;
}

.category-latest {
  flex-shrink: 0;
  text-align: right;
}

.latest-post {
  font-size: $font-size-sm;
}

.latest-title {
  color: $text-primary;
  margin-bottom: $spacing-xs;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.latest-meta {
  color: $text-secondary;
  font-size: $font-size-xs;
}

.posts-section {
  background: white;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-lg;
  border-bottom: 1px solid $border-color;
}

.section-title {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: $font-size-xl;
  font-weight: bold;
  color: $text-primary;
  margin: 0;
}

.filter-options {
  display: flex;
  gap: $spacing-md;
}

.posts-list {
  padding: $spacing-lg;
}

.post-item {
  padding: $spacing-lg;
  margin-bottom: $spacing-lg;
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: $box-shadow-hover;
  }
  
  &:last-child {
    margin-bottom: 0;
  }
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: $spacing-md;
}

.post-title h3 {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-primary;
  margin: 0 0 $spacing-sm 0;
}

.post-tags {
  display: flex;
  gap: $spacing-xs;
  flex-wrap: wrap;
}

.post-meta {
  display: flex;
  gap: $spacing-xs;
  flex-shrink: 0;
}

.post-content {
  margin-bottom: $spacing-md;
}

.post-content p {
  color: $text-secondary;
  line-height: 1.6;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-author {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.author-name {
  font-weight: 500;
  color: $text-primary;
}

.post-time {
  color: $text-light;
  font-size: $font-size-xs;
}

.post-stats {
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

/* 响应式设计 */
@media (max-width: 768px) {
  .forum-page {
    padding: $spacing-lg;
  }
  
  .forum-header {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
  
  .forum-categories {
    grid-template-columns: 1fr;
  }
  
  .category-card {
    flex-direction: column;
    text-align: center;
  }
  
  .category-latest {
    text-align: center;
  }
  
  .post-header {
    flex-direction: column;
    gap: $spacing-sm;
  }
  
  .post-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
}
</style>
