<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div ref="qrRef" class="qr-code" />
</template>

<script setup lang="ts">
import { ref, onMounted, watch, inject } from "vue"
import QRCodeStyling from "qr-code-styling"

import { DOCUMENT_HELPER_KEY } from "@/constants"

const props = defineProps<{
  data: string
  icon?: string
}>()

const documentHelper = inject(DOCUMENT_HELPER_KEY)!

const qrRef = ref<HTMLElement | null>(null)
let qr: QRCodeStyling | null = null

/**
 * Creates QR code instance with current props.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - QRCodeStyling instance.
 */
function createQr(): QRCodeStyling {
  const titleColor = documentHelper.getRootStyle("--color-title")

  return new QRCodeStyling({
    width: 220,
    height: 220,
    type: "svg",
    data: props.data,
    dotsOptions: {
      type: "rounded",
      color: titleColor
    },
    backgroundOptions: {
      color: "transparent"
    },
    cornersSquareOptions: {
      type: "extra-rounded",
      color: titleColor
    },
    cornersDotOptions: {
      type: "dot",
      color: titleColor
    },
    imageOptions: {
      crossOrigin: "anonymous",
      margin: 5,
      imageSize: 0.3
    },
    ...(props.icon
      ? { image: `data:image/svg+xml;base64,${btoa(props.icon)}` }
      : {})
  })
}

onMounted(() => {
  if (!qrRef.value) return
  qr = createQr()
  qr.append(qrRef.value)
})

watch(
  () => [props.data, props.icon],
  () => {
    if (!qr || !qrRef.value) return
    qr.update({
      data: props.data,
      ...(props.icon
        ? { image: `data:image/svg+xml;base64,${btoa(props.icon)}` }
        : { image: "" })
    })
  }
)
</script>

<style scoped lang="scss">
.qr-code {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>