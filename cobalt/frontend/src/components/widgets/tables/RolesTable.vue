<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block class="roles">
    <div class="heading">
      <Header
        :icon="icon"
        :icon-color="iconColor"
        :title="title"
        :description="description"
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
          @click="handleDeleteRole(row.id)"
        />
      </template>
      <template #footerActions>
        <SolidButton
          v-if="hasRolesCreateAccess"
          type="button"
          text="Create"
          color="blue"
          @click="openCreateRole"
        />
        <SolidButton
          v-if="hasSelected && hasRolesDeleteAccess"
          type="button"
          text="Delete"
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
        title="Role"
        description="New role creation"
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
          validationName="Name"
          label="Name"
          placeholder="Enter role name"
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
          text="Close"
          color="gray"
          @click="close"
        />
        <SolidButton
          type="button"
          text="Create"
          color="blue"
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
        title="Role"
        description="Edit role"
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
          validationName="Name"
          label="Name"
          placeholder="Enter role name"
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
          text="Close"
          color="gray"
          @click="close"
        />
        <SolidButton
          type="button"
          text="Save"
          color="blue"
          @click="editRoleForm?.validate() && handleEditRole(close)"
        />
      </div>
    </template>
  </Popup>
  <ConfirmPopup ref="confirmPopup"/>
</template>

<script setup lang="ts">
import { computed, inject, onMounted, onUnmounted, ref } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import { LOCALE_HELPER_KEY, HTTP_ROLES_API_SERVICE_KEY } from "@/utils"
import { useTableStore, useUserStore } from "@/stores"
import { PermissionsEnum } from "@/types"
import type {
  BlockHeaderSize,
  Color,
  PermissionGroup,
  RolesPageRequest,
  RolesPageEntity,
  TableColumn
} from "@/types"

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
  title: "Roles",
  description: "Admin panel roles",
  size: "large",
  filled: true
})

const localeHelper = inject(LOCALE_HELPER_KEY)!
const httpRolesApiService = inject(HTTP_ROLES_API_SERVICE_KEY)!
const tableStore = useTableStore()
const userStore = useUserStore()

const { notify } = useNotification()

const pageData = ref<RolesPageEntity | null>(null)
const tableStoreId = "roles"

const createRoleForm = ref<InstanceType<typeof Form> | null>(null)
const createRolePopup = ref<InstanceType<typeof Popup> | null>(null)
const roleName = ref<string>("")
const selectedPermissions = ref<PermissionsEnum[]>([])

const editRoleForm = ref<InstanceType<typeof Form> | null>(null)
const editRolePopup = ref<InstanceType<typeof Popup> | null>(null)
const editRoleId = ref<number | null>(null)
const editRoleName = ref<string>("")
const editSelectedPermissions = ref<PermissionsEnum[]>([])

const confirmPopup = ref<InstanceType<typeof ConfirmPopup> | null>(null)

const permissionGroups: PermissionGroup[] = [
  {
    label: "Dashboard",
    permissions: [
      { value: PermissionsEnum.DASHBOARD_VIEW, label: "View dashboard" },
      { value: PermissionsEnum.DASHBOARD_CPU_VIEW, label: "View CPU metrics" },
      { value: PermissionsEnum.DASHBOARD_RAM_VIEW, label: "View RAM metrics" },
      { value: PermissionsEnum.DASHBOARD_DISK_VIEW, label: "View disk metrics" },
      { value: PermissionsEnum.DASHBOARD_LOGS_VIEW, label: "View logs" }
    ]
  },
  {
    label: "Servers",
    permissions: [
      { value: PermissionsEnum.SERVERS_VIEW, label: "View servers list" },
      { value: PermissionsEnum.SERVERS_CREATE, label: "Create new servers" },
      { value: PermissionsEnum.SERVERS_DELETE, label: "Delete existing servers" }
    ]
  },
  {
    label: "Server",
    permissions: [
      { value: PermissionsEnum.SERVER_VIEW, label: "View server page" },
      { value: PermissionsEnum.SERVER_UPDATE, label: "Edit existing server" },
      { value: PermissionsEnum.SERVER_START, label: "Start server" },
      { value: PermissionsEnum.SERVER_STOP, label: "Stop server" },
      { value: PermissionsEnum.SERVER_CPU_VIEW, label: "View server CPU metrics" },
      { value: PermissionsEnum.SERVER_RAM_VIEW, label: "View server RAM metrics" },
      { value: PermissionsEnum.SERVER_LOGS_VIEW, label: "View server logs" },
      { value: PermissionsEnum.SERVER_CONSOLE_EXECUTE, label: "Execute console commands" },
      { value: PermissionsEnum.SERVER_FILES_VIEW, label: "View server files" },
      { value: PermissionsEnum.SERVER_FILES_UPDATE, label: "Edit server files" },
      { value: PermissionsEnum.SERVER_FILES_DOWNLOAD, label: "Download server files" },
      { value: PermissionsEnum.SERVER_SETTINGS_VIEW, label: "View server settings" },
      { value: PermissionsEnum.SERVER_SETTINGS_UPDATE, label: "Edit server settings" }
    ]
  },
  {
    label: "Users",
    permissions: [
      { value: PermissionsEnum.USERS_VIEW, label: "View users list" },
      { value: PermissionsEnum.USERS_CREATE, label: "Create new users" },
      { value: PermissionsEnum.USERS_UPDATE, label: "Edit existing users" },
      { value: PermissionsEnum.USERS_DELETE, label: "Delete existing users" }
    ]
  },
  {
    label: "Roles",
    permissions: [
      { value: PermissionsEnum.ROLES_VIEW, label: "View roles list" },
      { value: PermissionsEnum.ROLES_CREATE, label: "Create new roles" },
      { value: PermissionsEnum.ROLES_UPDATE, label: "Edit existing roles" },
      { value: PermissionsEnum.ROLES_DELETE, label: "Delete existing roles" }
    ]
  },
  {
    label: "Games",
    permissions: [
      { value: PermissionsEnum.GAMES_VIEW, label: "View games list" }
    ]
  },
  {
    label: "Settings",
    permissions: [
      { value: PermissionsEnum.SETTINGS_CACHE_CLEAR, label: "Clear cached data" },
      { value: PermissionsEnum.SETTINGS_CONTAINERS_CLEAR, label: "Clear unused containers data" }
    ]
  }
]

const columns: TableColumn[] = [
  {
    field: "name",
    type: "text",
    params: {
      label: {
        value: "Name",
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
        value: "Created at",
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
      text: error?.response?.data?.message ?? "Failed to fetch roles"
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
 * If checked — adds the value, otherwise removes it.
 *
 * Parameters:
 * - permissions: The permissions array to modify.
 * - value: Permission value to toggle.
 * - checked: Whether the permission is checked.
 *
 * Returns:
 * - void.
 */
function togglePermission(permissions: PermissionsEnum[], value: PermissionsEnum, checked: boolean): void {
  if (checked) {
    permissions.push(value)
  } else {
    permissions.splice(permissions.indexOf(value), 1)
  }
}

/**
 * Toggles all permissions in a group.
 * If all permissions in the group are selected — deselects all, otherwise selects all.
 *
 * Parameters:
 * - group: The permission group to toggle.
 * - permissions: The permissions array to modify.
 *
 * Returns:
 * - void.
 */
function toggleGroup(group: PermissionGroup, permissions: PermissionsEnum[]): void {
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
      text: "Role deleted successfully"
    })
    fetchRoles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to delete role"
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
      text: "Roles deleted successfully"
    })
    tableStore.clearSelected(tableStoreId)
    fetchRoles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to delete selected roles"
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
      text: "Role created successfully"
    })
    close()
    resetCreateRoleForm()
    fetchRoles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to create role"
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
      text: "Role updated successfully"
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
      text: error?.response?.data?.message ?? "Failed to update role"
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
      text: error?.response?.data?.message ?? "Failed to fetch role"
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
  userStore.hasPermission(PermissionsEnum.ROLES_VIEW)
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
  userStore.hasPermission(PermissionsEnum.ROLES_CREATE)
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
  userStore.hasPermission(PermissionsEnum.ROLES_UPDATE)
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
  userStore.hasPermission(PermissionsEnum.ROLES_DELETE)
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
          color: $color-text;
          cursor: pointer;
          user-select: none;
          transition: color 0.3s ease;

          &:hover {
            color: $color-title;
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