<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="label">
    <span class="text" :class="{ titled: description }">
      {{ text }}
      <span v-if="required" class="required">*</span>
    </span>
    <span v-if="description" class="description">{{ description }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  text: string
  description?: string
  required?: boolean
}>()
</script>

<style scoped lang="scss">
.label {
  display: flex;
  flex-direction: column;
  gap: $space-md;

  .text {
    font-size: $font-md;
    font-weight: 600;
    color: var(--color-description);
    transition: color 0.3s ease;

    &.titled {
      color: var(--color-title);
    }

    .required {
      color: var(--color-red);
    }
  }

  .description {
    font-size: $font-md;
    font-weight: 600;
    color: var(--color-description);
    line-height: unset;
    transition: color 0.3s ease;
  }
}

@media (max-width: 768px) {
  .label {
    .text {
      font-size: $font-sm;
    }

    .description {
      font-size: $font-sm;
    }
  }
}
</style>