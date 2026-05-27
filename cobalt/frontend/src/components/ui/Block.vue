<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="block" :class="{ padded, gapped }">
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  padded?: boolean
  gapped?: boolean
}>()
</script>

<style scoped lang="scss">
.block {
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: $color-block;
  border-radius: 12px;
  box-sizing: border-box;

  &.padded {
    padding: $space-xl;
  }

  &.gapped {
    gap: $space-xl;
  }
}

@media (max-width: 768px) {
  .block {
    &.padded {
      padding: $space-lg;
    }

    &.gapped {
      gap: $space-lg;
    }
  }
}
</style>