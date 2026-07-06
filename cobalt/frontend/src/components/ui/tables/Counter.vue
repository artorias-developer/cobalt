<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <span class="counter">{{ total }} {{ total === 1 ? 'item' : 'items' }}</span>
</template>

<script setup lang="ts">
defineProps<{
  total: number
}>()
</script>

<style scoped lang="scss">
.counter {
  font-size: $font-md;
  font-weight: 600;
  color: var(--color-description);
}

@media (max-width: 768px) {
  .counter {
    font-size: $font-sm;
  }
}
</style>