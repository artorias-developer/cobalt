<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <ChildBlock class="support" padded>
    <Header
      :icon="coinIcon"
      icon-color="green"
      :title="$t('nav.banners.support.title')"
      :description="$t('nav.banners.support.description')"
      size="small"
      :icon-filled="true"
    />
    <div class="wallets">
      <GhostButton
        v-for="wallet in wallets.slice(0, 4)"
        type="button"
        :key="wallet.name"
        :icon="wallet.icon"
        :base-color="wallet.baseColor"
        :hover-color="wallet.hoverColor"
        :filled="true"
        align="center"
        @click="walletPopupRef?.open(wallet.name)"
      />
    </div>
  </ChildBlock>
  <WalletPopup ref="walletPopupRef" :wallets="wallets"/>
</template>

<script setup lang="ts">
import { ref } from "vue"

import type { WalletButton } from "@/types"

import ChildBlock from "@/components/ui/ChildBlock.vue"
import Header from "@/components/ui/Header.vue"
import GhostButton from "@/components/ui/forms/buttons/GhostButton.vue"
import WalletPopup from "@/components/widgets/popups/WalletPopup.vue"
import coinIcon from "@/assets/images/svg/coin.svg?raw"
import btcIcon from "@/assets/images/svg/btc.svg?raw"
import ethIcon from "@/assets/images/svg/eth.svg?raw"
import bnbIcon from "@/assets/images/svg/bnb.svg?raw"
import solIcon from "@/assets/images/svg/sol.svg?raw"
import trxIcon from "@/assets/images/svg/trx.svg?raw"
import usdtIcon from "@/assets/images/svg/usdt.svg?raw"
import usdcIcon from "@/assets/images/svg/usdc.svg?raw"

const walletPopupRef = ref<InstanceType<typeof WalletPopup> | null>(null)

const wallets: Array<WalletButton> = [
  {
    name: "USDC",
    icon: usdcIcon,
    baseColor: "gray",
    hoverColor: "gray",
    networks: [
      {
        name: "ERC20",
        address: "0x0C24ee1cDC35824390879Bd8A7235c473FCEcEDC",
        icon: ethIcon
      },
      {
        name: "BEP20",
        address: "0x0C24ee1cDC35824390879Bd8A7235c473FCEcEDC",
        icon: bnbIcon
      },
      {
        name: "SPL",
        address: "7gUG9Xz94V7nBEdC37DD5fhH75L6qQxRmnpke19tQVZP",
        icon: solIcon
      }
    ]
  },
  {
    name: "USDT",
    icon: usdtIcon,
    baseColor: "gray",
    hoverColor: "gray",
    networks: [
      {
        name: "ERC20",
        address: "0x0C24ee1cDC35824390879Bd8A7235c473FCEcEDC",
        icon: ethIcon
      },
      {
        name: "BEP20",
        address: "0x0C24ee1cDC35824390879Bd8A7235c473FCEcEDC",
        icon: bnbIcon
      },
      {
        name: "SPL",
        address: "7gUG9Xz94V7nBEdC37DD5fhH75L6qQxRmnpke19tQVZP",
        icon: solIcon
      },
      {
        name: "TRC20",
        address: "TK85QzUhftZmm3rfDreWnVi5Q5eE5t42e1",
        icon: trxIcon
      }
    ]
  },
  {
    name: "BTC",
    icon: btcIcon,
    baseColor: "gray",
    hoverColor: "gray",
    networks: [
      {
        name: "Bitcoin",
        address: "bc1qnw605zwkz6jz23fsydxmzms7tsh7jwp2kaumjw",
        icon: btcIcon
      }
    ]
  },
  {
    name: "ETH",
    icon: ethIcon,
    baseColor: "gray",
    hoverColor: "gray",
    networks: [
      {
        name: "Ethereum",
        address: "0x0C24ee1cDC35824390879Bd8A7235c473FCEcEDC",
        icon: ethIcon
      }
    ]
  },
  {
    name: "BNB",
    icon: bnbIcon,
    baseColor: "gray",
    hoverColor: "gray",
    networks: [
      {
        name: "BNB Smart Chain",
        address: "0x0C24ee1cDC35824390879Bd8A7235c473FCEcEDC",
        icon: bnbIcon
      }
    ]
  },
  {
    name: "SOL",
    icon: solIcon,
    baseColor: "gray",
    hoverColor: "gray",
    networks: [
      {
        name: "Solana",
        address: "7gUG9Xz94V7nBEdC37DD5fhH75L6qQxRmnpke19tQVZP",
        icon: solIcon
      }
    ]
  }
]
</script>

<style scoped lang="scss">
.support {
  .wallets {
    display: flex;
    gap: $space-md;
    margin-top: $space-md;

    .button {
      width: 100%;
    }
  }
}
</style>