<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block class="users">
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
      :access-denied="!hasUsersViewAccess"
      :table-id="tableStoreId"
      :columns="columns"
      :rows="rows"
      :with-actions="true"
      @sort-change="handleSortChange"
    >
      <template #tableRowActions="{ row }">
        <GhostButton
          v-if="hasUsersUpdateAccess"
          type="button"
          :icon="editIcon"
          base-color="gray"
          hover-color="gray"
          :filled="true"
          align="center"
          name="user-edit-popup"
          @click="openEditUser(row.id)"
        />
        <GhostButton
          v-if="hasUsersDeleteAccess"
          type="button"
          :icon="trashIcon"
          base-color="red"
          hover-color="red"
          :filled="true"
          align="center"
          name="user-delete-popup"
          @click="handleDeleteUser(row.id)"
        />
      </template>
      <template #footerActions>
        <SolidButton
          v-if="hasUsersCreateAccess"
          type="button"
          text="Create"
          color="blue"
          name="user-create-popup"
          @click="openCreateUser"
        />
        <SolidButton
          v-if="hasSelected && hasUsersDeleteAccess"
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
  <Popup ref="createUserPopup" class="create-user-popup">
    <template #content="{ close }">
      <Header
        :icon="usersIcon"
        icon-color="blue"
        title="User"
        description="New user creation"
        size="large"
        :icon-filled="true"
      />
      <Form
        ref="createUserForm"
        class="form"
        :on-submit="() => createUserForm?.validate() && handleCreateUser(close)"
      >
        <Input
          v-model="userLogin"
          validationName="Login"
          label="Login"
          placeholder="Enter user login"
          name="user-login"
          :required="true"
        />
        <Input
          v-model="userPassword"
          validationName="Password"
          label="Password"
          placeholder="Enter user password"
          name="user-password"
          :required="true"
        />
        <Select
          v-model="selectedRole"
          :options="roleOptions"
          validationName="Role"
          label="Role"
          placeholder="Select role..."
          name="role-select"
          :required="true"
        />
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
          name="user-create"
          @click="createUserForm?.validate() && handleCreateUser(close)"
        />
      </div>
    </template>
  </Popup>
  <Popup ref="editUserPopup" class="edit-user-popup">
    <template #content="{ close }">
      <Header
        :icon="usersIcon"
        icon-color="blue"
        title="User"
        description="Edit user"
        size="large"
        :icon-filled="true"
      />
      <Form
        ref="editUserForm"
        class="form"
        :on-submit="() => editUserForm?.validate() && handleEditUser(close)"
      >
        <Input
          v-model="editUserLogin"
          validationName="Login"
          label="Login"
          placeholder="Enter user login"
          name="user-login"
          :required="false"
        />
        <Input
          v-model="editUserPassword"
          validationName="Password"
          label="Password"
          placeholder="Enter new password"
          name="user-password"
          :required="false"
        />
        <Select
          v-model="editSelectedRole"
          :options="roleOptions"
          validationName="Role"
          label="Role"
          placeholder="Select role..."
          name="role-select"
          :required="false"
        />
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
          name="user-update"
          @click="editUserForm?.validate() && handleEditUser(close)"
        />
      </div>
    </template>
  </Popup>
  <ConfirmPopup ref="confirmPopup"/>
</template>

<script setup lang="ts">
import { ref, computed, inject, onMounted, onUnmounted } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import { LOCALE_HELPER_KEY, HTTP_USERS_API_SERVICE_KEY, HTTP_ROLES_API_SERVICE_KEY } from "@/utils"
import { useTableStore, useUserStore } from "@/stores"
import { PermissionsEnum } from "@/types"
import type {
  UsersPageEntity,
  RoleEntity,
  Color,
  BlockHeaderSize,
  TableColumn,
  UsersPageRequest,
  SelectOption
} from "@/types"

import Block from "@/components/ui/Block.vue"
import Header from "@/components/ui/Header.vue"
import Popup from "@/components/ui/Popup.vue"
import Input from "@/components/ui/forms/Input.vue"
import Select from "@/components/ui/forms/Select.vue"
import GhostButton from "@/components/ui/forms/buttons/GhostButton.vue"
import SolidButton from "@/components/ui/forms/buttons/SolidButton.vue"
import Table from "@/components/ui/tables/Table.vue"
import Pagination from "@/components/ui/tables/Pagination.vue"
import Counter from "@/components/ui/tables/Counter.vue"
import Search from "@/components/ui/tables/Search.vue"
import Form from "@/components/ui/forms/Form.vue"
import ConfirmPopup from "@/components/widgets/popups/ConfirmPopup.vue"
import usersIcon from "@/assets/images/svg/users.svg?raw"
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
  icon: usersIcon,
  iconColor: "blue",
  title: "Users",
  description: "Admin panel users",
  size: "large",
  filled: true
})

const localeHelper = inject(LOCALE_HELPER_KEY)!
const httpUsersApiService = inject(HTTP_USERS_API_SERVICE_KEY)!
const httpRolesApiService = inject(HTTP_ROLES_API_SERVICE_KEY)!
const tableStore = useTableStore()
const userStore = useUserStore()

const { notify } = useNotification()

const pageData = ref<UsersPageEntity | null>(null)
const roles = ref<RoleEntity[]>([])
const tableStoreId = "users"

const createUserForm = ref<InstanceType<typeof Form> | null>(null)
const createUserPopup = ref<InstanceType<typeof Popup> | null>(null)
const userLogin = ref<string>("")
const userPassword = ref<string>("")
const selectedRole = ref<number | undefined>(undefined)

const editUserForm = ref<InstanceType<typeof Form> | null>(null)
const editUserPopup = ref<InstanceType<typeof Popup> | null>(null)
const editUserId = ref<number | null>(null)
const editUserLogin = ref<string>("")
const editUserPassword = ref<string>("")
const editSelectedRole = ref<number | undefined>(undefined)

const confirmPopup = ref<InstanceType<typeof ConfirmPopup> | null>(null)

const columns: TableColumn[] = [
  {
    field: "login",
    type: "text",
    params: {
      label: {
        value: "Login",
        highlighted: true
      },
      sorting: {
        sortable: true,
        default: false,
        field: "login"
      }
    }
  },
  {
    field: "role",
    type: "tag",
    params: {
      label: {
        value: "Role"
      },
      sorting: {
        sortable: true,
        default: false,
        field: "role_id"
      },
      color: "green"
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
 * Fetches paginated users list from the API using current page and sort state from the store.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchUsers(): Promise<void> {
  const sort = tableStore.getSort(tableStoreId)
  const page = tableStore.getPage(tableStoreId)
  const search = tableStore.getSearch(tableStoreId)

  try {
    pageData.value = await httpUsersApiService.getPage({
      page: page,
      search: search || undefined,
      sort_field: sort?.field as UsersPageRequest["sort_field"],
      sort_direction: sort?.direction
    })
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to fetch users"
    })
    pageData.value = null
  }
}

/**
 * Fetches all roles from the API.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchRoles(): Promise<void> {
  try {
    let currentPage = 1
    let totalPages = 1
    const allRoles: RoleEntity[] = []

    do {
      const page = await httpRolesApiService.getPage({
        page: currentPage,
        limit: 100
      })

      allRoles.push(...page.roles)
      totalPages = page.pages
      currentPage++
    } while (currentPage <= totalPages)

    roles.value = allRoles
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to fetch roles"
    })
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
  fetchUsers()
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
  fetchUsers()
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
  fetchUsers()
}

/**
 * Opens the confirm popup before deleting a user.
 *
 * Parameters:
 * - userId: ID of the user to delete.
 *
 * Returns:
 * - void.
 */
function handleDeleteUser(userId: number): void {
  confirmPopup.value?.open(() => deleteUser(userId))
}

/**
 * Deletes a user by ID and refreshes the table.
 *
 * Parameters:
 * - userId: ID of the user to delete.
 *
 * Returns:
 * - Promise<void>.
 */
async function deleteUser(userId: number): Promise<void> {
  try {
    await httpUsersApiService.deleteOne(userId)
    notify({
      type: "success",
      text: "User deleted successfully"
    })
    fetchUsers()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to delete user"
    })
  }
}

/**
 * Opens the confirm popup before deleting selected users.
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
 * Deletes all selected users and refreshes the table.
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
    await httpUsersApiService.deleteMany(selected)
    notify({
      type: "success",
      text: "Users deleted successfully"
    })
    tableStore.clearSelected(tableStoreId)
    fetchUsers()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to delete selected users"
    })
  }
}

/**
 * Resets the create user popup form state to its initial values.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function resetCreateUserForm(): void {
  userLogin.value = ""
  userPassword.value = ""
  selectedRole.value = undefined
}

/**
 * Resets the edit user popup form state to its initial values.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function resetEditUserForm(): void {
  editUserId.value = null
  editUserLogin.value = ""
  editUserPassword.value = ""
  editSelectedRole.value = undefined
}

/**
 * Creates a new user from the popup form data.
 * On success resets the form state, closes the popup, and refreshes the table.
 *
 * Parameters:
 * - close: Popup close callback.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleCreateUser(close: () => void): Promise<void> {
  try {
    await httpUsersApiService.createOne({
      login: userLogin.value,
      password: userPassword.value,
      role_id: selectedRole.value as number
    })
    notify({
      type: "success",
      text: "User created successfully"
    })
    close()
    resetCreateUserForm()
    fetchUsers()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to create user"
    })
  }
}

/**
 * Updates an existing user from the edit popup form data.
 * On success resets the form state, closes the popup, and refreshes the table.
 *
 * Parameters:
 * - close: Popup close callback.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleEditUser(close: () => void): Promise<void> {
  if (!editUserId.value) return

  try {
    const updated = await httpUsersApiService.updateOne(editUserId.value, {
      login: editUserLogin.value || undefined,
      password: editUserPassword.value || undefined,
      role_id: editSelectedRole.value
    })
    notify({
      type: "success",
      text: "User updated successfully"
    })

    if (userStore.user?.id === editUserId.value) {
      userStore.updateUser(updated)
    }

    close()
    resetEditUserForm()
    fetchUsers()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to update user"
    })
  }
}

/**
 * Opens the create user popup.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function openCreateUser(): void {
  createUserPopup.value?.open()
}

/**
 * Opens the edit user popup and fetches current user data from the API.
 *
 * Parameters:
 * - userId: ID of the user to edit.
 *
 * Returns:
 * - Promise<void>.
 */
async function openEditUser(userId: number): Promise<void> {
  try {
    const user = await httpUsersApiService.getOne(userId)

    editUserId.value = user.id
    editUserLogin.value = user.login
    editUserPassword.value = ""
    editSelectedRole.value = user.role.id

    editUserPopup.value?.open()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to fetch user"
    })
  }
}

/**
 * Maps users response to flat row objects for the table.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Array<Record<string, any>>: Flat row objects with primitive values, or empty array if no data.
 */
const rows = computed((): Array<Record<string, any>> =>
  pageData.value?.users.map(user => ({
    id: user.id,
    login: user.login,
    role: user.role.name,
    created_at: localeHelper.formatDateTime(user.created_at)
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
 * Maps roles to select options.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - SelectOption[]: List of select options derived from the roles list.
 */
const roleOptions = computed((): SelectOption[] =>
  roles.value.map(role => ({
    value: role.id,
    label: role.name
  }))
)

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

/**
 * Checks whether the current user has access to create users.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasUsersCreateAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.USERS_CREATE)
)

/**
 * Checks whether the current user has access to update users.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasUsersUpdateAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.USERS_UPDATE)
)

/**
 * Checks whether the current user has access to delete users.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasUsersDeleteAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.USERS_DELETE)
)

onMounted(() => {
  if (hasUsersViewAccess.value) {
    fetchUsers()
  }
  
  if (hasUsersCreateAccess.value || hasUsersUpdateAccess.value) {
    fetchRoles()
  }
})

onUnmounted(() => {
  tableStore.clear(tableStoreId)
})
</script>

<style scoped lang="scss">
.users {
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
  .users {
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
.create-user-popup,
.edit-user-popup {
  .actions {
    width: 100%;
    display: flex;
    justify-content: space-between;
    gap: $space-xl;

    .right {
      display: flex;
      gap: $space-md;
    }
  }
}

@media (max-width: 768px) {
  .create-user-popup,
  .edit-user-popup {
    .actions {
      gap: $space-md;
    }
  }
}
</style>