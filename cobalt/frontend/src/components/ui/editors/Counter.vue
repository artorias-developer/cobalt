<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <span class="counter">
    {{ $t('servers.server.files.counter.folders', { n: props.folders }) }},
    {{ $t('servers.server.files.counter.files', { n: props.files }) }}
  </span>
</template>

<script setup lang="ts">
const props = defineProps<{
  folders: number
  files: number
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