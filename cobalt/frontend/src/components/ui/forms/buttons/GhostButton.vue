<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <router-link
    v-if="type === 'router-link'"
    class="button"
    :class="buttonClasses"
    :to="to!"
    :aria-label="name"
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
    :aria-label="name"
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
    :name="name"
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
  name?: string
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
  color: var(--color-description);
  background-color: transparent;
  border-radius: 6px;
  transition: background-color 0.3s ease, color 0.3s ease;
  box-sizing: border-box;

  &:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: -2px;
  }

  &:disabled {
    opacity: 0.5;
    pointer-events: none;
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
    color: var(--color-description);

    &.background {
      background-color: var(--color-gray-background);
    }

    &.background-text {
      background-color: var(--color-gray-background);
    }
  }

  &.hover-gray:hover,
  &.active.hover-gray {
    color: var(--color-description);
    background-color: var(--color-gray-background);
  }

  &.same-color.hover-gray:hover {
    background-color: color-mix(in srgb, var(--color-gray) 10%, transparent);
  }

  &.red {
    color: var(--color-red);

    &.background {
      background-color: var(--color-red-background);
    }

    &.background-text {
      background-color: var(--color-red-background);
    }
  }

  &.hover-red:hover,
  &.active.hover-red {
    color: var(--color-red);
    background-color: var(--color-red-background);
  }

  &.same-color.hover-red:hover {
    background-color: color-mix(in srgb, var(--color-red) 10%, transparent);
  }

  &.blue {
    color: var(--color-blue);

    &.background {
      background-color: var(--color-blue-background);
    }

    &.background-text {
      background-color: var(--color-blue-background);
    }
  }

  &.hover-blue:hover,
  &.active.hover-blue {
    color: var(--color-blue);
    background-color: var(--color-blue-background);
  }

  &.same-color.hover-blue:hover {
    background-color: color-mix(in srgb, var(--color-blue) 10%, transparent);
  }

  &.green {
    color: var(--color-green);

    &.background {
      background-color: var(--color-green-background);
    }

    &.background-text {
      background-color: var(--color-green-background);
    }
  }

  &.hover-green:hover,
  &.active.hover-green {
    color: var(--color-green);
    background-color: var(--color-green-background);
  }

  &.same-color.hover-green:hover {
    background-color: color-mix(in srgb, var(--color-green) 10%, transparent);
  }

  &.yellow {
    color: var(--color-yellow);

    &.background {
      background-color: var(--color-yellow-background);
    }

    &.background-text {
      background-color: var(--color-yellow-background);
    }
  }

  &.hover-yellow:hover,
  &.active.hover-yellow {
    color: var(--color-yellow);
    background-color: var(--color-yellow-background);
  }

  &.same-color.hover-yellow:hover {
    background-color: color-mix(in srgb, var(--color-yellow) 10%, transparent);
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