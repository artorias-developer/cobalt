<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block class="servers">
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
      :access-denied="!hasServersViewAccess"
      :table-id="tableStoreId"
      :columns="columns"
      :rows="rows"
      :with-actions="true"
      @sort-change="handleSortChange"
    >
      <template #tableRowActions="{ row }">
        <template v-if="row.status !== ServerStatusEnum.CREATED">
          <div class="status-icon">
            <Icon
              :icon="row.status === ServerStatusEnum.FAILED ? errorIcon : clockIcon"
              :base-color="row.status === ServerStatusEnum.FAILED ? 'red' : 'yellow'"
              :filled="true"
            />
            <span class="hint">{{ statusMessages[row.status as ServerStatusEnum] }}</span>
          </div>
        </template>
        <GhostButton
          v-if="row.status === ServerStatusEnum.CREATED && hasServerViewAccess"
          type="router-link"
          :icon="settingsIcon"
          base-color="gray"
          hover-color="gray"
          :filled="true"
          align="center"
          :to="`/servers/${row.gameName}/${row.id}`"
        />
        <GhostButton
          v-if="(row.status === ServerStatusEnum.CREATED || row.status === ServerStatusEnum.FAILED) && hasServersDeleteAccess"
          type="button"
          :icon="trashIcon"
          base-color="red"
          hover-color="red"
          :filled="true"
          align="center"
          @click="handleDeleteServer(row.id)"
        />
      </template>
      <template #footerActions>
        <SolidButton
          v-if="hasServersCreateAccess"
          type="button"
          text="Create"
          color="blue"
          @click="openCreateServer"
        />
        <SolidButton
          v-if="hasSelected && hasServersDeleteAccess"
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
  <Popup ref="createServerPopup" class="create-server-popup">
    <template #content="{ close }">
      <template v-if="createServerStep === 1">
        <Header
          :icon="serversIcon"
          icon-color="blue"
          title="Step 1 of 2"
          description="Game selection"
          size="large"
          :icon-filled="true"
        />
        <Form
          ref="step1Form"
          class="form"
          :on-submit="() => step1Form?.validate() && (createServerStep = 2)"
        >
          <RadioList
            v-model="selectedGame"
            :options="gameOptions"
            :searchable="true"
            :required="true"
            validationName="Game"
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
            text="Next"
            color="blue"
            @click="step1Form?.validate() && (createServerStep = 2)"
          />
        </div>
      </template>
      <template v-else-if="createServerStep === 2">
        <Header
          :icon="serversIcon"
          icon-color="blue"
          title="Step 2 of 2"
          description="Server properties"
          size="large"
          :icon-filled="true"
        />
        <Form
          ref="step2Form"
          class="form"
          :on-submit="() => step2Form?.validate() && handleCreateServer(close)"
        >
          <div class="selected-game" v-if="selectedGameEntity">
            <img
              :src="selectedGameModule?.icon"
              :alt="selectedGameModule?.displayName"
              class="game-icon"
            />
            <div class="game-info">
              <h3>{{ selectedGameModule?.displayName }}</h3>
              <p>{{ selectedGameModule?.description }}</p>
            </div>
          </div>
          <Input
            v-model="serverName"
            validationName="Name"
            label="Name"
            placeholder="Enter server name"
            :required="true"
          />
          <Select
            v-model="selectedLoader"
            :options="loaderOptions"
            validationName="Loader"
            label="Loader"
            placeholder="Select loader..."
            :required="true"
            @update:model-value="selectedVersion = undefined"
          />
          <Select
            v-model="selectedVersion"
            :options="versionOptions"
            validationName="Version"
            label="Version"
            placeholder="Select version..."
            :required="true"
            :disabled="!selectedLoader"
          />
        </Form>
        <div class="actions">
          <div class="left">
            <SolidButton
              type="button"
              text="Close"
              color="gray"
              @click="close"
            />
          </div>
          <div class="right">
            <SolidButton
              type="button"
              text="Back"
              color="gray"
              @click="createServerStep = 1"
            />
            <SolidButton
              type="button"
              text="Create"
              color="blue"
              @click="step2Form?.validate() && handleCreateServer(close)"
            />
          </div>
        </div>
      </template>
    </template>
  </Popup>
  <ConfirmPopup ref="confirmPopup"/>
</template>

<script setup lang="ts">
import { ref, computed, inject, onMounted, onUnmounted } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import { LOCALE_HELPER_KEY, HTTP_SERVERS_API_SERVICE_KEY, HTTP_GAMES_API_SERVICE_KEY, GameModules } from "@/utils"
import { useTableStore, useUserStore } from "@/stores"
import { PermissionsEnum, ServerStatusEnum } from "@/types"
import type {
  ServersPageEntity,
  GameEntity,
  Color,
  BlockHeaderSize,
  TableColumn,
  ServersPageRequest,
  RadioOption,
  SelectOption
} from "@/types"

import Block from "@/components/ui/Block.vue"
import Icon from "@/components/ui/Icon.vue"
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
import RadioList from "@/components/ui/forms/RadioList.vue"
import Form from "@/components/ui/forms/Form.vue"
import ConfirmPopup from "@/components/widgets/popups/ConfirmPopup.vue"
import serversIcon from "@/assets/images/svg/servers.svg?raw"
import trashIcon from "@/assets/images/svg/trash.svg?raw"
import settingsIcon from "@/assets/images/svg/settings.svg?raw"
import errorIcon from "@/assets/images/svg/error.svg?raw"
import clockIcon from "@/assets/images/svg/clock.svg?raw"

withDefaults(defineProps<{
  icon?: string
  iconColor?: Color
  title?: string
  description?: string
  size?: BlockHeaderSize
  filled?: boolean
}>(), {
  icon: serversIcon,
  iconColor: "blue",
  title: "Servers",
  description: "Created game servers",
  size: "large",
  filled: true
})

const localeHelper = inject(LOCALE_HELPER_KEY)!
const httpServersApiService = inject(HTTP_SERVERS_API_SERVICE_KEY)!
const httpGamesApiService = inject(HTTP_GAMES_API_SERVICE_KEY)!
const tableStore = useTableStore()
const userStore = useUserStore()

const { notify } = useNotification()

const pageData = ref<ServersPageEntity | null>(null)
const games = ref<GameEntity[]>([])
const tableStoreId = "servers"

const step1Form = ref<InstanceType<typeof Form> | null>(null)
const step2Form = ref<InstanceType<typeof Form> | null>(null)

const createServerPopup = ref<InstanceType<typeof Popup> | null>(null)
const createServerStep = ref(1)

const selectedGame = ref<number | undefined>(undefined)
const selectedLoader = ref<number | undefined>(undefined)
const selectedVersion = ref<string | undefined>(undefined)
const serverName = ref<string>("")

const confirmPopup = ref<InstanceType<typeof ConfirmPopup> | null>(null)

const statusMessages: Record<ServerStatusEnum, string> = {
  [ServerStatusEnum.PENDING]: "Server is in queue",
  [ServerStatusEnum.PROCESSING]: "Server is being created",
  [ServerStatusEnum.FAILED]: "Error while creating server",
  [ServerStatusEnum.CREATED]: ""
}

const columns: TableColumn[] = [
  {
    field: "game",
    type: "icon-text",
    params: {
      label: {
        value: "Game",
        highlighted: true
      },
      sorting: {
        sortable: true,
        default: false,
        field: "game_id"
      },
      iconField: "gameIcon",
      iconSize: "medium"
    }
  },
  {
    field: "version",
    type: "tag",
    params: {
      label: {
        value: "Version"
      },
      sorting: {
        sortable: true,
        default: false,
        field: "version"
      },
      color: "green"
    }
  },
  {
    field: "loader",
    type: "tag",
    params: {
      label: {
        value: "Loader"
      },
      sorting: {
        sortable: true,
        default: false,
        field: "loader_id"
      },
      color: "yellow"
    }
  },
  {
    field: "name",
    type: "text",
    params: {
      label: {
        value: "Name",
        highlighted: false
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
 * Fetches paginated servers list from the API using current page and sort state from the store.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchServers(): Promise<void> {
  const sort = tableStore.getSort(tableStoreId)
  const page = tableStore.getPage(tableStoreId)
  const search = tableStore.getSearch(tableStoreId)

  try {
    pageData.value = await httpServersApiService.getPage({
      page: page,
      search: search || undefined,
      sort_field: sort?.field as ServersPageRequest["sort_field"],
      sort_direction: sort?.direction
    })
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to fetch servers"
    })
    pageData.value = null;
  }
}

/**
 * Fetches all games from the API.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchGames(): Promise<void> {
  try {
    let currentPage = 1
    let totalPages = 1
    const allGames: GameEntity[] = []

    do {
      const page = await httpGamesApiService.getPage({
        page: currentPage,
        limit: 100
      })

      allGames.push(...page.games)
      totalPages = page.pages
      currentPage++
    } while (currentPage <= totalPages)

    games.value = allGames
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to fetch games"
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
  fetchServers()
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
  fetchServers()
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
  fetchServers()
}

/**
 * Opens the confirm popup before deleting a server.
 *
 * Parameters:
 * - serverId: ID of the server to delete.
 *
 * Returns:
 * - void.
 */
function handleDeleteServer(serverId: number): void {
  confirmPopup.value?.open(() => deleteServer(serverId))
}

/**
 * Deletes a server by ID and refreshes the table.
 *
 * Parameters:
 * - serverId: ID of the server to delete.
 *
 * Returns:
 * - Promise<void>.
 */
async function deleteServer(serverId: number): Promise<void> {
  try {
    await httpServersApiService.deleteOne(serverId)

    notify({
      type: "success",
      text: "Server deleted successfully"
    })

    fetchServers()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to delete server"
    })
  }
}

/**
 * Opens the confirm popup before deleting selected servers.
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
 * Deletes all selected servers and refreshes the table.
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
    await httpServersApiService.deleteMany(selected)

    notify({
      type: "success",
      text: "Servers deleted successfully"
    })

    tableStore.clearSelected(tableStoreId)
    fetchServers()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to delete selected servers"
    })
  }
}

/**
 * Resets the create server popup form state to its initial values.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function resetCreateServerForm(): void {
  createServerStep.value = 1
  selectedGame.value = undefined
  selectedLoader.value = undefined
  selectedVersion.value = undefined
  serverName.value = ""
}

/**
 * Creates a new server from the popup form data.
 * On success resets the form state, closes the popup, and refreshes the table.
 *
 * Parameters:
 * - close: Popup close callback.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleCreateServer(close: () => void): Promise<void> {
  try {
    await httpServersApiService.createOne({
      name: serverName.value,
      game_id: selectedGame.value as number,
      loader_id: selectedLoader.value as number,
      version: selectedVersion.value!
    })

    notify({
      type: "success",
      text: "Server added to queue"
    })

    close()
    resetCreateServerForm()
    fetchServers()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? "Failed to create server"
    })
  }
}

/**
 * Opens the create server popup and resets the step to 1.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function openCreateServer(): void {
  createServerStep.value = 1
  createServerPopup.value?.open()
}

/**
 * Maps servers response to flat row objects for the table.
 * Display name and icon are resolved from GameModules by game name,
 * loader display name is resolved from the corresponding game module's loaders map.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Array<Record<string, any>>: Flat row objects with primitive values, or empty array if no data.
 */
const rows = computed((): Array<Record<string, any>> =>
  pageData.value?.servers.map(server => {
    const gameModule = GameModules[server.game.name]
    const loaderModule = gameModule?.loaders[server.loader.name]

    return {
      id: server.id,
      game: gameModule?.displayName,
      gameIcon: gameModule?.icon,
      gameName: server.game.name,
      version: server.version,
      loader: loaderModule?.displayName,
      name: server.name,
      status: server.status,
      created_at: localeHelper.formatDateTime(server.created_at)
    }
  }) ?? [])

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
 * Returns the selected game entity based on current selectedGame value.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - GameEntity | undefined: The matched game entity, or undefined if no game is selected.
 */
const selectedGameEntity = computed((): GameEntity | undefined =>
  games.value.find(game => game.id === selectedGame.value)
)

/**
 * Returns the GameModules entry for the currently selected game.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - GameModules entry | undefined: The matched module, or undefined if no game is selected.
 */
const selectedGameModule = computed(() =>
  selectedGameEntity.value
    ? GameModules[selectedGameEntity.value.name]
    : undefined
)

/**
 * Maps games to radio button options.
 * Display name, description and icon are resolved from GameModules by game name.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - RadioOption[]: List of radio options derived from the games list.
 */
const gameOptions = computed((): RadioOption[] =>
  games.value.map(game => {
    const gameModule = GameModules[game.name]!

    return {
      value: game.id,
      title: gameModule.displayName,
      description: gameModule.description,
      icon: gameModule.icon,
      sort_number: gameModule.sort_number
    }
  }).sort(
    (a, b) => a.sort_number - b.sort_number
  )
)

/**
 * Maps loaders of the selected game to select options.
 * Loader display name is resolved from GameModules by game and loader name.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - SelectOption[]: List of select options derived from the selected game's loaders, or empty array if no game is selected.
 */
const loaderOptions = computed((): SelectOption[] => {
  const game = selectedGameEntity.value
  if (!game) return []

  const gameModule = GameModules[game.name]!

  return game.loaders.map(loader => {
    const loaderModule = gameModule.loaders[loader.name]!

    return {
      value: loader.id,
      label: loaderModule.displayName
    }
  })
})

/**
 * Maps versions of the selected loader to select options.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - SelectOption[]: List of select options derived from the selected loader's versions, or empty array if no loader is selected.
 */
const versionOptions = computed((): SelectOption[] => {
  const loader = selectedGameEntity.value?.loaders.find(loader => loader.id === selectedLoader.value)
  return loader?.versions.map(version => ({
    value: version,
    label: version
  })) ?? []
})

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
  userStore.hasPermission(PermissionsEnum.SERVERS_VIEW)
)

/**
 * Checks whether the current user has access to create servers.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServersCreateAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.SERVERS_CREATE)
)

/**
 * Checks whether the current user has access to delete servers.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServersDeleteAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.SERVERS_DELETE)
)

/**
 * Checks whether the current user has access to view server.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServerViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.SERVER_VIEW)
)

onMounted(() => {
  if (hasServersViewAccess.value) {
    fetchServers()
  }

  if (hasServersCreateAccess.value) {
    fetchGames()
  }
})

onUnmounted(() => {
  tableStore.clear(tableStoreId)
})
</script>

<style scoped lang="scss">
.servers {
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
  .servers {
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
.create-server-popup {
  .selected-game {
    display: flex;
    align-items: center;
    gap: $space-xl;
    padding: $space-xl;
    background-color: $color-block-alt;
    border-radius: 12px;

    .game-icon {
      width: 40px;
      height: 40px;
      object-fit: contain;
      flex-shrink: 0;
    }

    .game-info {
      display: flex;
      flex-direction: column;
      gap: $space-sm;

      h3 {
        font-size: $font-md;
        font-weight: 600;
        color: $color-title;
      }

      p {
        font-size: $font-sm;
        font-weight: 600;
        color: $color-text;
        line-height: unset;
      }
    }
  }

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
  .create-server-popup {
    .selected-game {
      gap: $space-lg;
      padding: $space-lg;
    }

    .actions {
      gap: $space-md;
    }
  }
}
</style>