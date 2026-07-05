<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="not-found">
    <div class="icon" v-html="notFoundIcon"/>
    <div class="content">
      <h1>{{ title }}</h1>
      <p>{{ message }}</p>
    </div>
    <SolidButton
      type="button"
      text="Go back"
      color="blue"
      @click="router.back()"
    />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"

import SolidButton from "@/components/ui/forms/buttons/SolidButton.vue"
import notFoundIcon from "@/assets/images/svg/404.svg?raw"

withDefaults(defineProps<{
  title?: string
  message?: string
}>(), {
  title: "Page not found",
  message: "The page does not exist or has been moved."
})

const router = useRouter()
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
      color: var(--color-text);
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