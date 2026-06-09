<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="radio-list">
    <div v-if="searchable" class="search">
      <Input
        placeholder="Search"
        :model-value="localSearch"
        @update:model-value="localSearch = $event"
      />
      <GhostButton
        type="button"
        :icon="resetIcon"
        base-color="gray"
        hover-color="gray"
        :filled="true"
        align="center"
        @click="localSearch = ''"
      />
    </div>
    <div
      class="options"
      tabindex="0"
      @mousedown="handleMouseDown"
      @focus="handleFocus"
      @keydown.down.prevent="handleKeyDown"
      @keydown.up.prevent="handleKeyUp"
    >
      <div
        v-for="option in filteredOptions"
        :key="option.value"
        class="option"
        :class="{ selected: modelValue === option.value }"
        :data-label="option.title"
        :aria-label="name"
        @click="emit('update:modelValue', option.value)"
      >
        <div class="icon" v-if="option.icon">
          <img :src="option.icon" :alt="option.title" />
        </div>
        <div class="info">
          <h3>{{ option.title }}</h3>
          <p v-if="option.description">{{ option.description }}</p>
        </div>
        <div class="radio">
          <div class="dot" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, inject, onMounted, onUnmounted } from "vue"

import { FORM_KEY } from "@/utils"
import type { FormContext, RadioOption } from "@/types"

import Input from "@/components/ui/forms/Input.vue"
import GhostButton from "@/components/ui/forms/buttons/GhostButton.vue"
import resetIcon from "@/assets/images/svg/reset.svg?raw"

const props = defineProps<{
  validationName?: string
  options: RadioOption[]
  name?: string
  modelValue?: string | number
  searchable?: boolean
  required?: boolean
}>()

const emit = defineEmits<{
  (e: "update:modelValue", value: string | number): void
}>()

const form = inject<FormContext | null>(FORM_KEY, null)

const id = Symbol()
const localSearch = ref("")
const isFocusingByMouse = ref(false)

/**
 * Marks that the focus was triggered by a mouse interaction.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleMouseDown(): void {
  isFocusingByMouse.value = true
}

/**
 * Handles focus on the options list.
 * Selects the first option only when focused via keyboard (Tab), not mouse.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleFocus(): void {
  if (isFocusingByMouse.value) {
    isFocusingByMouse.value = false
    return
  }
  if (props.modelValue !== undefined) return
  const first = filteredOptions.value[0]
  if (first) emit("update:modelValue", first.value)
}

/**
 * Handles arrow down key — only when focus is on the options list itself.
 *
 * Parameters:
 * - event: KeyboardEvent.
 *
 * Returns:
 * - void.
 */
function handleKeyDown(event: KeyboardEvent): void {
  if (event.target !== event.currentTarget) return
  selectNext()
}

/**
 * Handles arrow up key — only when focus is on the options list itself.
 *
 * Parameters:
 * - event: KeyboardEvent.
 *
 * Returns:
 * - void.
 */
function handleKeyUp(event: KeyboardEvent): void {
  if (event.target !== event.currentTarget) return
  selectPrev()
}

/**
 * Selects the next option in the filtered list.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function selectNext(): void {
  const currentIndex = filteredOptions.value.findIndex(o => o.value === props.modelValue)
  const next = currentIndex < filteredOptions.value.length - 1 ? currentIndex + 1 : 0
  const option = filteredOptions.value[next]
  if (option) emit("update:modelValue", option.value)
}

/**
 * Selects the previous option in the filtered list.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function selectPrev(): void {
  const currentIndex = filteredOptions.value.findIndex(o => o.value === props.modelValue)
  const prev = currentIndex > 0 ? currentIndex - 1 : filteredOptions.value.length - 1
  const option = filteredOptions.value[prev]
  if (option) emit("update:modelValue", option.value)
}

/**
 * Filters options based on the local search query.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - RadioOption[]: Full options array if search is empty, otherwise filtered by title match.
 */
const filteredOptions = computed((): RadioOption[] =>
  localSearch.value
    ? props.options.filter(option => option.title.toLowerCase().includes(localSearch.value.toLowerCase()))
    : props.options
)

onMounted(() => {
  if (props.required && props.validationName && form) {
    form.register(id, {
      name: props.validationName,
      getValue: () => props.modelValue
    })
  }
})

onUnmounted(() => {
  form?.unregister(id)
})
</script>

<style scoped lang="scss">
.radio-list {
  display: flex;
  flex-direction: column;
  gap: $space-xl;

  .search {
    display: flex;
    align-items: center;
    gap: $space-md;

    .button {
      flex-shrink: 0;
    }
  }

  .options {
    display: flex;
    flex-direction: column;
    gap: $space-md;

    &:focus-visible {
      outline: none;

      .option.selected {
        outline: 2px solid $color-red;
        outline-offset: -2px;
      }
    }

    .option {
      display: flex;
      align-items: center;
      gap: $space-xl;
      padding: $space-xl;
      border-radius: 12px;
      border: 2px solid $color-block-alt;
      background-color: $color-block-alt;
      cursor: pointer;
      transition: border-color 0.3s ease;

      &.selected {
        border-color: $color-primary;

        .radio {
          border-color: $color-primary;
          background-color: $color-primary;

          .dot {
            opacity: 1;
            transform: scale(1);
          }
        }
      }

      .icon {
        width: 40px;
        height: 40px;
        flex-shrink: 0;

        img {
          width: 100%;
          height: 100%;
          object-fit: contain;
        }
      }

      .info {
        display: flex;
        flex-direction: column;
        gap: $space-sm;

        h3 {
          font-size: $font-md;
          font-weight: 600;
          color: $color-title;
        }

        p {
          font-size: $font-sm;
          font-weight: 600;
          color: $color-text;
          line-height: unset;
        }
      }

      .radio {
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        border: 2px solid $color-border;
        transition: background-color 0.3s ease, border-color 0.3s ease;
        box-sizing: border-box;
        flex-shrink: 0;

        .dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background-color: $color-title;
          opacity: 0;
          transform: scale(0);
          transition: opacity 0.3s ease, transform 0.3s ease;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .radio-list {
    gap: $space-lg;

    .options {
      .option {
        gap: $space-lg;
        padding: $space-lg;
      }
    }
  }
}
</style>