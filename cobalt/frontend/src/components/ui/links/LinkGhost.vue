<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <a
    class="button"
    :class="buttonClasses"
    :href="href"
    :target="target"
    :rel="target === '_blank' ? 'noopener noreferrer' : undefined"
    :aria-label="name"
  >
    <Icon
      v-if="icon"
      :icon="icon"
      :base-color="baseColor"
      :hover-color="hoverColor"
      :is-active="false"
    />
    <span v-if="text">{{ text }}</span>
  </a>
</template>

<script setup lang="ts">
import { computed } from "vue"

import type { Color, ButtonAlign, ButtonTarget } from "@/types"

import Icon from "@/components/ui/Icon.vue"

const props = defineProps<{
  href: string
  icon?: string
  text?: string
  baseColor: Color
  hoverColor?: Color
  name?: string
  align?: ButtonAlign
  filled?: boolean
  target?: ButtonTarget
}>()

/**
 * Returns whether the button is in "filled with text" mode.
 * In this mode the button itself gets a colored background instead of just the icon.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if filled and text are both provided.
 */
const isFilledWithText = computed((): boolean =>
  props.filled && !!props.text
)

/**
 * Returns the list of dynamic CSS classes for the link.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - string[]: Array of CSS class names based on current props.
 */
const buttonClasses = computed((): string[] => [
  props.baseColor,
  props.hoverColor ? `hover-${props.hoverColor}` : "",
  props.filled && !props.text ? "background" : "",
  isFilledWithText.value ? "background-text" : "",
  props.align ? `align-${props.align}` : "align-start",
  props.hoverColor && props.hoverColor === props.baseColor ? "same-color" : ""
])
</script>

<style scoped lang="scss">
@use "@/assets/styles/mixins" as *;

.button {
  @include button-ghost-base;
}
</style>