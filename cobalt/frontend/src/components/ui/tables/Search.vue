<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="search">
    <GhostButton
      v-if="isActive"
      type="button"
      :icon="resetIcon"
      base-color="gray"
      hover-color="gray"
      :filled="true"
      align="center"
      @click="handleReset"
    />
    <Input
      placeholder="Search"
      :model-value="localValue"
      @update:model-value="localValue = $event"
      @keydown.enter="handleSubmit"
    />
    <GhostButton
      type="button"
      :icon="searchIcon"
      base-color="gray"
      hover-color="gray"
      :filled="true"
      align="center"
      @click="handleSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue"

import { useTableStore } from "@/stores/table"

import Input from "@/components/ui/forms/Input.vue"
import GhostButton from "@/components/ui/forms/buttons/GhostButton.vue"
import searchIcon from "@/assets/images/svg/search.svg?raw"
import resetIcon from "@/assets/images/svg/reset.svg?raw"

const props = defineProps<{
  tableId: string
}>()

const emit = defineEmits<{
  (e: "search-change"): void
}>()

const tableStore = useTableStore()

const localValue = ref<string>(tableStore.getSearch(props.tableId))

/**
 * Commits current local value to the store and emits search-change event.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleSubmit(): void {
  tableStore.setSearch(props.tableId, localValue.value)
  emit("search-change")
}

/**
 * Clears search query in both local state and store, then emits search-change event.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleReset(): void {
  localValue.value = ""
  tableStore.setSearch(props.tableId, "")
  emit("search-change")
}

/**
 * Returns true if the search query for the current table is not empty.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the search query is not empty, `false` otherwise.
 */
const isActive = computed((): boolean =>
  tableStore.getSearch(props.tableId) !== ""
)
</script>

<style scoped lang="scss">
.search {
  display: flex;
  align-items: center;
  gap: $space-md;

  :deep(.button.background) {
    flex-shrink: 0;
  }
}
</style>