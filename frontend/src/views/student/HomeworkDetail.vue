<template>
  <div class="homework-detail education-card">
    <h2>{{ homework.title }}</h2>
    <p class="deadline" :class="{ urgent: isUrgent }">
      截止时间：{{ formattedDeadline }}
    </p>
    <p>{{ homework.content }}</p>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import { ref, computed } from "vue";
import { homeworkList } from "@/mock/homework";

const route = useRoute();
const homework = ref(homeworkList.find(x => x.id === route.params.id));

const formattedDeadline = computed(() =>
  new Date(homework.value.deadline).toLocaleString()
);

const isUrgent = computed(() => {
  const diff = new Date(homework.value.deadline) - new Date();
  return diff < 24 * 60 * 60 * 1000;
});
</script>

<style scoped>
.deadline.urgent {
  color: red;
  font-weight: bold;
}
</style>
