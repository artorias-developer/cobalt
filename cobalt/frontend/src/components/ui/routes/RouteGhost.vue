<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <router-link
    class="button"
    :class="buttonClasses"
    :to="to"
    :aria-label="name"
  >
    <Icon
      v-if="icon"
      :icon="icon"
      :base-color="baseColor"
      :hover-color="hoverColor"
      :is-active="isActiveRoute"
    />
    <span v-if="text">{{ text }}</span>
  </router-link>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from "vue-router"
import type { RouteLocationRaw } from "vue-router"

import type { Color, ButtonAlign } from "@/types"

import Icon from "@/components/ui/Icon.vue"

const props = defineProps<{
  to: RouteLocationRaw
  icon?: string
  text?: string
  baseColor: Color
  hoverColor?: Color
  name?: string
  align?: ButtonAlign
  filled?: boolean
}>()

const route = useRoute()

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
 * Checks if the current route matches the component's target route.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the current route matches the target route, otherwise `false`.
 */
const isActiveRoute = computed((): boolean => {
  if (typeof props.to === "string") {
    return route.path === props.to
  } else if (typeof props.to === "object" && "name" in props.to) {
    return route.name === props.to.name
  } else if (typeof props.to === "object" && "path" in props.to) {
    return route.path === props.to.path
  } else {
    return false
  }
})

/**
 * Returns the list of dynamic CSS classes for the button.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - string[]: Array of CSS class names based on current props and route state.
 */
const buttonClasses = computed((): string[] => [
  props.baseColor,
  props.hoverColor ? `hover-${props.hoverColor}` : "",
  props.filled && !props.text ? "background" : "",
  isFilledWithText.value ? "background-text" : "",
  isActiveRoute.value ? "active" : "",
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