<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="child-block" :class="{ padded, gapped, hoverable }">
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  padded?: boolean
  gapped?: boolean
  hoverable?: boolean
}>()
</script>

<style scoped lang="scss">
.child-block {
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: $color-block;
  border-radius: 12px;
  box-sizing: border-box;
  outline: none;
  border: 2px solid transparent;
  transition: border-color 0.3s;

  &.hoverable:focus-visible {
    outline: 2px solid $color-primary;
    outline-offset: -2px;
  }

  &.hoverable:hover {
    border: 2px solid $color-primary;
  }

  &.padded {
    padding: calc(#{$space-md} - 2px);
  }

  &.gapped {
    gap: $space-md;
  }
}
</style>