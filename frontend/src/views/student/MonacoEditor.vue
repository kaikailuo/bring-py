<template>
  <div ref="container" class="monaco-wrapper"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as monaco from 'monaco-editor'

const props = defineProps({
  modelValue: { type: String, default: '' },
  readOnly: { type: Boolean, default: false }
})
const emit = defineEmits(['update:modelValue'])

const container = ref(null)
let editor = null

onMounted(() => {
  editor = monaco.editor.create(container.value, {
    value: props.modelValue || '',
    language: 'python',
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