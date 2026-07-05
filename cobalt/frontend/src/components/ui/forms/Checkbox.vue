<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <label class="checkbox" :class="{ disabled }">
    <input
      class="input"
      type="checkbox"
      :checked="modelValue"
      :disabled="disabled"
      @change="emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
    />
    <FieldLabel
      :text="label"
      :required="required"
      :class="{ checked: modelValue }"
    />
  </label>
</template>

<script setup lang="ts">
import { inject, onMounted, onUnmounted } from "vue"

import { FORM_KEY } from "@/utils"
import type { FormContext } from "@/types"

import FieldLabel from "@/components/ui/forms/FieldLabel.vue"

const props = defineProps<{
  validationName?: string
  label: string
  modelValue?: boolean
  disabled?: boolean
  required?: boolean
}>()

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void
}>()

const form = inject<FormContext | null>(FORM_KEY, null)

const id = Symbol()

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
.checkbox {
  display: flex;
  align-items: center;
  gap: $space-md;
  cursor: pointer;
  user-select: none;

  &.disabled {
    opacity: 0.5;
    pointer-events: none;
  }

  .input {
    flex-shrink: 0;
    appearance: none;
    -webkit-appearance: none;
    width: 20px;
    height: 20px;
    margin: 0;
    border: 2px solid var(--color-border);
    border-radius: 4px;
    background-color: transparent;
    cursor: pointer;
    position: relative;
    outline: none;
    transition: background-color 0.3s ease, border-color 0.3s ease;

    &::after {
      content: "";
      position: absolute;
      inset: 0;
      background-color: var(--color-white);
      -webkit-mask-image: url("@/assets/images/svg/check.svg");
      mask-image: url("@/assets/images/svg/check.svg");
      mask-repeat: no-repeat;
      mask-position: center;
      mask-size: 16px;
      opacity: 0;
      transition: opacity 0.3s ease;
    }

    &:focus-visible {
      outline: 2px solid var(--color-primary);
      outline-offset: -2px;
    }

    &:checked {
      background-color: var(--color-primary);
      border-color: var(--color-primary);

      &::after {
        opacity: 1;
      }
    }
  }

  :deep(.label) {
    &.checked .text {
      color: var(--color-title);
    }
  }
}

@media (max-width: 768px) {
  .checkbox {
    .input {
      width: 18px;
      height: 18px;
    }
  }
}
</style>