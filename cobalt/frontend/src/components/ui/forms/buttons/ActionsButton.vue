<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div ref="triggerRef" class="actions-button">
    <button class="trigger" @click="toggle">
      <span class="dots">•••</span>
    </button>
    <Teleport to="body">
      <Transition name="actions-button">
        <div
          v-if="isOpen"
          ref="menuRef"
          class="actions-button-items"
          :style="style"
          @keydown.esc="close"
        >
          <button
            v-for="item in items"
            :key="item.label"
            class="item"
            :class="{ danger: item.danger }"
            :name="item.name"
            @click="item.action(); close()"
          >
            <span class="icon" v-html="item.icon" />
            <span>{{ item.label }}</span>
          </button>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from "vue"

import type { ActionsMenuButton } from "@/types"

const MENU_MOBILE_BREAKPOINT = 768
const MENU_OFFSET_MOBILE = 10
const MENU_OFFSET_DESKTOP = 20
const MENU_GAP = 10

const props = defineProps<{
  items: ActionsMenuButton[]
}>()

const isOpen = ref(false)
const triggerRef = ref<HTMLElement | null>(null)
const menuRef = ref<HTMLElement | null>(null)
const style = ref<Record<string, string>>({})

/**
 * Toggles the menu open or closed.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function toggle(): void {
  isOpen.value = !isOpen.value
}

/**
 * Closes the menu.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function close(): void {
  isOpen.value = false
}

/**
 * Closes the menu when clicking outside the component.
 *
 * Parameters:
 * - event: Click event.
 *
 * Returns:
 * - void.
 */
function handleClickOutside(event: MouseEvent): void {
  const target = event.target as Node

  if (
    triggerRef.value &&
    !triggerRef.value.contains(target) &&
    !(menuRef.value && menuRef.value.contains(target))
  ) {
    close()
  }
}

/**
 * Computes menu position when it opens, opening upward if there is
 * insufficient space below.
 *
 * Parameters:
 * - value: Whether the menu is opening or closing.
 *
 * Returns:
 * - Promise<void>.
 */
watch(isOpen, async (value: boolean): Promise<void> => {
  if (!value || !triggerRef.value || !menuRef.value) return

  const rect = triggerRef.value.getBoundingClientRect()
  const offset = window.innerWidth <= MENU_MOBILE_BREAKPOINT ? MENU_OFFSET_MOBILE : MENU_OFFSET_DESKTOP
  const item = menuRef.value.querySelector(".item") as HTMLElement | null
  const itemHeight = item?.getBoundingClientRect().height ?? 0
  const minItemsHeight = itemHeight * props.items.length

  const spaceBelow = window.innerHeight - rect.bottom - MENU_GAP - offset
  const spaceAbove = rect.top - MENU_GAP - offset
  const openUp = spaceBelow < minItemsHeight && spaceAbove > spaceBelow

  style.value = {
    position: "fixed",
    zIndex: "1000",
    right: `${window.innerWidth - rect.right}px`,
    ...(openUp
        ? {
          bottom: `${window.innerHeight - rect.top + MENU_GAP}px`,
          maxHeight: `${spaceAbove}px`,
        }
        : {
          top: `${rect.bottom + MENU_GAP}px`,
          maxHeight: `${spaceBelow}px`,
        }
    ),
  }
}, { flush: "post" })

onMounted(() => {
  document.addEventListener("click", handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside)
})
</script>

<style scoped lang="scss">
.actions-button {
  position: relative;

  .trigger {
    background: transparent;
    border: none;
    cursor: pointer;
    color: $color-text;

    .dots {
      font-size: $font-md;
    }
  }
}
</style>

<style lang="scss">
.actions-button-items {
  background-color: $color-block-alt;
  border: 1px solid $color-border-alt;
  box-shadow: $shadow-easy;
  border-radius: 6px;
  min-width: 160px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overscroll-behavior: none;
  @include scrollbar();

  .item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: $space-md;
    padding: $space-md;
    background: none;
    border: none;
    cursor: pointer;
    color: $color-text;
    font-size: $font-sm;
    text-align: left;
    transition: background-color 0.3s;

    &:hover {
      background-color: $color-block;
    }

    &.danger {
      color: $color-red;
    }

    .icon {
      display: flex;
      align-items: center;
      flex-shrink: 0;

      svg {
        width: 14px;
        height: 14px;
      }
    }
  }
}

.actions-button-enter-active,
.actions-button-leave-active {
  transition: opacity 0.3s ease;
}

.actions-button-enter-from,
.actions-button-leave-to {
  opacity: 0;
}
</style>