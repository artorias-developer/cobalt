<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="pagination">
    <GhostButton
      type="button"
      :icon="prevIcon"
      base-color="gray"
      hover-color="gray"
      :filled="true"
      align="center"
      :disabled="!prevPage"
      :data-page="prevPage"
      @click="prevPage && emit('page-change', prevPage)"
    />
    <div class="page">
      <span>{{ currentPage }}</span>
    </div>
    <GhostButton
      type="button"
      :icon="nextIcon"
      base-color="gray"
      hover-color="gray"
      :filled="true"
      align="center"
      :disabled="!nextPage"
      :data-page="nextPage"
      @click="nextPage && emit('page-change', nextPage)"
    />
  </div>
</template>

<script setup lang="ts">
import GhostButton from "@/components/ui/forms/buttons/GhostButton.vue"
import prevIcon from "@/assets/images/svg/prev.svg?raw"
import nextIcon from "@/assets/images/svg/next.svg?raw"

defineProps<{
  currentPage: number
  prevPage?: number
  nextPage?: number
}>()

const emit = defineEmits<{
  (e: "page-change", page: number): void
}>()
</script>

<style scoped lang="scss">
.pagination {
  display: flex;
  align-items: center;
  gap: $space-md;

  :deep(.button) {
    width: 40px;
    height: 40px;

    .icon {
      width: 13px;
      height: 13px;

      svg {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
    }
  }

  .page {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    background-color: var(--color-primary);

    span {
      font-size: $font-md;
      font-weight: 600;
      color: var(--color-white);
    }
  }
}

@media (max-width: 768px) {
  .pagination {
    :deep(.button) {
      width: 36px;
      height: 36px;
    }

    .page {
      width: 36px;
      height: 36px;

      span {
        font-size: $font-sm;
      }
    }
  }
}
</style>