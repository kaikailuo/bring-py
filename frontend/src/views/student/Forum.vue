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
                <span class="stat-item" @click="showComments(post)" style="cursor: pointer;">
                  <el-icon><ChatDotRound /></el-icon>
                  {{ post.replies }}
                </span>
                <span class="stat-item" @click="toggleFavorite(post)" :class="{ 'favorited': post.isFavorited }" style="cursor: pointer;">
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
          <el-button @click="showNewPostDialog = false" :disabled="submitting">取消</el-button>
          <el-button type="primary" @click="submitNewPost" :loading="submitting">发布</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 评论对话框 -->
    <el-dialog
      v-model="showCommentDialog"
      :title="`评论 - ${currentPost?.title || ''}`"
      width="800px"
    >
      <div class="comments-section" v-if="currentPost">
        <!-- 评论输入框 -->
        <div class="comment-input-area">
          <el-input
            v-model="newComment"
            type="textarea"
            :rows="3"
            placeholder="写下你的评论..."
          />
          <div class="comment-actions">
            <el-button type="primary" @click="submitComment" :loading="submittingComment">
              发表评论
            </el-button>
          </div>
        </div>

        <!-- 评论列表 -->
        <div class="comments-list">
          <div class="comment-item" v-for="comment in comments" :key="comment.id">
            <div class="comment-header">
              <el-avatar :size="32">
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="comment-author">
                <span class="author-name">{{ comment.author.name }}</span>
                <span class="comment-time">{{ comment.time }}</span>
              </div>
            </div>
            <div class="comment-content">{{ comment.content }}</div>
            <div class="comment-footer">
              <span class="comment-action" @click="replyToComment(comment)" style="cursor: pointer;">
                <el-icon><ChatDotRound /></el-icon>
                回复
              </span>
              <span class="comment-action" @click="likeComment(comment)" style="cursor: pointer;">
                <el-icon><Star /></el-icon>
                {{ comment.likes }}
              </span>
            </div>
            
            <!-- 回复列表 -->
            <div class="replies-list" v-if="comment.replies && comment.replies.length > 0">
              <div class="reply-item" v-for="reply in comment.replies" :key="reply.id">
                <el-avatar :size="24">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <div class="reply-content">
                  <span class="reply-author">{{ reply.author.name }}：</span>
                  <span class="reply-text">{{ reply.content }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="comments.length === 0" class="no-comments">
            暂无评论，快来抢沙发吧！
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

// 响应式数据
const selectedCategory = ref('all')
const sortBy = ref('latest')
const showNewPostDialog = ref(false)
const newPostFormRef = ref()
const submitting = ref(false)

// 评论相关
const showCommentDialog = ref(false)
const currentPost = ref(null)
const comments = ref([])
const newComment = ref('')
const submittingComment = ref(false)
const replyingTo = ref(null)

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
  
  // 如果正在提交，防止重复点击
  if (submitting.value) return
  
  try {
    // 验证表单
    await newPostFormRef.value.validate()
    
    submitting.value = true

    // 获取token
    const token = localStorage.getItem('token')
    if (!token) {
      ElMessage.error('请先登录')
      return
    }

    // 发送请求到后端
    const res = await axios.post("http://127.0.0.1:8000/api/posts/", {
      title: newPost.value.title,
      content: newPost.value.content,
      category: newPost.value.category,
      tags: newPost.value.tags ? newPost.value.tags.split(',').map(t => t.trim()).filter(t => t) : []
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    // 成功提示
    ElMessage.success("✅ 发布成功！")

    // 关闭弹窗
    showNewPostDialog.value = false

    // 重置表单
    handleNewPostClose()

    // 重新加载帖子列表
    const postsRes = await axios.get("http://127.0.0.1:8000/api/posts/")
    if (postsRes.data && postsRes.data.data) {
      posts.value = postsRes.data.data
    }

  } catch (error) {
    // 表单验证失败
    if (error && typeof error === 'object' && !error.message) {
      ElMessage.warning('请完善表单信息')
    } else {
      console.error('发布失败:', error)
      
      // 详细错误信息
      let errorMessage = '发布失败，请稍后重试'
      
      if (error.response) {
        // 服务器返回了错误响应
        const status = error.response.status
        const detail = error.response.data?.detail || error.response.data?.message
        
        if (status === 401 || detail?.includes('credentials') || detail?.includes('validate')) {
          // 认证失败，清除token并提示重新登录
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          errorMessage = '登录已过期，请重新登录'
          ElMessage.error(errorMessage)
          // 延迟跳转到登录页
          setTimeout(() => {
            window.location.href = '/login'
          }, 1500)
          return
        }
        
        errorMessage = detail || `服务器错误: ${status}`
        console.error('服务器响应:', error.response.data)
      } else if (error.request) {
        // 请求已发出但没有收到响应
        errorMessage = '无法连接到服务器，请检查后端服务是否运行（http://127.0.0.1:8000）'
        console.error('请求错误:', error.request)
      } else {
        // 其他错误
        errorMessage = error.message || errorMessage
        console.error('错误信息:', error.message)
      }
      
      ElMessage.error(errorMessage)
    }
  } finally {
    submitting.value = false
  }
}

// 显示评论对话框
const showComments = async (post) => {
  currentPost.value = post
  showCommentDialog.value = true
  newComment.value = ''
  replyingTo.value = null
  
  // 加载评论列表
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`http://127.0.0.1:8000/api/posts/${post.id}/comments/`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
    if (res.data && res.data.data) {
      comments.value = res.data.data
    }
  } catch (error) {
    console.error('加载评论失败:', error)
    comments.value = []
  }
}

// 提交评论
const submitComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  
  if (!currentPost.value) return
  
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.error('请先登录')
    return
  }
  
  try {
    submittingComment.value = true
    
    await axios.post(
      `http://127.0.0.1:8000/api/posts/${currentPost.value.id}/comments/`,
      {
        content: newComment.value,
        parent_id: replyingTo.value?.id || null
      },
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    )
    
    ElMessage.success('评论发表成功！')
    newComment.value = ''
    replyingTo.value = null
    
    // 重新加载评论列表
    await showComments(currentPost.value)
    
    // 刷新帖子列表
    const postsRes = await axios.get("http://127.0.0.1:8000/api/posts/")
    if (postsRes.data && postsRes.data.data) {
      posts.value = postsRes.data.data
    }
  } catch (error) {
    console.error('发表评论失败:', error)
    ElMessage.error(error?.response?.data?.detail || '发表评论失败')
  } finally {
    submittingComment.value = false
  }
}

// 回复评论
const replyToComment = (comment) => {
  replyingTo.value = comment
  newComment.value = `@${comment.author.name} `
}

// 点赞评论
const likeComment = async (comment) => {
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.error('请先登录')
    return
  }
  
  try {
    const res = await axios.put(
      `http://127.0.0.1:8000/api/comments/${comment.id}/like`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    )
    if (res.data && res.data.data) {
      comment.likes = res.data.data.likes
      ElMessage.success('点赞成功')
    }
  } catch (error) {
    console.error('点赞失败:', error)
    ElMessage.error('点赞失败')
  }
}

// 收藏/取消收藏
const toggleFavorite = async (post) => {
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.error('请先登录')
    return
  }
  
  try {
    const res = await axios.post(
      `http://127.0.0.1:8000/api/posts/${post.id}/favorite`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    )
    
    if (res.data && res.data.data) {
      post.isFavorited = res.data.data.is_favorited
      ElMessage.success(res.data.message)
      
      // 更新点赞数（这里用收藏数替代，实际应该分开）
      if (post.isFavorited) {
        post.likes = (post.likes || 0) + 1
      } else {
        post.likes = Math.max(0, (post.likes || 0) - 1)
      }
    }
  } catch (error) {
    console.error('收藏操作失败:', error)
    ElMessage.error(error?.response?.data?.detail || '操作失败')
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
  line-clamp: 3; 
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

/* 评论相关样式 */
.comments-section {
  max-height: 600px;
  overflow-y: auto;
}

.comment-input-area {
  margin-bottom: $spacing-xl;
  padding-bottom: $spacing-lg;
  border-bottom: 1px solid $border-color;
}

.comment-actions {
  margin-top: $spacing-md;
  text-align: right;
}

.comments-list {
  padding-top: $spacing-lg;
}

.comment-item {
  padding: $spacing-lg;
  margin-bottom: $spacing-lg;
  background: #f5f5f5;
  border-radius: $border-radius;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  margin-bottom: $spacing-sm;
}

.comment-author {
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
}

.author-name {
  font-weight: 500;
  color: $text-primary;
}

.comment-time {
  font-size: $font-size-xs;
  color: $text-light;
}

.comment-content {
  margin: $spacing-sm 0;
  color: $text-secondary;
  line-height: 1.6;
}

.comment-footer {
  display: flex;
  gap: $spacing-md;
  margin-top: $spacing-sm;
}

.comment-action {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  color: $text-secondary;
  font-size: $font-size-sm;
  transition: color 0.3s;
  
  &:hover {
    color: $primary-color;
  }
}

.replies-list {
  margin-top: $spacing-md;
  margin-left: $spacing-xl;
  padding-left: $spacing-lg;
  border-left: 2px solid $border-color;
}

.reply-item {
  display: flex;
  align-items: flex-start;
  gap: $spacing-sm;
  margin-bottom: $spacing-sm;
  padding: $spacing-sm;
  background: white;
  border-radius: $border-radius;
}

.reply-content {
  flex: 1;
  font-size: $font-size-sm;
}

.reply-author {
  font-weight: 500;
  color: $text-primary;
}

.reply-text {
  color: $text-secondary;
}

.no-comments {
  text-align: center;
  padding: $spacing-xxl;
  color: $text-light;
}

.stat-item.favorited {
  color: #ffd700;
  
  .el-icon {
    color: #ffd700;
  }
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
