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
      // 普通对话走 chat 接口
      try {
        const res = await aiAPI.chat(text)
        if (res?.reply) messages.value.push({ role: 'ai', text: res.reply })
        else messages.value.push({ role: 'ai', text: '（占位）未获取到回复' })
      } catch (err) {
        console.error(err)
        messages.value.push({ role: 'ai', text: 'AI 请求失败' })
      }
    } else if (mode.value === 'summarize') {
      // summarize 模式下的后续对话也走 chat 接口，但携带 post_id 以便后端可以结合上下文处理
      try {
        const res = await aiAPI.chat(text, post.value?.id)
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
.message-content { display: inline-block; padding: 8px 12px; border-radius: 6px; }
.chat-input { display: flex; flex-direction: column; gap: 8px; }
.chat-actions { display: flex; gap: 8px; justify-content: flex-end; }
</style>