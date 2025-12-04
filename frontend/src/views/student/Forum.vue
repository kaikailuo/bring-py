<template>
  <div class="forum-page">
    <div class="forum-header">
      <h1
        class="page-title"
        role="button"
        tabindex="0"
        style="cursor: pointer;"
        @click="selectCategory('all')"
        @keydown.enter="selectCategory('all')"
      >
        互动交流
      </h1>
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
          <div class="post-item education-card" v-for="post in filteredPosts" :key="post.id" @click="onPostAreaClick(post, $event)">
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
                <el-avatar 
                  :src="post.author?.avatar" 
                  :size="24"
                  style="cursor: pointer;"
                  @click="goToUserProfile(post.author)"
                >
                  <el-icon><User /></el-icon>
                </el-avatar>
                <span 
                  class="author-name"
                  style="cursor: pointer;"
                  @click="goToUserProfile(post.author)"
                >
                  {{ post.author?.name || '未知用户' }}
                </span>
                <el-tag v-if="post.author?.role === 'teacher'" size="small" type="info" style="margin-left:8px">教师</el-tag>
                <span class="post-time">{{ post.time }}</span>
                <el-button size="small" type="primary" @click.stop="aiSummarize(post.id)" style="margin-left:8px">一键AI总结</el-button>
                <!-- 教师管理按钮：仅教师或管理员可见 -->
                <template v-if="userStore.userRole === 'teacher' || userStore.userRole === 'admin'">
                  <el-button size="small" type="danger" @click.stop="deletePost(post)" style="margin-left:8px">删除帖子</el-button>
                  <el-button size="small" type="warning" @click.stop="toggleMuteUser(post.author)" style="margin-left:8px">
                    {{ post.author?.is_muted ? '解禁用户' : '禁言用户' }}
                  </el-button>
                </template>
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
      :title="currentPost?.title || '评论'"
      width="800px"
    >
      <div class="comments-section" v-if="currentPost">
        <!-- 帖子预览：在评论列表上方展示发帖者和全文（保留换行） -->
        <div class="dialog-post-preview">
          <div class="preview-author">
            <el-avatar :src="currentPost.author?.avatar" :size="36" style="cursor: pointer;" @click.stop="goToUserProfile(currentPost.author)">
              <el-icon><User /></el-icon>
            </el-avatar>
            <div class="preview-meta">
              <div class="preview-name">{{ currentPost.author?.name || '未知用户' }} <el-tag v-if="currentPost.author?.role === 'teacher'" size="small" type="info" style="margin-left:6px">教师</el-tag></div>
              <div class="preview-time">{{ currentPost.time }}</div>
            </div>
          </div>
          <div class="dialog-post-content">{{ currentPost.content }}</div>
        </div>
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
              <el-avatar 
                :src="comment.author?.avatar" 
                :size="32"
                style="cursor: pointer;"
                @click="goToUserProfile(comment.author)"
              >
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="comment-author">
                <span 
                  class="author-name"
                  style="cursor: pointer;"
                  @click="goToUserProfile(comment.author)"
                >
                  {{ comment.author?.name || '未知用户' }}
                </span>
                <el-tag v-if="comment.author?.role === 'teacher'" size="small" type="info" style="margin-left:6px">教师</el-tag>
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
              <!-- 删除：教师/管理员/评论作者可见；禁言：仅教师可见 -->
              <template v-if="userStore.userRole === 'teacher' || userStore.userRole === 'admin' || comment.author?.id === userStore.user?.id">
                <el-button size="small" type="danger" @click="deleteComment(comment)" style="margin-left:8px">删除</el-button>
              </template>
              <template v-if="userStore.userRole === 'teacher'">
                <el-button size="small" type="warning" @click="toggleMuteUser(comment.author)" style="margin-left:8px">
                  {{ comment.author?.is_muted ? '解禁' : '禁言' }}
                </el-button>
              </template>
            </div>
            
            <!-- 回复列表 -->
            <div class="replies-list" v-if="comment.replies && comment.replies.length > 0">
              <div class="reply-item" v-for="reply in comment.replies" :key="reply.id">
                <el-avatar 
                  :src="reply.author?.avatar" 
                  :size="24"
                  style="cursor: pointer;"
                  @click="goToUserProfile(reply.author)"
                >
                  <el-icon><User /></el-icon>
                </el-avatar>
                <div class="reply-content">
                  <span 
                    class="reply-author"
                    style="cursor: pointer;"
                    @click="goToUserProfile(reply.author)"
                  >
                    {{ reply.author?.name || '未知用户' }}：
                  </span>
                  <el-tag v-if="reply.author?.role === 'teacher'" size="small" type="info" style="margin-left:6px">教师</el-tag>
                  <span class="reply-text">{{ reply.content }}</span>
                </div>
                <div class="reply-actions">
                  <template v-if="userStore.userRole === 'teacher' || userStore.userRole === 'admin' || reply.author?.id === userStore.user?.id">
                    <el-button size="small" type="danger" @click="deleteComment(reply)" style="margin-left:8px">删除</el-button>
                  </template>
                  <template v-if="userStore.userRole === 'teacher'">
                    <el-button size="small" type="warning" @click="toggleMuteUser(reply.author)" style="margin-left:8px">{{ reply.author?.is_muted ? '解禁' : '禁言' }}</el-button>
                  </template>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import api from '@/utils/api'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

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
    
  },
  {
    id: 'data-structure',
    name: '数据结构',
    description: '数组、链表、栈、队列等数据结构相关问题',
    icon: 'Box',
    postCount: 32,
    replyCount: 156,
  },
  {
    id: 'algorithm',
    name: '算法讨论',
    description: '排序、搜索、动态规划等算法问题',
    icon: 'TrendCharts',
    postCount: 28,
    replyCount: 189,
  }
])

const posts = ref([])

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

const onPostAreaClick = (post, e) => {
  // 如果点击的是已有交互元素（头像、按钮、标签、统计区等）则忽略父容器的打开行为
  const ignored = e.target.closest('.el-avatar, .el-button, .post-author, .post-stats, .post-tags, .el-tag, .author-name, .reply-item, .reply-actions')
  if (ignored) return

  // 否则打开评论弹窗（复用已有方法）
  showComments(post)
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
    await loadPosts()

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
    await loadPosts()
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
  newComment.value = `@${comment.author?.name || '未知用户'} `
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

// 跳转到用户个人主页
const goToUserProfile = (author) => {
  if (!author || !author.id) return
  
  // 如果查看的是自己的主页，跳转到个人主页
  if (author.id === userStore.user?.id) {
    if (userStore.userRole === 'student') {
      router.push('/student/profile')
    } else if (userStore.userRole === 'teacher') {
      router.push('/teacher/profile')
    }
    return
  }
  
  // 查看其他用户的主页，根据当前用户角色跳转
  if (userStore.userRole === 'student') {
    router.push(`/student/user/${author.id}`)
  } else if (userStore.userRole === 'teacher') {
    router.push(`/teacher/user/${author.id}`)
  } else {
    // 如果是其他角色或未登录，跳转到学生端
    router.push(`/student/user/${author.id}`)
  }
}

// 加载帖子列表
const loadPosts = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/posts/")
    if (res.data && res.data.code === 200 && res.data.data) {
      posts.value = res.data.data.map(post => ({
        ...post,
        // 确保字段映射正确
        isFeatured: post.isFeatured !== undefined ? post.isFeatured : post.is_featured,
        isPinned: post.isPinned !== undefined ? post.isPinned : post.is_pinned,
        author: post.author || { name: '未知用户', avatar: null, id: null, role: null }
      }))
    }
  } catch (error) {
    console.error('加载帖子列表失败:', error)
    posts.value = []
  }
}

// 初始化加载帖子
onMounted(async () => {
  await loadPosts()
  // 帖子加载后检查是否需要打开特定帖子的评论（来自教师监控页）
  const postId = route.query.post_id
  if (postId && posts.value.length > 0) {
    const target = posts.value.find(p => String(p.id) === String(postId))
    if (target) {
      // 使用 nextTick 确保 DOM 已更新
      setTimeout(() => {
        showComments(target)
        // 清除 query 参数避免刷新时重复打开
        router.replace({ name: 'StudentForum', query: {} })
      }, 100)
    }
  }
})

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

// AI 总结触发函数（前端仅发起请求，后端返回占位）
const aiSummarize = async (postId) => {
  try {
    await api.http.post('/ai/summarize', { post_id: postId })
    ElMessage.success('AI 总结请求已发送')
  } catch (err) {
    console.error('AI summarize error', err)
    ElMessage.error('AI 总结请求失败')
  }
}

// 教师/管理员：删除帖子
const deletePost = async (post) => {
  if (!post || !post.id) return
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.error('请先登录')
    return
  }

  try {
    await axios.delete(`http://127.0.0.1:8000/api/posts/${post.id}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    ElMessage.success('帖子已删除')
    // 从本地列表移除
    posts.value = posts.value.filter(p => p.id !== post.id)
  } catch (err) {
    console.error('删除帖子失败', err)
    ElMessage.error(err?.response?.data?.message || '删除帖子失败')
  }
}

// 教师/管理员：禁言/解禁用户
const toggleMuteUser = async (author) => {
  if (!author || !author.id) return
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.error('请先登录')
    return
  }

  try {
    const mute = !author.is_muted
    const res = await axios.put(`http://127.0.0.1:8000/api/auth/users/${author.id}/mute?mute=${mute}`, {}, {
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (res.data && res.data.code === 200) {
      ElMessage.success(res.data.message || '操作成功')
      // 更新本地作者状态（界面体现）
      posts.value = posts.value.map(p => {
        if (p.author && p.author.id === author.id) {
          p.author.is_muted = mute
        }
        return p
      })
      // 如果评论已经加载，也更新评论显示
      comments.value = comments.value.map(c => {
        if (c.author && c.author.id === author.id) c.author.is_muted = mute
        if (c.replies) c.replies = c.replies.map(r => { if (r.author && r.author.id === author.id) r.author.is_muted = mute; return r })
        return c
      })
    } else {
      ElMessage.error(res.data?.message || '操作失败')
    }
  } catch (err) {
    console.error('禁言操作失败', err)
    ElMessage.error('禁言操作失败')
  }
}

// 删除评论或回复（作者或教师/管理员可用）
const deleteComment = async (comment) => {
  if (!comment || !comment.id) return
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.error('请先登录')
    return
  }

  try {
    await axios.delete(`http://127.0.0.1:8000/api/comments/${comment.id}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })

    ElMessage.success('评论已删除')

    // 如果是顶级评论，则从 comments 列表移除
    if (!comment.parent_id) {
      comments.value = comments.value.filter(c => c.id !== comment.id)
    } else {
      // 否则在对应父评论的 replies 中移除
      comments.value = comments.value.map(c => {
        if (c.replies && c.replies.length) {
          c.replies = c.replies.filter(r => r.id !== comment.id)
        }
        return c
      })
    }

    // 刷新帖子列表中的回复计数
    await loadPosts()
  } catch (err) {
    console.error('删除评论失败', err)
    ElMessage.error(err?.response?.data?.message || '删除评论失败')
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

/* 弹窗中帖子预览样式（保留换行） */
.dialog-post-preview {
  padding: $spacing-lg;
  background: #f5f5f5;
  border-radius: $border-radius;
  margin-bottom: $spacing-lg;
  box-shadow: $box-shadow;
}
.dialog-post-preview .preview-author {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  margin-bottom: $spacing-md;
}
.dialog-post-preview .preview-meta {
  display: flex;
  flex-direction: column;
}
.dialog-post-content {
  white-space: pre-wrap; /* 保留换行 */
  color: $text-secondary;
  line-height: 1.6;
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
