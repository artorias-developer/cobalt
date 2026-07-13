<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
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
        <span>{{ placeholder ?? $t("servers.server.files.popups.upload.placeholder") }}</span>
        <span v-if="modelValue.length" class="count">
          {{ $t('servers.server.files.popups.upload.selected', { n: modelValue.length }) }}
        </span>
      </div>
    </div>
    <div v-if="uploadProgress !== null" class="progress-bar">
      <div class="progress-line">
        <div class="progress-fill" :style="{ width: uploadProgress + '%' }" />
      </div>
      <span class="progress-label">{{ uploadProgress }}%</span>
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
  uploadProgress?: number | null
}>(), {
  multiple: true,
  uploadProgress: null
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
  gap: $space-md;

  .upload-area {
    height: 100px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 2px dashed var(--color-border);
    border-radius: 8px;
    padding: $space-xl;
    cursor: pointer;
    transition: border-color 0.2s;

    &:hover {
      border-color: var(--color-blue);
    }

    .input {
      display: none;
    }

    .placeholder {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: $space-md;
      color: var(--color-description-muted);
      font-size: $font-md;

      .count {
        color: var(--color-blue);
        font-weight: 600;
        font-size: $font-sm;
      }
    }
  }

  .progress-bar {
    display: flex;
    align-items: center;
    gap: $space-md;

    .progress-line {
      flex: 1;
      height: 5px;
      background-color: var(--color-border);
      border-radius: 10px;
      overflow: hidden;

      .progress-fill {
        height: 100%;
        background-color: var(--color-blue);
        border-radius: 2px;
        transition: width 0.2s ease;
      }
    }

    .progress-label {
      font-size: $font-sm;
      color: var(--color-description-muted);
      min-width: 36px;
      text-align: right;
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