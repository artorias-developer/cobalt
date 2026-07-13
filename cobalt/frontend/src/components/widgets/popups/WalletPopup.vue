<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Popup ref="popupRef" :adaptive="true">
    <template #content="{ close }">
      <div class="wallet-popup">
        <div class="coin" v-if="selectedWallet && selectedNetwork">
          <span class="name">{{ selectedWallet.name }}</span>
          <span class="network">({{ selectedNetwork.name }})</span>
        </div>
        <div class="qr-wrapper">
          <QrCode
            v-if="selectedWallet && selectedNetwork"
            :data="selectedNetwork.address"
            :icon="selectedWallet.icon"
          />
        </div>
        <span
          v-if="selectedNetwork"
          class="address"
          @click="copyAddress(selectedNetwork.address)"
        >
          {{ selectedNetwork.address }}
        </span>
        <div class="form">
          <Select
            v-model="selectedWalletName"
            :options="walletOptions"
            :label="$t('nav.walletPopup.coin')"
          />
          <Select
            v-model="selectedNetworkName"
            :options="networkOptions"
            :label="$t('nav.walletPopup.network')"
          />
          <SolidButton
            type="button"
            :text="$t('common.close')"
            color="gray"
            @click="close"
          />
        </div>
      </div>
    </template>
  </Popup>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"
import { ref, computed, watch } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import type { WalletButton, WalletNetwork, SelectOption } from "@/types"

import Popup from "@/components/ui/Popup.vue"
import Select from "@/components/ui/forms/Select.vue"
import SolidButton from "@/components/ui/forms/buttons/SolidButton.vue"
import QrCode from "@/components/ui/QrCode.vue"

const props = defineProps<{
  wallets: Array<WalletButton>
}>()

defineExpose({
  open
})

const { notify } = useNotification()
const { t } = useI18n()

const popupRef = ref<InstanceType<typeof Popup> | null>(null)

const selectedWalletName = ref<string>("")
const selectedNetworkName = ref<string>("")

/**
 * Opens the popup with the given wallet preselected.
 *
 * Parameters:
 * - walletName: Name of the wallet to preselect.
 *
 * Returns:
 * - void.
 */
function open(walletName: string): void {
  selectedWalletName.value = walletName
  selectedNetworkName.value = props.wallets.find(wallet => wallet.name === walletName)?.networks[0]?.name ?? ""
  popupRef.value?.open()
}

/**
 * Copies the provided address string to the system clipboard.
 *
 * Parameters:
 * - address: The text string to be copied to clipboard.
 *
 * Returns:
 * - Promise<void>.
 */
async function copyAddress(address: string): Promise<void> {
  try {
    await navigator.clipboard.writeText(address)
    notify({
      type: "success",
      text: t("common.copy.success")
    })
  } catch {
    notify({
      type: "error",
      text: t("common.copy.error")
    })
  }
}

/**
 * Returns the currently selected wallet object.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - WalletButton | undefined: The matched wallet or undefined.
 */
const selectedWallet = computed((): WalletButton | undefined =>
  props.wallets.find(wallet => wallet.name === selectedWalletName.value)
)

/**
 * Returns the currently selected network object.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - WalletNetwork | undefined: The matched network or undefined.
 */
const selectedNetwork = computed((): WalletNetwork | undefined =>
  selectedWallet.value?.networks.find(network => network.name === selectedNetworkName.value)
)

/**
 * Maps wallets to select options.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - SelectOption[]: List of select options derived from the wallets list.
 */
const walletOptions = computed((): SelectOption[] =>
  props.wallets.map(wallet => ({
    label: wallet.name,
    value: wallet.name,
    icon: wallet.icon
  }))
)

/**
 * Maps networks of the selected wallet to select options.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - SelectOption[]: List of select options derived from the selected wallet's networks.
 */
const networkOptions = computed((): SelectOption[] =>
  selectedWallet.value?.networks.map(network => ({
    label: network.name,
    value: network.name,
    icon: network.icon
  })) ?? []
)

watch(selectedWalletName, (): void => {
  selectedNetworkName.value = selectedWallet.value?.networks[0]?.name ?? ""
})
</script>

<style scoped lang="scss">
.wallet-popup {
  display: flex;
  flex-direction: column;
  gap: $space-xl;
  align-items: center;

  .coin {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: $space-sm;

    .name {
      font-size: $font-lg;
      font-weight: 700;
      color: var(--color-title);
    }

    .network {
      font-size: $font-lg;
      font-weight: 600;
      color: var(--color-description);
    }
  }

  .qr-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--color-block-alt);
    border-radius: 12px;
  }

  .address {
    font-size: $font-sm;
    font-weight: 500;
    color: var(--color-description);
    background-color: var(--color-block-alt);
    padding: $space-md;
    border-radius: 6px;
    word-break: break-all;
    text-align: center;
    cursor: pointer;
    transition: color 0.3s ease;

    &:hover {
      color: var(--color-title);
    }
  }

  .form {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: $space-xl;
  }
}

@media (max-width: 768px) {
  .wallet-popup {
    gap: $space-lg;

    .coin {
      .name {
        font-size: $font-md;
      }

      .network {
        font-size: $font-md;
      }
    }

    .address {
      font-size: $font-sm;
    }

    .form {
      gap: $space-lg;
    }
  }
}
</style>