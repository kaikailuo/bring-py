<template>
  <div class="system-settings">
    <div class="container">
      
      <!-- 主题设置 -->
      <el-card class="setting-card equal-card">
        <template #header>
          <span>主题设置</span>
        </template>

        <el-form label-position="top" :model="local">
          <el-radio-group v-model="local.theme" @change="onThemeChange">
            <el-radio-button label="light">浅色</el-radio-button>
            <el-radio-button label="dark">深色</el-radio-button>
            <el-radio-button label="system">跟随系统</el-radio-button>
          </el-radio-group>
        </el-form>
      </el-card>

      <!-- 通知设置 -->
      <el-card class="setting-card equal-card">
        <template #header>
          <span>通知设置</span>
        </template>

        <el-form label-position="top" :model="local">
          <el-switch
            v-model="local.notificationEnabled"
            active-text="启用通知"
            inactive-text="禁用通知"
            @change="onNotificationChange"
          />

          <div class="field" style="margin-top:12px">
            <el-select v-model="local.notificationSound" placeholder="通知声音" @change="onNotificationChange">
              <el-option label="默认" value="default" />
              <el-option label="静音" value="mute" />
            </el-select>
          </div>

          <el-switch
            v-model="local.taskReminder"
            active-text="启用任务提醒"
            inactive-text="禁用任务提醒"
            @change="onNotificationChange"
            style="margin-top:12px"
          />
        </el-form>
      </el-card>

      <!-- 语言设置 -->
      <el-card class="setting-card equal-card">
        <template #header>
          <span>语言设置</span>
        </template>

        <el-form label-position="top" :model="local">
          <el-select v-model="local.language" placeholder="选择语言" @change="onLanguageChange">
            <el-option label="中文（简体）" value="zh-CN" />
            <el-option label="English (US)" value="en-US" />
          </el-select>
        </el-form>
      </el-card>

      <!-- 系统信息与重置 -->
      <el-card class="setting-card longer-card">
        <template #header>
          <span>系统信息 & 重置</span>
        </template>

        <div class="info-row">
          <div class="label">应用版本：</div>
          <div class="value">{{ version }}</div>
        </div>

        <div class="info-row">
          <div class="label">当前角色：</div>
          <div class="value">{{ role }}</div>
        </div>

        <el-button type="danger" @click="confirmReset" class="reset-btn">
          重置所有设置
        </el-button>
      </el-card>

    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import pkg from '/package.json'

// stores
const settings = useSettingsStore()
settings.load()

const userStore = useUserStore()

// 本地副本，避免实时修改 store
const local = reactive({
  theme: settings.theme,
  notificationEnabled: settings.notificationEnabled,
  notificationSound: settings.notificationSound,
  taskReminder: settings.taskReminder,
  language: settings.language
})

const version = pkg?.version || '1.0.0'
const role = userStore.user?.role || 'student'

function persist() {
  settings.theme = local.theme
  settings.notificationEnabled = local.notificationEnabled
  settings.notificationSound = local.notificationSound
  settings.taskReminder = local.taskReminder
  settings.language = local.language
  settings.save()
  settings.applyAll()
}

const onThemeChange = persist
const onNotificationChange = persist
const onLanguageChange = persist

function confirmReset() {
  ElMessageBox.confirm('确定要重置所有设置吗？', '重置设置', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    settings.resetAll()
    local.theme = settings.theme
    local.notificationEnabled = settings.notificationEnabled
    local.notificationSound = settings.notificationSound
    local.taskReminder = settings.taskReminder
    local.language = settings.language
    ElMessage.success('设置已重置')
  })
}
</script>

<style scoped>
/* 整个设置页面容器 */
.system-settings {
  padding: 16px;
  min-height: 100vh; /* 确保高度铺满屏幕，解决底部灰色不显示问题 */
  box-sizing: border-box;
  background-color: #f5f5f5; /* 页面背景色 */
}

/* 内层容器，居中且排列卡片 */
.container {
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px; /* 卡片间距 */
}

/* 卡片通用样式 */
.setting-card {
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  background-color: #fff; /* 卡片白色背景 */
}

/* 前三个卡片等高 */
.equal-card {
  min-height: 160px; /* 可根据内容调节 */
}

/* 最后一个卡片稍微长一点 */
.longer-card {
  min-height: 240px; /* 系统信息卡稍高 */
}

/* 调整 el-card 内部 body 的 padding */
.setting-card ::v-deep(.el-card__body) {
  padding: 12px 0 0 0;
  flex: 1;
}

/* 信息行样式 */
.info-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px dashed rgba(0,0,0,0.06);
}

.info-row .label {
  color: rgba(0,0,0,0.6);
}

.info-row .value {
  color: rgba(0,0,0,0.85);
}

/* 重置按钮样式 */
.reset-btn {
  margin-top: 12px;
}
</style>
