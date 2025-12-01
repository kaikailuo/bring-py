<template>
  <div ref="container" class="monaco-wrapper"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as monaco from 'monaco-editor'

const props = defineProps({
  modelValue: { type: String, default: '' },
  readOnly: { type: Boolean, default: false },
  language: { type: String, default: 'python' }
})
const emit = defineEmits(['update:modelValue'])

const container = ref(null)
let editor = null

onMounted(() => {
  editor = monaco.editor.create(container.value, {
    value: props.modelValue || '',
    language: props.language || 'python',
    automaticLayout: true,
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    theme: 'vs-dark',
    tabSize: 4,
    fontFamily: 'Monaco, Menlo, Consolas, "Courier New", monospace',
    fontSize: 15,
    readOnly: props.readOnly,
  })

  const model = editor.getModel()
  editor.onDidChangeModelContent(() => {
    const val = model.getValue()
    emit('update:modelValue', val)
  })
})

onBeforeUnmount(() => {
  if (editor) {
    editor.dispose()
    const model = editor.getModel()
    if (model) model.dispose()
  }
})

watch(() => props.modelValue, (v) => {
  if (!editor) return
  const model = editor.getModel()
  if (model && model.getValue() !== v) {
    model.setValue(v || '')
  }
})

// 监听语言变化并切换模型语言
watch(() => props.language, (lang) => {
  if (!editor) return
  const model = editor.getModel()
  if (model && lang) {
    try {
      monaco.editor.setModelLanguage(model, lang)
    } catch (e) {
      // ignore if language not registered
    }
  }
})
</script>

<style scoped>
.monaco-wrapper {
  width: 100%;
  height: 100%;
  min-height: 360px;
  border-radius: 6px;
  overflow: hidden;
}
</style>