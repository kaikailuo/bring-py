import { defineStore } from 'pinia'

const STORAGE_KEY = 'bringpy_settings_v1'

const defaultState = {
  theme: 'light', // 'light' | 'dark' | 'system'
  sidebarCollapsed: false,
  headerFixed: false,
  layoutMode: 'wide', // 'wide' | 'compact'
  notificationEnabled: true,
  notificationSound: 'default', // 'default' | 'soft' | 'mute'
  taskReminder: true,
  language: 'zh-CN'
}

export const useSettingsStore = defineStore('settings', {
  state: () => ({ ...defaultState }),
  actions: {
    load() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY)
        if (raw) {
          const parsed = JSON.parse(raw)
          Object.assign(this, parsed)
        }
      } catch (e) {
        console.warn('Failed to load settings', e)
      }
      this.applyAll()
    },
    save() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
          theme: this.theme,
          sidebarCollapsed: this.sidebarCollapsed,
          headerFixed: this.headerFixed,
          layoutMode: this.layoutMode,
          notificationEnabled: this.notificationEnabled,
          notificationSound: this.notificationSound,
          taskReminder: this.taskReminder,
          language: this.language
        }))
      } catch (e) {
        console.warn('Failed to save settings', e)
      }
    },
    applyTheme() {
      const root = document.documentElement
      const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      let useDark = false
      if (this.theme === 'dark') useDark = true
      else if (this.theme === 'system') useDark = prefersDark
      else useDark = false

      if (useDark) root.classList.add('dark')
      else root.classList.remove('dark')
    },
    applyLayout() {
      const body = document.body
      if (this.headerFixed) body.classList.add('header-fixed')
      else body.classList.remove('header-fixed')

      if (this.sidebarCollapsed) body.classList.add('sidebar-collapsed')
      else body.classList.remove('sidebar-collapsed')

      if (this.layoutMode === 'wide') {
        body.classList.add('layout-wide')
        body.classList.remove('layout-compact')
      } else {
        body.classList.remove('layout-wide')
        body.classList.add('layout-compact')
      }
    },
    applyAll() {
      if (this.theme === 'dark') {
        document.documentElement.classList.add('dark')
        document.documentElement.classList.remove('light')
      } else if (this.theme === 'light') {
        document.documentElement.classList.add('light')
        document.documentElement.classList.remove('dark')
      } else {
        // 跟随系统
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
        document.documentElement.classList.toggle('dark', prefersDark)
        document.documentElement.classList.toggle('light', !prefersDark)
      }
    },
    resetAll() {
      Object.assign(this, JSON.parse(JSON.stringify(defaultState)))
      try {
        localStorage.removeItem(STORAGE_KEY)
      } catch (e) {
        console.warn('Failed to remove settings', e)
      }
      this.applyAll()
    }
  }
})
