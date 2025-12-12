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
          ref="chatInput"
          @keydown="onKeydown"
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
import { onBeforeUnmount } from 'vue'
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
const chatInput = ref(null)

// 处理键盘：Enter 发送，Shift+Enter 换行
function onKeydown(e) {
  if (e.key !== 'Enter') return

  const target = e.target
  const isShift = e.shiftKey

  if (!isShift) {
    e.preventDefault()
    // 调用发送（保持与按钮行为一致）
    onSend()
  } else {
    // 在光标处插入换行
    e.preventDefault()
    try {
      const start = (target.selectionStart != null) ? target.selectionStart : input.value.length
      const end = (target.selectionEnd != null) ? target.selectionEnd : start
      const v = input.value || ''
      input.value = v.substring(0, start) + '\n' + v.substring(end)
      // 恢复光标位置到新行后
      setTimeout(() => {
        if (target.setSelectionRange) target.setSelectionRange(start + 1, start + 1)
      }, 0)
    } catch (err) {
      // 回退为追加换行
      input.value = (input.value || '') + '\n'
    }
  }
}

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
  // 在关闭时请求后端清理该会话，避免内存增长
  try {
    const modeName = mode.value === 'summarize' ? 'summarize' : 'basic'
    // post.value?.id 可能为 undefined
    aiAPI.clearSession(post.value?.id ?? null, modeName)
      .catch(err => console.warn('clearSession failed', err))
  } catch (e) {
    console.warn('clearSession call error', e)
  }

  visible.value = false
}

onBeforeUnmount(() => {
  try {
    const modeName = mode.value === 'summarize' ? 'summarize' : 'basic'
    aiAPI.clearSession(post.value?.id ?? null, modeName).catch(() => {})
  } catch (e) {}
})

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
      // 先立即显示已接受提示，然后再调用 summarize
      messages.value.push({ role: 'ai', text: '已接受任务，正在处理中...' })
      loading.value = true
      try {
        const res = await aiAPI.summarize(post.value.id)
        if (res?.summary) {
          // 将最终摘要作为新的消息（与接受提示分开）
          messages.value.push({ role: 'ai', text: res.summary })
        } else if (res?.status === 'accepted') {
          // 后端仍然返回 accepted：提示已入队
          messages.value.push({ role: 'ai', text: '任务已入队，稍后可在消息中查看结果。' })
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
          // 普通对话走 chat 接口（basic mode）
          try {
            const res = await aiAPI.chat(text, null, 'basic')
            if (res?.reply) messages.value.push({ role: 'ai', text: res.reply })
            else messages.value.push({ role: 'ai', text: '（占位）未获取到回复' })
          } catch (err) {
            console.error(err)
            messages.value.push({ role: 'ai', text: 'AI 请求失败' })
          }
        } else if (mode.value === 'summarize') {
          // summarize 模式下的后续对话也走 chat 接口，但携带 post_id 与 mode 以便后端可以结合上下文处理
          try {
            const res = await aiAPI.chat(text, post.value?.id, 'summarize')
            if (res?.reply) messages.value.push({ role: 'ai', text: res.reply })
            else messages.value.push({ role: 'ai', text: '未获取到回复' })
          } catch (err) {
            console.error(err)
            messages.value.push({ role: 'ai', text: 'AI 请求失败' })
          }
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
.message-content { display: inline-block; padding: 8px 12px; border-radius: 6px; white-space: pre-wrap; word-break: break-word; }
.chat-input { display: flex; flex-direction: column; gap: 8px; }
.chat-actions { display: flex; gap: 8px; justify-content: flex-end; }
</style>