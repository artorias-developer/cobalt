<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="file-upload-wrapper">
    <FormFieldLabel
      v-if="label"
      :text="label"
      :required="required"
    />
    <div
      class="upload-area"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @click="openDialog"
    >
      <input
        ref="inputRef"
        type="file"
        class="input"
        :multiple="multiple"
        :accept="accept"
        @change="handleChange"
        @cancel="processing = false"
      />
      <div class="placeholder">
        <span>{{ placeholder ?? $t("servers.server.files.popups.upload.placeholder") }}</span>
        <i
          v-if="processing"
          class="spinner"
          aria-hidden="true"
          v-html="spinnerIcon"
        />
        <span v-else-if="modelValue.length" class="count">
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
import { inject, nextTick, onMounted, onUnmounted, ref } from "vue"

import { FORM_KEY } from "@/constants"
import type { FormContext } from "@/types"

import FormFieldLabel from "@/components/ui/forms/FormFieldLabel.vue"

import spinnerIcon from "@/assets/images/svg/spinner.svg?raw"

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
const processing = ref(false)

const id = Symbol()

/**
 * Shows the processing spinner. Used as a one-time window focus listener
 * after the native file dialog closes, while the browser builds the file list.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function showProcessing(): void {
  processing.value = true
}

/**
 * Opens the native file dialog and arms a one-time window focus listener
 * that shows the processing spinner once the dialog closes.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function openDialog(): void {
  processing.value = false
  window.addEventListener("focus", showProcessing, { once: true })
  inputRef.value?.click()
}

/**
 * Shows the processing spinner, waits for it to be painted, then converts
 * the FileList to an array and publishes it to the parent. When `multiple`
 * is disabled, only the first file is kept. Resets the native input so the
 * same files can be selected again.
 *
 * Parameters:
 * - files: FileList from the input or the drop event, or null.
 *
 * Returns:
 * - Promise<void>.
 */
async function applyFiles(files: FileList | null): Promise<void> {
  processing.value = true

  await nextTick()
  await new Promise<void>(resolve => requestAnimationFrame(() => setTimeout(resolve, 0)))

  const list = files ? Array.from(files) : []
  emit("update:modelValue", props.multiple ? list : list.slice(0, 1))

  if (inputRef.value) {
    inputRef.value.value = ""
  }

  await nextTick()
  processing.value = false
}

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
  void applyFiles(input.files)
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
  void applyFiles(event.dataTransfer?.files ?? null)
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
  window.removeEventListener("focus", showProcessing)
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

      .spinner {
        width: 20px;
        height: 20px;
        display: flex;
        animation: file-upload-spin 0.8s linear infinite;

        :deep(svg) {
          width: 100%;
          height: 100%;
        }
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

@keyframes file-upload-spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .file-upload-wrapper {
    .upload-area {
      padding: $space-lg;

      .placeholder {
        font-size: $font-sm;

        .spinner {
          width: 18px;
          height: 18px;
        }
      }
    }
  }
}
</style>