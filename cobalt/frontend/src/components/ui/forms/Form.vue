<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <form
    @submit.prevent
    @keydown.enter="handleEnter"
    tabindex="-1"
  >
    <slot/>
  </form>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"
import { provide, ref } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import { FORM_KEY } from "@/constants"
import type { FormField } from "@/types"

const props = defineProps<{
  onSubmit?: () => void
}>()

defineExpose({
  validate
})

const { notify } = useNotification()
const { t } = useI18n()

const fields = ref<Map<symbol, FormField>>(new Map())

/**
 * Handles the Enter key press event.
 * Calls the onSubmit callback if provided.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleEnter(): void {
  props.onSubmit?.()
}

/**
 * Registers a form field for validation.
 *
 * Parameters:
 * - id: symbol - unique identifier of the field.
 * - field: FormField - field metadata and value getter.
 *
 * Returns:
 * - void.
 */
function register(id: symbol, field: FormField): void {
  fields.value.set(id, field)
}

/**
 * Unregisters a form field by its identifier.
 *
 * Parameters:
 * - id: symbol - unique identifier of the field to remove.
 *
 * Returns:
 * - void.
 */
function unregister(id: symbol): void {
  fields.value.delete(id)
}

/**
 * Validates all registered fields sequentially.
 * Shows a warning notification for the first empty required field.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - true if all fields are filled, false if any field is empty.
 */
function validate(): boolean {
  for (const field of fields.value.values()) {
    const value = field.getValue()
    const empty = value === undefined || value === null || value === "" || (Array.isArray(value) && value.length === 0)

    if (empty) {
      notify({
        type: "warn",
        text: t("common.form.required", { field: field.name })
      })

      return false
    }
  }

  return true
}

provide(FORM_KEY, {
  register,
  unregister
})
</script>

<style scoped lang="scss">
form {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: $space-xl;
  outline: none;
  overflow-y: auto;
  overscroll-behavior: none;
  @include scrollbar();
  box-sizing: border-box;
}

@media (max-width: 768px) {
  form {
    gap: $space-lg;
  }
}
</style>