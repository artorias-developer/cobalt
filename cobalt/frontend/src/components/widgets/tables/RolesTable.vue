<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block class="roles">
    <div class="heading">
      <Header
        :icon="icon"
        :icon-color="iconColor"
        :title="title ?? $t('roles.list.title')"
        :description="description ?? $t('roles.list.description')"
        :size="size"
        :icon-filled="filled"
      />
      <Search
        :table-id="tableStoreId"
        @search-change="handleSearchChange"
      />
    </div>
    <Table
      :access-denied="!hasRolesViewAccess"
      :table-id="tableStoreId"
      :columns="columns"
      :rows="rows"
      :with-actions="true"
      @sort-change="handleSortChange"
    >
      <template #tableRowActions="{ row }">
        <GhostButton
          v-if="hasRolesUpdateAccess"
          type="button"
          :icon="editIcon"
          base-color="gray"
          hover-color="gray"
          :filled="true"
          align="center"
          name="role-edit-popup"
          @click="openEditRole(row.id)"
        />
        <GhostButton
          v-if="hasRolesDeleteAccess"
          type="button"
          :icon="trashIcon"
          base-color="red"
          hover-color="red"
          :filled="true"
          align="center"
          name="role-delete-popup"
          @click="handleDeleteRole(row.id)"
        />
      </template>
      <template #footerActions>
        <SolidButton
          v-if="hasRolesCreateAccess"
          type="button"
          :text="$t('common.create')"
          color="blue"
          name="role-create-popup"
          @click="openCreateRole"
        />
        <SolidButton
          v-if="hasSelected && hasRolesDeleteAccess"
          type="button"
          :text="$t('common.delete')"
          color="gray"
          @click="handleDeleteSelected"
        />
      </template>
      <template #footerPagination>
        <Pagination
          :current-page="pageData?.page ?? 1"
          :prev-page="pageData?.page && pageData.page > 1 ? pageData.page - 1 : undefined"
          :next-page="pageData?.page && pageData?.pages && pageData.page < pageData.pages ? pageData.page + 1 : undefined"
          @page-change="handlePageChange"
        />
      </template>
      <template #footerCounter>
        <Counter
          :total="pageData?.total ?? 0"
        />
      </template>
    </Table>
  </Block>
  <Popup ref="createRolePopup" class="create-role-popup">
    <template #content="{ close }">
      <Header
        :icon="rolesIcon"
        icon-color="blue"
        :title="$t('roles.list.popups.create.title')"
        :description="$t('roles.list.popups.create.description')"
        size="large"
        :icon-filled="true"
      />
      <Form
        ref="createRoleForm"
        class="form"
        :on-submit="() => createRoleForm?.validate() && handleCreateRole(close)"
      >
        <Input
          v-model="roleName"
          :validationName="$t('roles.list.popups.name.label')"
          :label="$t('roles.list.popups.name.label')"
          :placeholder="$t('roles.list.popups.name.placeholder')"
          name="role-name"
          :required="true"
        />
        <div class="permissions">
          <div
            v-for="group in permissionGroups"
            :key="group.label"
            class="group"
          >
            <span class="title" @click="toggleGroup(group, selectedPermissions)">{{ group.label }}</span>
            <Checkbox
              v-for="permission in group.permissions"
              :key="permission.value"
              :label="permission.label"
              :model-value="selectedPermissions.includes(permission.value)"
              @update:model-value="togglePermission(selectedPermissions, permission.value, $event)"
            />
          </div>
        </div>
      </Form>
      <div class="actions">
        <SolidButton
          type="button"
          :text="$t('common.close')"
          color="gray"
          @click="close"
        />
        <SolidButton
          type="button"
          :text="$t('common.create')"
          color="blue"
          name="role-create"
          @click="createRoleForm?.validate() && handleCreateRole(close)"
        />
      </div>
    </template>
  </Popup>
  <Popup ref="editRolePopup" class="edit-role-popup">
    <template #content="{ close }">
      <Header
        :icon="rolesIcon"
        icon-color="blue"
        :title="$t('roles.list.popups.edit.title')"
        :description="$t('roles.list.popups.edit.description')"
        size="large"
        :icon-filled="true"
      />
      <Form
        ref="editRoleForm"
        class="form"
        :on-submit="() => editRoleForm?.validate() && handleEditRole(close)"
      >
        <Input
          v-model="editRoleName"
          :validationName="$t('roles.list.popups.name.label')"
          :label="$t('roles.list.popups.name.label')"
          :placeholder="$t('roles.list.popups.name.placeholder')"
          name="role-name"
          :required="false"
        />
        <div class="permissions">
          <div
            v-for="group in permissionGroups"
            :key="group.label"
            class="group"
          >
            <span class="title" @click="toggleGroup(group, editSelectedPermissions)">{{ group.label }}</span>
            <Checkbox
              v-for="permission in group.permissions"
              :key="permission.value"
              :label="permission.label"
              :model-value="editSelectedPermissions.includes(permission.value)"
              @update:model-value="togglePermission(editSelectedPermissions, permission.value, $event)"
            />
          </div>
        </div>
      </Form>
      <div class="actions">
        <SolidButton
          type="button"
          :text="$t('common.close')"
          color="gray"
          @click="close"
        />
        <SolidButton
          type="button"
          :text="$t('common.save')"
          color="blue"
          name="role-update"
          @click="editRoleForm?.validate() && handleEditRole(close)"
        />
      </div>
    </template>
  </Popup>
  <ConfirmPopup ref="confirmPopup"/>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"
import { computed, inject, onMounted, onUnmounted, ref } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import { useTableStore, useUserStore } from "@/stores"
import { LOCALE_HELPER_KEY, HTTP_ROLES_API_SERVICE_KEY } from "@/constants"
import { PermissionEnum } from "@/types"
import type { BlockHeaderSize, Color, PermissionGroup, RolesPageRequest, RolesPageEntity, TableColumn } from "@/types"

import Block from "@/components/ui/Block.vue"
import Header from "@/components/ui/Header.vue"
import Popup from "@/components/ui/Popup.vue"
import Input from "@/components/ui/forms/Input.vue"
import Checkbox from "@/components/ui/forms/Checkbox.vue"
import GhostButton from "@/components/ui/forms/buttons/GhostButton.vue"
import SolidButton from "@/components/ui/forms/buttons/SolidButton.vue"
import Table from "@/components/ui/tables/Table.vue"
import Pagination from "@/components/ui/tables/Pagination.vue"
import Counter from "@/components/ui/tables/Counter.vue"
import Search from "@/components/ui/tables/Search.vue"
import Form from "@/components/ui/forms/Form.vue"
import ConfirmPopup from "@/components/widgets/popups/ConfirmPopup.vue"

import rolesIcon from "@/assets/images/svg/roles.svg?raw"
import trashIcon from "@/assets/images/svg/trash.svg?raw"
import editIcon from "@/assets/images/svg/edit.svg?raw"

withDefaults(defineProps<{
  icon?: string
  iconColor?: Color
  title?: string
  description?: string
  size?: BlockHeaderSize
  filled?: boolean
}>(), {
  icon: rolesIcon,
  iconColor: "blue",
  size: "large",
  filled: true
})

const localeHelper = inject(LOCALE_HELPER_KEY)!
const httpRolesApiService = inject(HTTP_ROLES_API_SERVICE_KEY)!
const tableStore = useTableStore()
const userStore = useUserStore()
const { notify } = useNotification()
const { t } = useI18n()

const pageData = ref<RolesPageEntity | null>(null)
const tableStoreId = "roles"

const createRoleForm = ref<InstanceType<typeof Form> | null>(null)
const createRolePopup = ref<InstanceType<typeof Popup> | null>(null)
const roleName = ref<string>("")
const selectedPermissions = ref<PermissionEnum[]>([])

const editRoleForm = ref<InstanceType<typeof Form> | null>(null)
const editRolePopup = ref<InstanceType<typeof Popup> | null>(null)
const editRoleId = ref<number | null>(null)
const editRoleName = ref<string>("")
const editSelectedPermissions = ref<PermissionEnum[]>([])

const confirmPopup = ref<InstanceType<typeof ConfirmPopup> | null>(null)

const permissionGroups = computed((): PermissionGroup[] => [
  {
    label: t("roles.list.permissions.groups.dashboard"),
    permissions: [
      { value: PermissionEnum.DASHBOARD_VIEW, label: t("roles.list.permissions.dashboard.view") },
      { value: PermissionEnum.DASHBOARD_CPU_VIEW, label: t("roles.list.permissions.dashboard.cpuView") },
      { value: PermissionEnum.DASHBOARD_RAM_VIEW, label: t("roles.list.permissions.dashboard.ramView") },
      { value: PermissionEnum.DASHBOARD_DISK_VIEW, label: t("roles.list.permissions.dashboard.diskView") },
      { value: PermissionEnum.DASHBOARD_LOGS_VIEW, label: t("roles.list.permissions.dashboard.logsView") }
    ]
  },
  {
    label: t("roles.list.permissions.groups.servers"),
    permissions: [
      { value: PermissionEnum.SERVERS_VIEW, label: t("roles.list.permissions.servers.view") },
      { value: PermissionEnum.SERVERS_CREATE, label: t("roles.list.permissions.servers.create") },
      { value: PermissionEnum.SERVERS_DELETE, label: t("roles.list.permissions.servers.delete") }
    ]
  },
  {
    label: t("roles.list.permissions.groups.server"),
    permissions: [
      { value: PermissionEnum.SERVER_VIEW, label: t("roles.list.permissions.server.view") },
      { value: PermissionEnum.SERVER_UPDATE, label: t("roles.list.permissions.server.update") },
      { value: PermissionEnum.SERVER_START, label: t("roles.list.permissions.server.start") },
      { value: PermissionEnum.SERVER_STOP, label: t("roles.list.permissions.server.stop") },
      { value: PermissionEnum.SERVER_CPU_VIEW, label: t("roles.list.permissions.server.cpuView") },
      { value: PermissionEnum.SERVER_RAM_VIEW, label: t("roles.list.permissions.server.ramView") },
      { value: PermissionEnum.SERVER_LOGS_VIEW, label: t("roles.list.permissions.server.logsView") },
      { value: PermissionEnum.SERVER_CONSOLE_EXECUTE, label: t("roles.list.permissions.server.consoleExecute") },
      { value: PermissionEnum.SERVER_FILES_VIEW, label: t("roles.list.permissions.server.files.view") },
      { value: PermissionEnum.SERVER_FILES_UPDATE, label: t("roles.list.permissions.server.files.update") },
      { value: PermissionEnum.SERVER_FILES_DOWNLOAD, label: t("roles.list.permissions.server.files.download") },
      { value: PermissionEnum.SERVER_SETTINGS_VIEW, label: t("roles.list.permissions.server.settings.view") },
      { value: PermissionEnum.SERVER_SETTINGS_UPDATE, label: t("roles.list.permissions.server.settings.update") }
    ]
  },
  {
    label: t("roles.list.permissions.groups.users"),
    permissions: [
      { value: PermissionEnum.USERS_VIEW, label: t("roles.list.permissions.users.view") },
      { value: PermissionEnum.USERS_CREATE, label: t("roles.list.permissions.users.create") },
      { value: PermissionEnum.USERS_UPDATE, label: t("roles.list.permissions.users.update") },
      { value: PermissionEnum.USERS_DELETE, label: t("roles.list.permissions.users.delete") }
    ]
  },
  {
    label: t("roles.list.permissions.groups.roles"),
    permissions: [
      { value: PermissionEnum.ROLES_VIEW, label: t("roles.list.permissions.roles.view") },
      { value: PermissionEnum.ROLES_CREATE, label: t("roles.list.permissions.roles.create") },
      { value: PermissionEnum.ROLES_UPDATE, label: t("roles.list.permissions.roles.update") },
      { value: PermissionEnum.ROLES_DELETE, label: t("roles.list.permissions.roles.delete") }
    ]
  },
  {
    label: t("roles.list.permissions.groups.games"),
    permissions: [
      { value: PermissionEnum.GAMES_VIEW, label: t("roles.list.permissions.games.view") }
    ]
  },
  {
    label: t("roles.list.permissions.groups.settings"),
    permissions: [
      { value: PermissionEnum.SETTINGS_CACHE_CLEAR, label: t("roles.list.permissions.settings.cache.clear") },
      { value: PermissionEnum.SETTINGS_CONTAINERS_CLEAR, label: t("roles.list.permissions.settings.containers.clear") }
    ]
  }
])

const columns: TableColumn[] = [
  {
    field: "name",
    type: "text",
    params: {
      label: {
        value: t("roles.list.columns.name"),
        highlighted: true
      },
      sorting: {
        sortable: true,
        default: false,
        field: "name"
      }
    }
  },
  {
    field: "created_at",
    type: "text",
    params: {
      label: {
        value: t("roles.list.columns.createdAt"),
        highlighted: false
      },
      sorting: {
        sortable: true,
        default: false,
        field: "created_at"
      }
    }
  }
]

/**
 * Fetches paginated roles list from the API using current page and sort state from the store.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchRoles(): Promise<void> {
  const sort = tableStore.getSort(tableStoreId)
  const page = tableStore.getPage(tableStoreId)
  const search = tableStore.getSearch(tableStoreId)

  try {
    pageData.value = await httpRolesApiService.getPage({
      page: page,
      search: search || undefined,
      sort_field: sort?.field as RolesPageRequest["sort_field"],
      sort_direction: sort?.direction
    })
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("roles.list.fetch.error")
    })
    pageData.value = null
  }
}

/**
 * Handles page change event from Pagination component.
 *
 * Parameters:
 * - page: Target page number to navigate to.
 *
 * Returns:
 * - void.
 */
function handlePageChange(page: number): void {
  tableStore.setPage(tableStoreId, page)
  fetchRoles()
}

/**
 * Handles sort change event from Table component.
 * Sort state is already updated in the store by the time this is called.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleSortChange(): void {
  fetchRoles()
}

/**
 * Handles search change event from Search component.
 * Resets page to 1 and re-fetches data with updated search query.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleSearchChange(): void {
  tableStore.setPage(tableStoreId, 1)
  fetchRoles()
}

/**
 * Toggles a permission in the given permissions array.
 * If checked - adds the value, otherwise removes it.
 *
 * Parameters:
 * - permissions: The permissions array to modify.
 * - value: Permission value to toggle.
 * - checked: Whether the permission is checked.
 *
 * Returns:
 * - void.
 */
function togglePermission(permissions: PermissionEnum[], value: PermissionEnum, checked: boolean): void {
  if (checked) {
    permissions.push(value)
  } else {
    permissions.splice(permissions.indexOf(value), 1)
  }
}

/**
 * Toggles all permissions in a group.
 * If all permissions in the group are selected - deselects all, otherwise selects all.
 *
 * Parameters:
 * - group: The permission group to toggle.
 * - permissions: The permissions array to modify.
 *
 * Returns:
 * - void.
 */
function toggleGroup(group: PermissionGroup, permissions: PermissionEnum[]): void {
  const allSelected = group.permissions.every(permission => permissions.includes(permission.value))
  const values = group.permissions.map(permission => permission.value)

  if (allSelected) {
    values.forEach(value => permissions.splice(permissions.indexOf(value), 1))
  } else {
    values.filter(value => !permissions.includes(value)).forEach(value => permissions.push(value))
  }
}

/**
 * Opens the confirm popup before deleting a role.
 *
 * Parameters:
 * - roleId: ID of the role to delete.
 *
 * Returns:
 * - void.
 */
function handleDeleteRole(roleId: number): void {
  confirmPopup.value?.open(() => deleteRole(roleId))
}

/**
 * Deletes a role by ID and refreshes the table.
 *
 * Parameters:
 * - roleId: ID of the role to delete.
 *
 * Returns:
 * - Promise<void>.
 */
async function deleteRole(roleId: number): Promise<void> {
  try {
    await httpRolesApiService.deleteOne(roleId)
    notify({
      type: "success",
      text: t("roles.list.delete.success")
    })
    fetchRoles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("roles.list.delete.error")
    })
  }
}

/**
 * Opens the confirm popup before deleting selected roles.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleDeleteSelected(): void {
  confirmPopup.value?.open(() => deleteSelected())
}

/**
 * Deletes all selected roles and refreshes the table.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function deleteSelected(): Promise<void> {
  const selected = [...tableStore.getSelected(tableStoreId)] as number[]

  try {
    await httpRolesApiService.deleteMany(selected)
    notify({
      type: "success",
      text: t("roles.list.deleteSelected.success")
    })
    tableStore.clearSelected(tableStoreId)
    fetchRoles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("roles.list.deleteSelected.error")
    })
  }
}

/**
 * Resets the create role popup form state to its initial values.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function resetCreateRoleForm(): void {
  roleName.value = ""
  selectedPermissions.value = []
}

/**
 * Resets the edit role popup form state to its initial values.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function resetEditRoleForm(): void {
  editRoleId.value = null
  editRoleName.value = ""
  editSelectedPermissions.value = []
}

/**
 * Creates a new role from the popup form data.
 * On success resets the form state, closes the popup, and refreshes the table.
 *
 * Parameters:
 * - close: Popup close callback.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleCreateRole(close: () => void): Promise<void> {
  try {
    await httpRolesApiService.createOne({
      name: roleName.value,
      permissions: selectedPermissions.value
    })
    notify({
      type: "success",
      text: t("roles.list.create.success")
    })
    close()
    resetCreateRoleForm()
    fetchRoles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("roles.list.create.error")
    })
  }
}

/**
 * Updates an existing role from the edit popup form data.
 * On success resets the form state, closes the popup, and refreshes the table.
 *
 * Parameters:
 * - close: Popup close callback.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleEditRole(close: () => void): Promise<void> {
  if (!editRoleId.value) return

  try {
    const updated = await httpRolesApiService.updateOne(editRoleId.value, {
      name: editRoleName.value || undefined,
      permissions: editSelectedPermissions.value
    })
    notify({
      type: "success",
      text: t("roles.list.update.success")
    })

    if (userStore.user?.role.id === editRoleId.value) {
      userStore.setUserRole(updated)
    }

    close()
    resetEditRoleForm()
    fetchRoles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("roles.list.update.error")
    })
  }
}

/**
 * Opens the create role popup.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function openCreateRole(): void {
  createRolePopup.value?.open()
}

/**
 * Opens the edit role popup and fetches current role data from the API.
 *
 * Parameters:
 * - roleId: ID of the role to edit.
 *
 * Returns:
 * - Promise<void>.
 */
async function openEditRole(roleId: number): Promise<void> {
  try {
    const role = await httpRolesApiService.getOne(roleId)

    editRoleId.value = role.id
    editRoleName.value = role.name
    editSelectedPermissions.value = [...role.permissions]

    editRolePopup.value?.open()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("roles.list.role.fetch.error")
    })
  }
}

/**
 * Maps roles response to flat row objects for the table.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Array<Record<string, any>>: Flat row objects with primitive values, or empty array if no data.
 */
const rows = computed((): Array<Record<string, any>> =>
  pageData.value?.roles.map(role => ({
    id: role.id,
    name: role.name,
    created_at: localeHelper.formatDateTime(role.created_at)
  })) ?? [])

/**
 * Returns true if at least one row is selected in the current table.
 * Uses selectionVersion as a reactive dependency since Set mutations are not tracked by Vue.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if at least one row is selected across any page, `false` otherwise.
 */
const hasSelected = computed((): boolean => {
  void tableStore.getSelectionVersion(tableStoreId)
  return tableStore.getSelected(tableStoreId).size > 0
})

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

/**
 * Checks whether the current user has access to create roles.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasRolesCreateAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.ROLES_CREATE)
)

/**
 * Checks whether the current user has access to update roles.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasRolesUpdateAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.ROLES_UPDATE)
)

/**
 * Checks whether the current user has access to delete roles.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasRolesDeleteAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.ROLES_DELETE)
)

onMounted(() => {
  if (hasRolesViewAccess.value) {
    fetchRoles()
  }
})

onUnmounted(() => {
  tableStore.clear(tableStoreId)
})
</script>

<style scoped lang="scss">
.roles {
  min-height: calc(82px + 40px + (82px * 4) + 83px);

  .heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: $space-xl;
    padding: $space-xl;
  }
}

@media (max-width: 768px) {
  .roles {
    min-height: calc(121px + 40px + (68px * 4) + 93px);

    .heading {
      flex-direction: column;
      align-items: flex-start;
      justify-content: unset;
      gap: $space-lg;
      padding: $space-lg;

      .search {
        width: 100%;
      }
    }
  }
}
</style>

<style lang="scss">
.create-role-popup,
.edit-role-popup {
  .form {
    .permissions {
      display: flex;
      flex-direction: column;
      gap: $space-xl;

      .group {
        display: flex;
        flex-direction: column;
        gap: $space-md;

        .title {
          font-size: $font-md;
          font-weight: 600;
          color: var(--color-description);
          cursor: pointer;
          user-select: none;
          transition: color 0.3s ease;

          &:hover {
            color: var(--color-title);
          }
        }
      }
    }
  }

  .actions {
    width: 100%;
    display: flex;
    justify-content: space-between;
    gap: $space-xl;
  }
}

@media (max-width: 768px) {
  .create-role-popup,
  .edit-role-popup {
    .form {
      .permissions {
        gap: $space-lg;

        .group {
          .title {
            font-size: $font-sm;
          }
        }
      }
    }

    .actions {
      gap: $space-md;
    }
  }
}
</style>