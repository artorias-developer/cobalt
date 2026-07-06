<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="input-wrapper">
    <FieldLabel
      v-if="label"
      :text="label"
      :required="required"
    />
    <div class="input-container">
      <input
        class="input"
        :class="{ 'input--with-icon': isPassword }"
        v-bind="$attrs"
        :type="inputType"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :name="name"
        @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
      <button
        v-if="isPassword"
        type="button"
        class="toggle-visibility"
        :aria-label="isPasswordVisible ? 'Hide password' : 'Show password'"
        tabindex="-1"
        @click="isPasswordVisible = !isPasswordVisible"
      >
        <svg
          v-if="isPasswordVisible"
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8Z" />
          <circle cx="12" cy="12" r="3" />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24" />
          <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 11 8 11 8a13.16 13.16 0 0 1-1.67 2.68" />
          <path d="M6.61 6.61A13.526 13.526 0 0 0 1 12s4 8 11 8a9.74 9.74 0 0 0 5.39-1.61" />
          <line x1="2" y1="2" x2="22" y2="22" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, inject, onMounted, onUnmounted, ref } from "vue"

import { FORM_KEY } from "@/utils"
import type { FormContext } from "@/types"

import FieldLabel from "@/components/ui/forms/FieldLabel.vue"

defineOptions({
  inheritAttrs: false
})

const props = defineProps<{
  name?: string
  validationName?: string
  modelValue?: string
  type?: string
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  label?: string
  required?: boolean
}>()

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void
}>()

const form = inject<FormContext | null>(FORM_KEY, null)

const id = Symbol()

const isPasswordVisible = ref(false)

/**
 * Whether the current field type is "password".
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: True if `type` prop equals "password".
 */
const isPassword = computed((): boolean =>
  props.type === "password"
)

/**
 * Resolves the actual `type` attribute applied to the input element.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - string: The original `type` prop for non-password fields.
 */
const inputType = computed((): string => {
  if (!isPassword.value) {
    return props.type ?? "text"
  }

  return isPasswordVisible.value ? "text" : "password"
})

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
.input-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: $space-sm;

  .input-container {
    position: relative;
    width: 100%;
  }

  .input {
    width: 100%;
    height: 40px;
    padding: 0 $space-lg;
    color: var(--color-description);
    background-color: transparent;
    font-size: $font-md;
    font-weight: 600;
    font-family: "Montserrat", sans-serif;
    border: 2px solid var(--color-border);
    border-radius: 8px;
    outline: none;
    box-sizing: border-box;
    transition: border-color 0.3s ease;

    &.input--with-icon {
      padding-right: 40px;
    }

    &:focus {
      border: 2px solid var(--color-primary);
    }

    &::placeholder {
      color: var(--color-description-muted);
      opacity: 1;
    }
  }

  .toggle-visibility {
    position: absolute;
    top: 50%;
    right: $space-md;
    transform: translateY(-50%);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    padding: 0;
    color: var(--color-description-muted);
    background: transparent;
    border: none;
    cursor: pointer;
    transition: color 0.3s ease;

    &:hover {
      color: var(--color-description);
    }
  }
}

@media (max-width: 768px) {
  .input-wrapper {
    .input {
      height: 36px;
      font-size: $font-sm;
    }
  }
}
</style>