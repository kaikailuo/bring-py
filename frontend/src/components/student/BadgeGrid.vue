<template>
  <div class="badge-grid">
    <BadgeCard
      v-for="badge in badges"
      :key="badge.id"
      :badge="badge"
      @click="handleBadgeClick"
    />
  </div>
</template>

<script setup>
import BadgeCard from './BadgeCard.vue'

const props = defineProps({
  badges: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['badge-click'])

const handleBadgeClick = (badge) => {
  emit('badge-click', badge)
}
</script>

<style lang="scss" scoped>
.badge-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: $spacing-lg;
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .badge-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
}

@media (max-width: 768px) {
  .badge-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: $spacing-md;
  }
}

@media (max-width: 480px) {
  .badge-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>

