<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="message">
    <div class="icon" v-if="icon" v-html="icon"/>
    <p>{{ text }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon?: string
  text: string
}>()
</script>

<style scoped lang="scss">
.message {
  display: flex;
  align-items: center;
  gap: $space-md;

  .icon {
    width: 20px;
    height: 20px;
    color: var(--color-description);
    margin-bottom: 2px;

    svg {
      width: 100%;
      height: 100%;
    }
  }

  p {
    font-size: $font-md;
    font-weight: 600;
    color: var(--color-description);
  }
}

@media (max-width: 768px) {
  .message {
    .icon {
      width: 18px;
      height: 18px;
      margin-bottom: 1px;
    }

    p {
      font-size: $font-sm;
    }
  }
}
</style>