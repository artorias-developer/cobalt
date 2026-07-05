<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="input-wrapper">
    <FieldLabel
      v-if="label"
      :text="label"
      :required="required"
    />
    <input
      class="input"
      v-bind="$attrs"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :name="name"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
  </div>
</template>

<script setup lang="ts">
import { inject, onMounted, onUnmounted } from "vue"

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

    &:focus {
      border: 2px solid var(--color-primary);
    }

    &::placeholder {
      color: var(--color-description-muted);
      opacity: 1;
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