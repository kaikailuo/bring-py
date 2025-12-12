<template>
  <div class="practice-ai-chat">
    <div class="ai-status" v-if="loading">正在生成建议，请稍候...</div>
    <div class="ai-result" v-else>
        <div class="messages" ref="msgs">
          <div v-if="messages.length === 0 && !suggestion" class="empty">尚无建议，提交代码后 AI 会给出建议。</div>
          <template v-else>
            <div v-for="(m, idx) in messages" :key="idx" :class="['message', m.role]">
              <div class="message-content" v-if="m.role === 'ai'" v-html="renderMessageHtml(m.text)"></div>
              <div class="message-content user" v-else>{{ m.text }}</div>
            </div>
          </template>
        </div>

        <div class="chat-input-area">
          <el-input
            v-model="chatText"
            type="textarea"
            :rows="3"
            placeholder="向 AI 追问或澄清（Enter 发送，Shift+Enter 换行）"
            ref="chatInput"
            @keydown="onChatKeydown"
          />
          <div class="chat-actions">
            <el-button type="primary" @click="sendChat" :loading="chatLoading">发送</el-button>
          </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, toRefs, computed } from 'vue'
import { onBeforeUnmount } from 'vue'
import { ElMessage } from 'element-plus'
import { aiAPI } from '@/utils/api'
import { renderMarkdown } from '@/utils/markdown'


const props = defineProps({
  // problem 可以是一个对象，包含 id, title, description, path 等
  problem: { type: Object, default: null },
  // 提交的代码文本
  code: { type: String, default: '' },
  // 触发器：每次该数字变化时组件会请求一次建议
  trigger: { type: Number, default: 0 }
})
const { problem, code, trigger } = toRefs(props)
const emit = defineEmits(['suggestion'])

const loading = ref(false)
const suggestion = ref('')

// 聊天历史（assistant/user），AI 建议会被作为首条 assistant 消息插入
const messages = ref([])
const chatText = ref('')
const chatInput = ref(null)
const msgs = ref(null)

const suggestionHtml = computed(() => {
  const html = renderMarkdown(suggestion.value || '')
  return `<div class="markdown-body">${html}</div>`
})

// 是否在单独的 chat 请求中 loading（与请求建议分开）
const chatLoading = ref(false)

// 当 trigger 变化时触发请求（前端在每次提交后增加这个数字）
watch(trigger, (v, ov) => {
  if (v === ov) return
  if (problem.value && code.value != null) requestSuggestion()
})

async function requestSuggestion() {
  if (!problem.value) return
  loading.value = true
  suggestion.value = ''

  const payload = {
    problem_id: problem.value.id || null,
    // 同时传输题面与代码，后端可以用 problem_id 校验或补充参考答案
    problem_title: problem.value.title || '',
    problem_description: problem.value.description || '',
    code: code.value || ''
  }

  try {
    // 每次新的提交请求之前清理之前该 problem 的 feedback 会话，避免历史混淆与内存增长
    try { await aiAPI.clearSession(problem.value.id || null, 'feedback') } catch (e) { console.warn('clearSession failed', e) }
    const res = await aiAPI.suggest(payload)
      // 期待后端返回 { suggestion: '...' } 或类似结构
      if (res && (res.suggestion || res.data?.suggestion)) {
        suggestion.value = res.suggestion || res.data.suggestion
        emit('suggestion', suggestion.value)
        // 将建议作为历史消息插入
        messages.value = [{ role: 'ai', text: suggestion.value }]
        // 滚动到底部
        setTimeout(() => { if (msgs.value) msgs.value.scrollTop = msgs.value.scrollHeight }, 50)
      } else if (res && res.reply) {
        // 兼容 chat 风格返回
        suggestion.value = res.reply
        messages.value = [{ role: 'ai', text: suggestion.value }]
        emit('suggestion', suggestion.value)
        setTimeout(() => { if (msgs.value) msgs.value.scrollTop = msgs.value.scrollHeight }, 50)
      } else {
        suggestion.value = JSON.stringify(res)
        messages.value = [{ role: 'ai', text: suggestion.value }]
        emit('suggestion', suggestion.value)
        setTimeout(() => { if (msgs.value) msgs.value.scrollTop = msgs.value.scrollHeight }, 50)
      }
  } catch (err) {
    console.error('AI suggest error', err)
    ElMessage.error('AI 建议请求失败')
  } finally {
    loading.value = false
  }
}

onBeforeUnmount(() => {
  // 组件卸载时清理对应的 feedback 会话
  try {
    aiAPI.clearSession(problem.value?.id ?? null, 'feedback').catch(() => {})
  } catch (e) {}
})

function copySuggestion() {
  if (!suggestion.value) return
  navigator.clipboard?.writeText(suggestion.value).then(() => {
    ElMessage.success('已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

// 发送后续聊天消息（学生提问）
async function sendChat() {
  const text = (chatText.value || '').trim()
  if (!text) return
  // 将用户消息加入历史
  messages.value.push({ role: 'user', text })
  // 清空输入并滚动
  chatText.value = ''
  setTimeout(() => { if (msgs.value) msgs.value.scrollTop = msgs.value.scrollHeight }, 20)

  chatLoading.value = true
  try {
    // 在 suggest 场景中使用 mode='feedback'，problem.id 作为会话 key
    const res = await aiAPI.chat(text, problem.value?.id || null, 'feedback')
    const reply = res?.reply || res?.suggestion || JSON.stringify(res || '')
    messages.value.push({ role: 'ai', text: reply })
    setTimeout(() => { if (msgs.value) msgs.value.scrollTop = msgs.value.scrollHeight }, 50)
  } catch (err) {
    console.error('chat error', err)
    messages.value.push({ role: 'ai', text: 'AI 请求失败' })
  } finally {
    chatLoading.value = false
  }
}

function onChatKeydown(e) {
  if (e.key !== 'Enter') return
  const isShift = e.shiftKey
  const target = e.target
  if (!isShift) {
    e.preventDefault()
    sendChat()
  } else {
    // 插入换行到 chatText 的光标处
    try {
      const start = (target.selectionStart != null) ? target.selectionStart : chatText.value.length
      const end = (target.selectionEnd != null) ? target.selectionEnd : start
      const v = chatText.value || ''
      chatText.value = v.substring(0, start) + '\n' + v.substring(end)
      setTimeout(() => { if (target.setSelectionRange) target.setSelectionRange(start + 1, start + 1) }, 0)
    } catch (err) {
      chatText.value = (chatText.value || '') + '\n'
    }
  }
}

function renderMessageHtml(text) {
  return '<div class="markdown-body">' + renderMarkdown(text || '') + '</div>'
}
</script>

<style scoped>
.practice-ai-chat { min-height: 120px; display: flex; flex-direction: column; }
.ai-status { padding: 12px; color: #666; }
.suggestion { display: flex; flex-direction: column; gap: 8px; }
.suggestion-header { display:flex; justify-content:space-between; align-items:center }
.suggestion-body { background: #f7f7f9; padding: 18px; border-radius: 6px; max-height: 320px; overflow-y: auto; }
.suggestion-body pre { margin: 0; }
.empty { padding: 12px; color: #999 }

.messages { max-height: 50vh; overflow-y: auto; padding: 6px; display:flex; flex-direction:column; gap:8px }
.message { display:flex; }
.message.ai .message-content { background: #f0f4ff; padding: 10px 12px; border-radius: 6px; }
.message.user { justify-content: flex-end }
.message.user .message-content { background: #e9f6ef; padding: 10px 12px; border-radius: 6px; white-space: pre-wrap }
.chat-input-area { display:flex; flex-direction:column; gap:8px; margin-top:8px }
.chat-actions { display:flex; justify-content:flex-end }

/* Markdown styles - keep concise and similar to other views */
.markdown-body {
  color: #333;
  font-size: 14px;
  line-height: 1.6;
}
.markdown-body h1,
.markdown-body h2,
.markdown-body h3 {
  margin: 0 0 8px 0;
  font-weight: 600;
}
.markdown-body p { margin: 0 0 8px 0; }
.markdown-body ul,
.markdown-body ol { margin: 0 0 8px 1.2em; padding-left: 0.4em; }
.markdown-body blockquote { border-left: 3px solid #e6e6e6; padding-left: 12px; color: #666; margin: 8px 0; }
.markdown-body img { max-width: 100%; height: auto; display: block; margin: 8px 0; }
.markdown-body table { width: 100%; border-collapse: collapse; margin: 8px 0; }
.markdown-body table th,
.markdown-body table td { border: 1px solid #e6e6e6; padding: 6px 8px; }
.markdown-body code { background: rgba(0,0,0,0.04); padding: 2px 6px; border-radius: 4px; }
.markdown-body pre.hljs { padding: 12px; border-radius: 6px; overflow: auto; background: #f0f0f0; }

/* ensure mouse wheel works inside nested scrolling areas */
.suggestion-body::-webkit-scrollbar { height: 8px; width: 8px; }
.suggestion-body::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.2); border-radius: 4px; }
</style>
