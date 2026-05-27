<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Teleport to="body">
    <Transition :name="isAnimated ? 'popup' : ''">
      <div v-if="isOpen" class="overlay" @click.self="close()">
        <Block class="popup" padded gapped :class="[$attrs.class, { adaptive }]">
          <slot name="content" :close="close" />
        </Block>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue"

import Block from "@/components/ui/Block.vue"

defineOptions({
  inheritAttrs: false
})

withDefaults(defineProps<{
  adaptive?: boolean
}>(), {
  adaptive: false
})

defineExpose({
  open,
  close
})

const isOpen = ref(false)
const isAnimated = ref(true)

/**
 * Opens the popup.
 *
 * Parameters:
 * - animated: boolean - whether to animate the opening. Defaults to true.
 *
 * Returns:
 * - void.
 */
function open(animated: boolean = true): void {
  isAnimated.value = animated
  isOpen.value = true
}

/**
 * Closes the popup.
 *
 * Parameters:
 * - animated: boolean - whether to animate the closing. Defaults to true.
 *
 * Returns:
 * - void.
 */
function close(animated: boolean = true): void {
  isAnimated.value = animated
  isOpen.value = false
}

/**
 * Handles keydown events and closes the popup on Escape key press.
 *
 * Parameters:
 * - event: KeyboardEvent - the keyboard event.
 *
 * Returns:
 * - void.
 */
function handleKeydown(event: KeyboardEvent): void {
  if (event.key === "Escape" && isOpen.value) {
    close()
  }
}

onMounted(() => {
  document.addEventListener("keydown", handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener("keydown", handleKeydown)
})
</script>

<style scoped lang="scss">
.overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.5);
  overflow-y: auto;
  overscroll-behavior: none;
  @include scrollbar-hidden();
  padding: $space-xl;
  box-sizing: border-box;

  .popup {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 700px;
    max-width: 480px;
    margin: auto;

    &.adaptive {
      height: auto;
      max-height: 700px;
    }
  }
}

.popup-enter-active,
.popup-leave-active {
  transition: opacity 0.3s ease;
}

.popup-enter-from,
.popup-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .overlay {
    padding: $space-md;

    .popup {
      height: 100%;

      &.adaptive {
        height: auto;
        max-height: 700px;
      }
    }
  }
}
</style>