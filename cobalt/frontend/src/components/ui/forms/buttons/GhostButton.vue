<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <router-link
    v-if="type === 'router-link'"
    class="button"
    :class="buttonClasses"
    :to="to!"
    tabindex="0"
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
  <a
    v-else-if="type === 'a'"
    class="button"
    :class="buttonClasses"
    :href="href"
    :target="target"
    :rel="target === '_blank' ? 'noopener noreferrer' : undefined"
    tabindex="0"
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
  <button
    v-else
    type="button"
    class="button"
    :class="buttonClasses"
    tabindex="0"
  >
    <Icon
      v-if="icon"
      :icon="icon"
      :base-color="baseColor"
      :hover-color="hoverColor"
      :is-active="false"
    />
    <span v-if="text">{{ text }}</span>
  </button>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { useRoute, type RouteLocationRaw } from "vue-router"

import type {
  Color,
  ButtonAlign,
  ButtonTarget,
  ButtonType
} from "@/types"

import Icon from "@/components/ui/Icon.vue"

const props = defineProps<{
  type: ButtonType
  icon?: string
  text?: string
  baseColor: Color
  hoverColor?: Color
  align?: ButtonAlign
  filled?: boolean
  href?: string
  to?: RouteLocationRaw
  target?: ButtonTarget
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
  if (!props.to || props.type !== "router-link") return false

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
</script>

<style scoped lang="scss">
.button {
  height: 40px;
  min-width: 40px;
  display: flex;
  align-items: center;
  border: none;
  cursor: pointer;
  outline: none;
  text-decoration: none;
  gap: $space-md;
  padding: $space-md;
  color: $color-text;
  background-color: transparent;
  border-radius: 6px;
  transition: background-color 0.3s ease, color 0.3s ease;
  box-sizing: border-box;

  &:focus-visible {
    outline: 2px solid $color-primary;
    outline-offset: -2px;
  }

  &.align-start {
    justify-content: flex-start;
  }

  &.align-center {
    justify-content: center;
  }

  &.background-text {
    padding: 0 $space-xl;

    .icon {
      width: 14px;
      height: 14px;

      svg {
        width: 14px;
        height: 14px;
      }
    }
  }

  span {
    font-size: $font-md;
    font-weight: 600;
    white-space: nowrap;
  }

  &.gray {
    color: $color-text;

    &.background {
      background-color: $color-gray-background;
    }

    &.background-text {
      background-color: $color-gray-background;
    }
  }

  &.hover-gray:hover,
  &.active.hover-gray {
    color: $color-text;
    background-color: $color-gray-background;
  }

  &.same-color.hover-gray:hover {
    background-color: rgba($color-gray-background, 0.1);
  }

  &.red {
    color: $color-red;

    &.background {
      background-color: $color-red-background;
    }

    &.background-text {
      background-color: $color-red-background;
    }
  }

  &.hover-red:hover,
  &.active.hover-red {
    color: $color-red;
    background-color: $color-red-background;
  }

  &.same-color.hover-red:hover {
    background-color: rgba($color-red-background, 0.1);
  }

  &.blue {
    color: $color-blue;

    &.background {
      background-color: $color-blue-background;
    }

    &.background-text {
      background-color: $color-blue-background;
    }
  }

  &.hover-blue:hover,
  &.active.hover-blue {
    color: $color-blue;
    background-color: $color-blue-background;
  }

  &.same-color.hover-blue:hover {
    background-color: rgba($color-blue-background, 0.1);
  }

  &.green {
    color: $color-green;

    &.background {
      background-color: $color-green-background;
    }

    &.background-text {
      background-color: $color-green-background;
    }
  }

  &.hover-green:hover,
  &.active.hover-green {
    color: $color-green;
    background-color: $color-green-background;
  }

  &.same-color.hover-green:hover {
    background-color: rgba($color-green-background, 0.1);
  }

  &.yellow {
    color: $color-yellow;

    &.background {
      background-color: $color-yellow-background;
    }

    &.background-text {
      background-color: $color-yellow-background;
    }
  }

  &.hover-yellow:hover,
  &.active.hover-yellow {
    color: $color-yellow;
    background-color: $color-yellow-background;
  }

  &.same-color.hover-yellow:hover {
    background-color: rgba($color-yellow-background, 0.1);
  }

  &:disabled {
    opacity: 0.5;
    pointer-events: none;
  }
}

@media (max-width: 768px) {
  .button {
    height: 36px;
    min-width: 36px;

    span {
      font-size: $font-sm;
    }

    &.background-text {
      padding: 0 $space-lg;

      .icon {
        width: 12px;
        height: 12px;

        svg {
          width: 12px;
          height: 12px;
        }
      }
    }
  }
}
</style>