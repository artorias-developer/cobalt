<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <template v-if="route.name !== RoutesEnum.LOGIN">
    <MenuNavigation
      :open="menuOpen"
      @close="menuOpen = false"
    />
    <main>
      <HeaderNavigation
        :class="{
          'mobile-only': route.name == RoutesEnum.SERVER
        }"
        @toggle-menu="menuOpen = !menuOpen"
      />
      <RouterView/>
    </main>
  </template>
  <template v-else>
    <RouterView/>
  </template>
  <Notifications
    :pauseOnHover="true"
    :duration="4000"
  >
    <template #body="{ item, close }">
      <div
        :class="['vue-notification', item.type]"
        @click="close"
      >
        <div class="icon" v-html="
          item.type === 'success' ? checkIcon :
          item.type === 'error' ? crossIcon :
          item.type === 'warn' ? warningIcon : ''
        "/>
        <p>{{ item.text }}</p>
      </div>
    </template>
  </Notifications>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRoute } from "vue-router"
import { Notifications } from "@kyvg/vue3-notification"

import { RoutesEnum } from "@/types"

import MenuNavigation from "@/components/widgets/navigations/MenuNavigation.vue"
import HeaderNavigation from "@/components/widgets/navigations/HeaderNavigation.vue"
import checkIcon from "@/assets/images/svg/check.svg?raw"
import warningIcon from "@/assets/images/svg/warning.svg?raw"
import crossIcon from "@/assets/images/svg/cross.svg?raw"

const route = useRoute()

const menuOpen = ref(false)
</script>

<style lang="scss">
main {
  width: calc(100% - 276px);
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: $space-xl;
  gap: $space-xl;
  box-sizing: border-box;

  .header {
    &.mobile-only {
      display: none;
    }
  }

  .page {
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: $space-xl;
    overflow-y: auto;
    overscroll-behavior: none;
    @include scrollbar-hidden();
  }
}

@media (max-width: 1024px) {
  main {
    width: 100%;

    .header {
      &.mobile-only {
        display: flex;
      }
    }
  }
}

@media (max-width: 768px) {
  main {
    padding: $space-md;
    gap: $space-md;

    .page {
      gap: $space-md;
    }
  }
}
</style>
