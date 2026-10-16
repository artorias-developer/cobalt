<template>
  <Popup
    ref="popup"
    class="confirm-popup"
    :adaptive="true"
  >
    <template #content="{ close }">
      <Form
        id="confirm-popup"
        class="form"
        :on-submit="() => handleConfirm(close)"
      >
        <Icon
          :icon="warningIcon"
          base-color="yellow"
          :filled="true"
        />
        <div class="text">
          <span class="title">{{ title ?? $t('common.popups.delete.title') }}</span>
          <span class="message">{{ message ?? $t('common.popups.delete.message') }}</span>
        </div>
      </Form>
      <div class="actions">
        <ButtonSolid
          type="button"
          :text="cancelText ?? $t('common.cancel')"
          color="gray"
          @click="close"
        />
        <ButtonSolid
          submit
          form="confirm-popup"
          type="button"
          :text="confirmText ?? $t('common.confirm')"
          color="blue"
          name="confirm"
          :is-loading="isPopupConfirming"
        />
      </div>
    </template>
  </Popup>
</template>

<script setup lang="ts">
import { ref } from "vue"

import Icon from "@/components/ui/Icon.vue"
import Popup from "@/components/ui/Popup.vue"
import Form from "@/components/ui/forms/Form.vue"
import ButtonSolid from "@/components/ui/buttons/ButtonSolid.vue"

import warningIcon from "@/assets/images/svg/warning.svg?raw"

defineProps<{
  title?: string
  message?: string
  confirmText?: string
  cancelText?: string
}>()

const popup = ref<InstanceType<typeof Popup> | null>(null)
const isPopupConfirming = ref<boolean>(false)

let pendingCallback: (() => void | Promise<void>) | null = null

defineExpose({ open, close })

/**
 * Opens the confirm popup with a callback to invoke on confirmation.
 * The callback may be async: the confirm button shows loading until it resolves.
 *
 * Parameters:
 * - onConfirm: Callback to invoke when the user confirms the action.
 *
 * Returns:
 * - void.
 */
function open(onConfirm: () => void | Promise<void>): void {
  pendingCallback = onConfirm
  popup.value?.open()
}

/**
 * Closes the confirm popup and clears the pending callback.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function close(): void {
  popup.value?.close()
  pendingCallback = null
}

/**
 * Handles confirmation - awaits the pending callback, then closes the popup.
 * If the callback throws, the popup stays open and the loading state is reset.
 *
 * Parameters:
 * - closeFn: Popup close callback from slot.
 *
 * Returns:
 * - Promise that resolves when the callback is finished.
 */
async function handleConfirm(closeFn: () => void): Promise<void> {
  if (isPopupConfirming.value) return

  isPopupConfirming.value = true

  try {
    await pendingCallback?.()
    pendingCallback = null
    closeFn()
  } finally {
    isPopupConfirming.value = false
  }
}
</script>

<style scoped lang="scss">
.confirm-popup {
  .form {
    align-items: center;

    .text {
      display: flex;
      flex-direction: column;
      gap: $space-md;
      text-align: center;

      .title {
        font-size: $font-xl;
        font-weight: 600;
        color: var(--color-title);
      }

      .message {
        font-size: $font-sm;
        color: var(--color-description);
        line-height: 1.5;
      }
    }
  }

  .actions {
    width: 100%;
    display: flex;
    justify-content: space-between;
    gap: $space-xl;

    :deep(.button) {
      width: 100%;
    }
  }
}

@media (max-width: 768px) {
  .confirm-popup {
    .actions {
      gap: $space-lg;
    }
  }
}
</style>