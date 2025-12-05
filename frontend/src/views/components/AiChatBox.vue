<template>
  <el-dialog :model-value="visible" :title="title" width="720px" @close="handleClose">
    <div class="ai-chatbox">
      <div class="messages" ref="msgs">
        <div v-for="(m, idx) in messages" :key="idx" :class="['message', m.role]">
          <div class="message-content">{{ m.text }}</div>
        </div>
      </div>

      <div class="chat-input">
        <el-input
          v-model="input"
          type="textarea"
          :rows="3"
          placeholder="输入内容..."
        />
        <div class="chat-actions">
          <el-button @click="onSend" type="primary" :loading="loading">发送</el-button>
          <el-button @click="handleClose">关闭</el-button>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, watch, onMounted, toRefs } from 'vue'
import { ElMessage } from 'element-plus'
import api, { aiAPI } from '@/utils/api'

// 接收 props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  mode: { type: String, default: 'assistant' },
  post: { type: Object, default: null }
})

// 从 props 中解构成可响应的 ref
const { modelValue, mode, post } = toRefs(props)

// emits
const emit = defineEmits(['update:modelValue'])

const visible = ref(false)
const title = ref('AI 聊天')
const messages = ref([])
const input = ref('')
const loading = ref(false)
const msgs = ref(null)

// --- v-model 同步 ---
watch(modelValue, (v) => {
  visible.value = v
})

watch(visible, (v) => {
  emit('update:modelValue', v)
})

// 当 visible 打开时触发 onOpen()
watch(visible, (v) => {
  if (v) onOpen()
})

function handleClose() {
  visible.value = false
}

// -------------------------------------------------------------
// 打开窗口时根据模式执行不同初始化逻辑
// -------------------------------------------------------------
async function onOpen() {
  messages.value = []
  input.value = ''

  if (mode.value === 'assistant') {
    title.value = 'AI 编程助手'
    messages.value.push({ role: 'ai', text: '你好！我是你的 AI 编程助手。' })
  } else if (mode.value === 'summarize') {
    title.value = post.value?.title
      ? `AI 总结 - ${post.value.title}`
      : 'AI 总结'

    if (post.value && post.value.id) {
      loading.value = true
      try {
        const res = await aiAPI.summarize(post.value.id)
        if (res?.summary) {
          messages.value.push({ role: 'ai', text: res.summary })
        } else if (res?.status === 'accepted') {
          messages.value.push({ role: 'ai', text: '已接受任务，正在处理中...' })
        } else {
          messages.value.push({ role: 'ai', text: '已发送请求，未返回摘要。' })
        }
      } catch (err) {
        console.error(err)
        ElMessage.error('AI 总结请求失败')
      } finally {
        loading.value = false
      }
    }
  }

  setTimeout(() => {
    if (msgs.value) msgs.value.scrollTop = msgs.value.scrollHeight
  }, 50)
}

// -------------------------------------------------------------
// 发送消息
// -------------------------------------------------------------
async function onSend() {
  const text = input.value.trim()
  if (!text) return

  messages.value.push({ role: 'user', text })
  input.value = ''
  loading.value = true

  try {
    if (mode.value === 'assistant') {
      await new Promise(r => setTimeout(r, 600))
      messages.value.push({
        role: 'ai',
        text: '（占位回复）AI：我已收到你的问题，正在开发中。'
      })
    } else if (mode.value === 'summarize') {
      const res = await aiAPI.summarize(post.value?.id)
      if (res?.summary) messages.value.push({ role: 'ai', text: res.summary })
      else messages.value.push({ role: 'ai', text: '未获取到摘要结果' })
    }
  } catch (err) {
    console.error(err)
    ElMessage.error('AI 请求失败')
  } finally {
    loading.value = false
    setTimeout(() => {
      if (msgs.value) msgs.value.scrollTop = msgs.value.scrollHeight
    }, 50)
  }
}
</script>


<style scoped>
.ai-chatbox .messages {
  max-height: 360px;
  overflow-y: auto;
  padding: 12px;
  background: #fafafa;
  border-radius: 6px;
  margin-bottom: 12px;
}
.message { margin-bottom: 10px; }
.message.ai .message-content { background: #f0f4ff; }
.message.user .message-content { background: #e9f6ef; text-align: right; }
.message-content { display: inline-block; padding: 8px 12px; border-radius: 6px; }
.chat-input { display: flex; flex-direction: column; gap: 8px; }
.chat-actions { display: flex; gap: 8px; justify-content: flex-end; }
</style>