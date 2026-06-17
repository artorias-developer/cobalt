<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="file-upload-wrapper">
    <FieldLabel
      v-if="label"
      :text="label"
      :required="required"
    />
    <div
      class="upload-area"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @click="inputRef?.click()"
    >
      <input
        ref="inputRef"
        type="file"
        class="input"
        :multiple="multiple"
        :accept="accept"
        @change="handleChange"
      />
      <div class="placeholder">
        <span>{{ placeholder ?? $t("servers.server.files.popup.upload.placeholder") }}</span>
        <span v-if="modelValue.length" class="count">
          {{ $t('servers.server.files.popup.upload.selected', { n: modelValue.length }) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, onMounted, onUnmounted, ref } from "vue"

import { FORM_KEY } from "@/utils"
import type { FormContext } from "@/types"

import FieldLabel from "@/components/ui/forms/FieldLabel.vue"

const props = withDefaults(defineProps<{
  modelValue: File[]
  validationName?: string
  label?: string
  placeholder?: string
  multiple?: boolean
  accept?: string
  required?: boolean
}>(), {
  multiple: true
})

const emit = defineEmits<{
  (e: "update:modelValue", value: File[]): void
}>()

const form = inject<FormContext | null>(FORM_KEY, null)
const inputRef = ref<HTMLInputElement | null>(null)

const id = Symbol()

/**
 * Populates the file list from a native file input change event.
 *
 * Parameters:
 * - event: Native DOM change event from the file input element.
 *
 * Returns:
 * - void.
 */
function handleChange(event: Event): void {
  const input = event.target as HTMLInputElement
  emit("update:modelValue", input.files ? Array.from(input.files) : [])
}

/**
 * Populates the file list from a drag-and-drop event.
 *
 * Parameters:
 * - event: Native DOM drop event.
 *
 * Returns:
 * - void.
 */
function handleDrop(event: DragEvent): void {
  emit("update:modelValue", event.dataTransfer?.files
    ? Array.from(event.dataTransfer.files)
    : []
  )
}

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
.file-upload-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: $space-sm;

  .upload-area {
    border: 2px dashed $color-border;
    border-radius: 8px;
    padding: $space-xl;
    cursor: pointer;
    transition: border-color 0.2s;

    &:hover {
      border-color: $color-blue;
    }

    .input {
      display: none;
    }

    .placeholder {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: $space-md;
      color: $color-description;
      font-size: $font-md;

      .count {
        color: $color-blue;
        font-weight: 600;
        font-size: $font-sm;
      }
    }
  }
}

@media (max-width: 768px) {
  .file-upload-wrapper {
    .upload-area {
      padding: $space-lg;

      .placeholder {
        font-size: $font-sm;
      }
    }
  }
}
</style>