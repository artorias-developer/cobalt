<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="page" v-if="hasServersViewAccess" data-id="de97f626ab1b3c8e8c16b605ec79fc7f6dced8cf5b6">
    <section class="table">
      <ServersTable/>
    </section>
  </div>
  <NotFound v-else/>
</template>

<script setup lang="ts">
import { computed } from "vue"

import { useUserStore } from "@/stores"
import { PermissionEnum } from "@/types"

import ServersTable from "@/components/widgets/tables/ServersTable.vue"
import NotFound from "@/components/widgets/NotFound.vue"

const userStore = useUserStore()

/**
 * Checks whether the current user has access to view servers.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServersViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.SERVERS_VIEW)
)
</script>

<style scoped lang="scss">
.page {
  section {
    height: 100%;
    display: flex;
    justify-content: space-between;
    gap: $space-xl;
  }
}

@media (max-width: 768px) {
  .page {
    section {
      gap: $space-md;
    }
  }
}
</style>