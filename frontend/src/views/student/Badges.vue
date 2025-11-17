<template>
  <div class="badges-page">
    <div class="badges-header">
      <h1 class="page-title">
        <el-icon><Trophy /></el-icon>
        徽章墙
      </h1>
      <div class="badge-stats">
        <span class="stat-item">
          已获得: <strong>{{ obtainedCount }}</strong> / {{ totalCount }}
        </span>
      </div>
    </div>

    <div class="badges-content">
      <BadgeGrid :badges="badges" @badge-click="handleBadgeClick" />
    </div>

    <!-- 徽章详情弹窗 -->
    <BadgeModal
      v-model="showModal"
      :badge="selectedBadge"
      v-if="selectedBadge"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import BadgeGrid from '@/components/student/BadgeGrid.vue'
import BadgeModal from '@/components/student/BadgeModal.vue'

const route = useRoute()

// 响应式数据
const badges = ref([])
const showModal = ref(false)
const selectedBadge = ref(null)

// 计算属性
const obtainedCount = computed(() => {
  return badges.value.filter(b => b.obtained).length
})

const totalCount = computed(() => {
  return badges.value.length
})

// 方法
const handleBadgeClick = (badge) => {
  if (badge.obtained) {
    selectedBadge.value = badge
    showModal.value = true
  }
}

// 初始化徽章数据 (mock数据)
const initBadges = () => {
  badges.value = [
    {
      id: 1,
      name: '学习达人',
      icon: '🏆',
      obtained: true,
      description: '连续学习7天',
      date: '2025-01-08',
      requirement: '连续学习7天即可获得',
      category: '学习坚持'
    },
    {
      id: 2,
      name: 'Python新手',
      icon: '🐍',
      obtained: true,
      description: '完成Python基础课程',
      date: '2025-01-05',
      requirement: '完成Python基础语法课程',
      category: '课程完成'
    },
    {
      id: 3,
      name: '编程练习家',
      icon: '💻',
      obtained: true,
      description: '完成10道编程练习',
      date: '2025-01-06',
      requirement: '完成10道编程练习题',
      category: '练习完成'
    },
    {
      id: 4,
      name: '坚持学习',
      icon: '📚',
      obtained: true,
      description: '连续学习30天',
      date: '2025-01-07',
      requirement: '连续学习30天即可获得',
      category: '学习坚持'
    },
    {
      id: 5,
      name: 'Python基础掌握者',
      icon: '⭐',
      obtained: true,
      description: '掌握Python基础知识',
      date: '2025-01-04',
      requirement: '完成Python基础课程并通过测试',
      category: '知识掌握'
    },
    {
      id: 6,
      name: '数据结构专家',
      icon: '🔗',
      obtained: false,
      description: '完成数据结构课程',
      requirement: '完成数据结构与算法课程',
      category: '课程完成'
    },
    {
      id: 7,
      name: '算法大师',
      icon: '🧩',
      obtained: false,
      description: '解决50道算法题',
      requirement: '完成50道算法编程题',
      category: '练习完成'
    },
    {
      id: 8,
      name: '全勤奖',
      icon: '📅',
      obtained: false,
      description: '连续学习100天',
      requirement: '连续学习100天即可获得',
      category: '学习坚持'
    },
    {
      id: 9,
      name: '论坛活跃者',
      icon: '💬',
      obtained: false,
      description: '在论坛发帖10次',
      requirement: '在互动交流论坛发布10个帖子',
      category: '社区参与'
    },
    {
      id: 10,
      name: '助人为乐',
      icon: '🤝',
      obtained: false,
      description: '帮助其他同学10次',
      requirement: '在论坛中回答10个问题',
      category: '社区参与'
    },
    {
      id: 11,
      name: '完美主义',
      icon: '✨',
      obtained: false,
      description: '所有练习全部正确',
      requirement: '完成所有编程练习且全部通过',
      category: '练习完成'
    },
    {
      id: 12,
      name: '学习之星',
      icon: '🌟',
      obtained: false,
      description: '学习时长超过100小时',
      requirement: '累计学习时长达到100小时',
      category: '学习坚持'
    }
  ]

  // 检查路由参数，如果有badgeId，自动打开对应徽章
  if (route.query.badgeId) {
    const badgeId = parseInt(route.query.badgeId)
    const badge = badges.value.find(b => b.id === badgeId)
    if (badge && badge.obtained) {
      handleBadgeClick(badge)
    }
  }
}

onMounted(() => {
  initBadges()
})
</script>

<style lang="scss" scoped>
.badges-page {
  padding: $spacing-xl;
  height: 100%;
  overflow-y: auto;
}

.badges-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-xl;
  padding-bottom: $spacing-lg;
  border-bottom: 1px solid $border-color;
}

.page-title {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: 2rem;
  font-weight: bold;
  color: $text-primary;
  margin: 0;
  
  .el-icon {
    font-size: 2rem;
    color: $education-purple;
  }
}

.badge-stats {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
}

.stat-item {
  font-size: $font-size-md;
  color: $text-secondary;
  
  strong {
    color: $education-purple;
    font-size: $font-size-lg;
  }
}

.badges-content {
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .badges-page {
    padding: $spacing-lg;
  }
  
  .badges-header {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-md;
  }
}
</style>

