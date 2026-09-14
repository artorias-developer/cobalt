<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="not-found">
    <div class="icon" v-html="notFoundIcon"/>
    <div class="content">
      <h1>{{ displayTitle }}</h1>
      <p>{{ displayMessage }}</p>
    </div>
    <ButtonSolid
      type="button"
      :text="t('common.404.back')"
      color="blue"
      @click="router.back()"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { useRouter } from "vue-router"
import { useI18n } from "vue-i18n"

import ButtonSolid from "@/components/ui/buttons/ButtonSolid.vue"

import notFoundIcon from "@/assets/images/svg/404.svg?raw"

const props = defineProps<{
  title?: string
  message?: string
}>()

const { t } = useI18n()
const router = useRouter()

const displayTitle = computed(() =>
  props.title ?? t("common.404.title")
)

const displayMessage = computed(() =>
  props.message ?? t("common.404.message")
)
</script>

<style scoped lang="scss">
.not-found {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $space-xl;
  gap: $space-xl;

  .icon {
    width: 100%;
    height: max-content;
    max-width: 400px;

    svg {
      width: 100%;
      height: 100%;
    }
  }

  .content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: $space-md;

    h1 {
      font-size: $font-xxl;
      font-weight: 700;
      color: var(--color-title);
      text-align: center;
    }

    p {
      font-size: $font-md;
      font-weight: 600;
      color: var(--color-description);
      text-align: center;
    }
  }
}

@media (max-width: 768px) {
  .not-found {
    padding: $space-md;

    .content {
      h1 {
        font-size: $font-xl;
      }

      p {
        font-size: $font-sm;
      }
    }
  }
}
</style>