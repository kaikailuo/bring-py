<template>
	<div class="question-monitor-page">
		<div class="header">
			<h2>问题监控</h2>
			<p class="subtitle">教师可在此处管理讨论区帖子与用户（删除帖子 / 禁言用户）。</p>
		</div>

		<div class="list">
			<el-table :data="posts" style="width: 100%">
				<el-table-column prop="id" label="#" width="60" />
				<el-table-column label="标题">
					<template #default="{ row }">
						<div>
							<div class="title">{{ row.title }}</div>
							<div class="meta">作者：<span @click="goToUserProfile(row.author)" class="link">{{ row.author?.name || '未知' }}</span>
								<el-tag v-if="row.author?.role === 'teacher'" size="small" type="info" style="margin-left:8px">教师</el-tag>
							</div>
						</div>
					</template>
				</el-table-column>
				<el-table-column prop="time" label="时间" width="160" />
				<el-table-column prop="views" label="浏览" width="100" />
				<el-table-column prop="replies" label="回复" width="100" />
				<el-table-column label="操作" width="320">
					<template #default="{ row }">
						<el-button size="small" type="primary" @click="viewComments(row)" style="margin-left:4px">查看</el-button>
						<el-button size="small" type="danger" @click="deletePost(row)" style="margin-left:4px">删除</el-button>
						<el-button size="small" type="warning" @click="toggleMuteUser(row.author)" style="margin-left:4px">
							{{ row.author?.is_muted ? '解禁' : '禁言' }}
						</el-button>
					</template>
				</el-table-column>
			</el-table>

			<div v-if="posts.length === 0" class="empty">暂无帖子</div>
		</div>

		<!-- 评论对话框 -->
		<el-dialog
			v-model="showCommentDialog"
			:title="`评论：${currentPost?.title || ''}`"
			width="70%"
			@close="() => { currentPost = null; comments = []; newComment = '' }"
		>
			<div v-if="currentPost" class="comment-dialog">
				<!-- 帖子预览 -->
				<div class="post-preview">
					<div class="post-content">{{ currentPost.content }}</div>
					<div class="post-meta" style="margin-top: 8px; color: #999; font-size: 12px">
						作者：{{ currentPost.author?.name || '未知' }} | 发布于：{{ currentPost.time }}
					</div>
				</div>

				<el-divider />

				<!-- 现有评论列表 -->
				<div class="comments-section">
					<div class="section-title">评论列表（共 {{ comments.length }} 条）</div>
					<div v-if="comments.length === 0" style="padding: 16px; text-align: center; color: #999">
						暂无评论
					</div>
					<div v-for="comment in comments" :key="comment.id" class="comment-item">
						<div class="comment-header">
							<span class="author-name">{{ comment.author?.name || '未知' }}</span>
							<span class="comment-time" style="color: #999; font-size: 12px">{{ comment.time }}</span>
							<el-button
								v-if="comment.author?.id === userStore.user?.id || userStore.user?.role === 'teacher' || userStore.user?.role === 'admin'"
								link
								type="danger"
								size="small"
								@click="deleteComment(comment)"
								style="margin-left: auto"
							>
								删除
							</el-button>
						</div>
						<div class="comment-content">{{ comment.content }}</div>
					</div>
				</div>

				<el-divider />

				<!-- 发表评论输入框 -->
				<div class="comment-input-section">
					<div class="section-title">发表评论</div>
					<el-input
						v-model="newComment"
						type="textarea"
						:rows="4"
						placeholder="输入你的评论..."
						style="margin-bottom: 8px"
					/>
					<div style="display: flex; justify-content: flex-end; gap: 8px">
						<el-button @click="showCommentDialog = false">取消</el-button>
						<el-button
							type="primary"
							:loading="submittingComment"
							@click="submitComment"
						>
							提交评论
						</el-button>
					</div>
				</div>
			</div>
		</el-dialog>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { User } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const posts = ref([])
const showCommentDialog = ref(false)
const currentPost = ref(null)
const comments = ref([])
const newComment = ref('')
const submittingComment = ref(false)

const loadPosts = async () => {
	try {
		const res = await axios.get('http://127.0.0.1:8000/api/posts/')
		if (res.data && res.data.code === 200 && res.data.data) {
			posts.value = res.data.data
		} else {
			posts.value = []
		}
	} catch (err) {
		console.error('加载帖子失败', err)
		posts.value = []
	}
}
	// end loadPosts

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
		posts.value = posts.value.filter(p => p.id !== post.id)
	} catch (err) {
		console.error('删除帖子失败', err)
		ElMessage.error(err?.response?.data?.message || '删除帖子失败')
	}
}

// on mount, load posts and check query param to open a specific post's comments
onMounted(async () => {
	await loadPosts()
	const postId = route.query.post_id
	if (postId && posts.value.length > 0) {
		const target = posts.value.find(p => String(p.id) === String(postId))
		if (target) {
			setTimeout(() => {
				viewComments(target)
				router.replace({ name: 'QuestionMonitor', query: {} })
			}, 100)
		}
	}
})

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
			// 更新本地状态
			posts.value = posts.value.map(p => {
				if (p.author && p.author.id === author.id) p.author.is_muted = mute
				return p
			})
		} else {
			ElMessage.error(res.data?.message || '操作失败')
		}
	} catch (err) {
		console.error('禁言操作失败', err)
		ElMessage.error('禁言操作失败')
	}
}

const viewComments = async (post) => {
	currentPost.value = post
	showCommentDialog.value = true
	newComment.value = ''
	
	// 加载评论列表并更新浏览次数
	try {
		const token = localStorage.getItem('token')
		
		// 先获取帖子详情（这会增加浏览次数）
		const postRes = await axios.get(
			`http://127.0.0.1:8000/api/posts/${post.id}`,
			{
				headers: token ? { 'Authorization': `Bearer ${token}` } : {}
			}
		)
		if (postRes.data && postRes.data.data) {
			currentPost.value = postRes.data.data
		}
		
		// 再加载评论列表
		const res = await axios.get(
			`http://127.0.0.1:8000/api/posts/${post.id}/comments/`,
			{
				headers: token ? { 'Authorization': `Bearer ${token}` } : {}
			}
		)
		if (res.data && res.data.data) {
			comments.value = res.data.data
		} else {
			comments.value = []
		}
	} catch (error) {
		console.error('加载评论失败:', error)
		const status = error?.response?.status || error?.response?.data?.status
		if (status === 401) {
			ElMessage.error('未登录或登录已过期，请先登录')
			localStorage.removeItem('token')
			userStore.logout && userStore.logout()
			router.push('/login')
			return
		}
		comments.value = []
	}
}

const submitComment = async () => {
    if (!newComment.value || !newComment.value.trim()) {
        ElMessage.error('请输入评论内容')
        return
    }

    const token = localStorage.getItem('token')
    if (!token) {
        ElMessage.error('请先登录')
        router.push('/login')
        return
    }

    try {
        submittingComment.value = true

        await axios.post(
            `http://127.0.0.1:8000/api/posts/${currentPost.value.id}/comments/`,
            {
                content: newComment.value,
                parent_id: null
            },
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        )

        ElMessage.success('评论发表成功！')
        newComment.value = ''

        // 重新加载评论列表
        await viewComments(currentPost.value)
    } catch (error) {
        console.error('发表评论失败:', error)
        const status = error?.response?.status || error?.response?.data?.status
        if (status === 401) {
            ElMessage.error('未登录或登录已过期，请重新登录')
            localStorage.removeItem('token')
            userStore.logout && userStore.logout()
            router.push('/login')
            return
        }
        ElMessage.error(error?.response?.data?.detail || error?.response?.data?.message || '发表评论失败')
    } finally {
        submittingComment.value = false
    }
}

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
		// 从本地列表移除
		comments.value = comments.value.filter(c => c.id !== comment.id)
	} catch (err) {
		console.error('删除评论失败', err)
		ElMessage.error(err?.response?.data?.message || '删除评论失败')
	}
}

const goToUserProfile = (author) => {
	if (!author || !author.id) return
	router.push({ name: 'TeacherUserProfile', params: { userId: author.id } })
}

onMounted(() => {
	loadPosts()
})
</script>

<style scoped>
.question-monitor-page { padding: 16px }
.header { margin-bottom: 12px }
.subtitle { color: #666; margin-top: 4px }
.empty { padding: 32px; text-align: center; color: #999 }
.link { color: var(--el-color-primary); cursor: pointer }

/* 评论对话框样式 */
.comment-dialog {
	max-height: 600px;
	overflow-y: auto;
}

.post-preview {
	padding: 12px;
	background: #f5f5f5;
	border-radius: 4px;
	border-left: 3px solid var(--el-color-primary);
}

.post-content {
	font-size: 14px;
	line-height: 1.6;
	color: #333;
	word-break: break-word;
	white-space: pre-wrap;
}

.post-meta {
	margin-top: 8px;
	font-size: 12px;
	color: #999;
}

.section-title {
	font-weight: 600;
	font-size: 14px;
	margin-bottom: 8px;
	color: #333;
}

.comments-section {
	margin-bottom: 16px;
}

.comment-item {
	padding: 12px;
	border: 1px solid #eee;
	border-radius: 4px;
	margin-bottom: 8px;
	background: #fafafa;
}

.comment-header {
	display: flex;
	align-items: center;
	margin-bottom: 8px;
	gap: 8px;
}

.author-name {
	font-weight: 600;
	color: #333;
	font-size: 13px;
}

.comment-time {
	font-size: 12px;
	color: #999;
}

.comment-content {
	font-size: 13px;
	line-height: 1.5;
	color: #666;
	white-space: pre-wrap;
	word-break: break-word;
}

.comment-input-section {
	padding-top: 8px;
}
</style>
