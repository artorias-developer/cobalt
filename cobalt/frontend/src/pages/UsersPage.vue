<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="page" v-if="hasUsersViewAccess">
    <section class="table">
      <UsersTable/>
    </section>
  </div>
  <NotFound v-else/>
</template>

<script setup lang="ts">
import { computed } from "vue"

import { useUserStore } from "@/stores"
import { PermissionsEnum } from "@/types"

import UsersTable from "@/components/widgets/tables/UsersTable.vue"
import NotFound from "@/components/widgets/NotFound.vue"

const userStore = useUserStore()

/**
 * Checks whether the current user has access to view users.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasUsersViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.USERS_VIEW)
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