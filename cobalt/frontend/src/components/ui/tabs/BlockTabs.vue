<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="tabs">
    <div class="nav">
      <GhostButton
        type="button"
        :class="{ active: modelValue === tab.value }"
        base-color="gray"
        hover-color="blue"
        v-for="tab in tabs"
        :key="tab.value"
        :text="tab.label"
        :name="tab.value"
        @click="select(tab.value)"
      />
    </div>
    <div class="content">
      <template v-for="tab in tabs" :key="tab.value">
        <div v-show="modelValue === tab.value" class="wrapper" tabindex="-1">
          <slot :name="tab.value" />
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch } from "vue"
import { useRoute, useRouter } from "vue-router"

import type { Tab } from "@/types"

import GhostButton from "@/components/ui/forms/buttons/GhostButton.vue"

const props = withDefaults(defineProps<{
  tabs: Tab[]
  modelValue?: string | null
  queryKey?: string
}>(), {
  modelValue: null,
  queryKey: "tab"
})

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void
}>()

const route = useRoute()
const router = useRouter()

/**
 * Emits a modelValue update for the selected tab.
 *
 * Parameters:
 * - value: The value of the tab to activate.
 *
 * Returns:
 * - void.
 */
function select(value: string): void {
  emit("update:modelValue", value)
}

/**
 * Reads the query param and activates the matching tab or falls back to the first.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function applyQueryTab(): void {
  const query = route.query[props.queryKey]
  const value = Array.isArray(query) ? query[0] : query
  const match = props.tabs.find(tab => tab.value === value)
  const first = props.tabs[0]
  const target = match ?? first

  if (target) {
    select(target.value)
  }
}

/**
 * Strips the tab query param from the URL without adding a history entry.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function cleanQuery(): Promise<void> {
  const cleaned = { ...route.query }
  delete cleaned[props.queryKey]
  await router.replace({ query: cleaned })
}

onMounted(async (): Promise<void> => {
  const query = route.query[props.queryKey]
  const value = Array.isArray(query) ? query[0] : query

  applyQueryTab()

  if (value) {
    await cleanQuery()
  }
})

watch(
  () => route.query[props.queryKey],
  async (value) => {
    if (!value) return
    applyQueryTab()
    await cleanQuery()
  }
)

watch(
  () => props.tabs,
  (tabs) => {
    const exists = tabs.some(tab => tab.value === props.modelValue)
    const [first] = tabs
    if (!exists && first) {
      select(first.value)
    }
  }
)
</script>

<style scoped lang="scss">
.tabs {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;

  .nav {
    width: 100%;
    padding: $space-md $space-xl;
    background-color: var(--color-block-alt);
    box-sizing: border-box;
    display: flex;
    flex-wrap: nowrap;
    overflow-x: auto;
    overscroll-behavior: none;
    @include scrollbar-hidden();
    gap: $space-md;
    flex-shrink: 0;
  }

  .content {
    flex: 1;
    min-height: 0;
    padding: 0 $space-xl;
    display: flex;
    flex-direction: column;
  }

  .wrapper {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    overscroll-behavior: none;
    @include scrollbar();
    box-sizing: border-box;
    outline: none;
  }
}

@media (max-width: 768px) {
  .tabs {
    .nav {
      padding: $space-md $space-lg;
    }

    .content {
      padding: 0 $space-lg;
    }
  }
}
</style>