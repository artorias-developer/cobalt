<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="page" v-if="hasRolesViewAccess">
    <section class="table">
      <RolesTable/>
    </section>
  </div>
  <NotFound v-else/>
</template>

<script setup lang="ts">
import { computed } from "vue"

import { useUserStore } from "@/stores"
import { PermissionEnum } from "@/types"

import RolesTable from "@/components/widgets/tables/RolesTable.vue"
import NotFound from "@/components/widgets/NotFound.vue"

const userStore = useUserStore()

/**
 * Checks whether the current user has access to view roles.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasRolesViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.ROLES_VIEW)
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