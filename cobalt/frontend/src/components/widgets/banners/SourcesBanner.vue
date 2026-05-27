<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <ChildBlock
    class="github"
    padded
    hoverable
    @click="openGithub"
  >
    <Header
      :icon="githubIcon"
      icon-color="blue"
      title="Sources"
      description="Star it if you like it!"
      size="small"
      :icon-filled="true"
    />
  </ChildBlock>
</template>

<script setup lang="ts">
import ChildBlock from "@/components/ui/ChildBlock.vue"
import Header from "@/components/ui/Header.vue"
import githubIcon from "@/assets/images/svg/github.svg?raw"

/**
 * Opens the GitHub repository in a new tab.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function openGithub(): void {
  window.open("https://github.com/ArtoriasCode/cobalt", "_blank", "noopener,noreferrer")
}
</script>

<style scoped lang="scss">
.github {
  cursor: pointer;
}
</style>