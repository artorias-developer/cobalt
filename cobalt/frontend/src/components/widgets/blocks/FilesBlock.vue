<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block class="files">
    <div class="heading">
      <Header
        :icon="icon"
        :icon-color="iconColor"
        :title="title ?? $t('servers.server.files.title')"
        :description="description ?? $t('servers.server.files.description')"
        :size="size"
        :icon-filled="filled"
      />
      <Search
        v-if="mode !== 'empty'"
        :table-id="tableStoreId"
        @search-change="handleSearchChange"
      />
    </div>
    <Message
      v-if="mode === 'empty'"
      :icon="listIcon"
      :text="$t('common.noData')"
    />
    <template v-else>
      <template v-if="!isEditing">
        <Table
          :access-denied="!hasServerFilesViewAccess"
          :table-id="tableStoreId"
          :columns="columns"
          :rows="rows"
          :with-actions="true"
          @sort-change="handleSortChange"
        >
          <template #tableRowActions="{ row }">
            <ActionsButton
              v-if="row.id !== '__back__'"
              :items="actionsMenuItems(row)"
            />
          </template>
          <template #footerActions>
            <template v-if="hasSelected">
              <SolidButton
                v-if="hasServerFilesDownloadAccess"
                type="button"
                :text="$t('common.download')"
                color="gray"
                name="files-download"
                @click="handleDownloadSelected"
              />
              <SolidButton
                v-if="hasServerFilesUpdateAccess"
                type="button"
                :text="$t('common.duplicate')"
                color="gray"
                name="files-duplicate"
                @click="handleDuplicateSelected"
              />
              <SolidButton
                v-if="hasServerFilesUpdateAccess"
                type="button"
                :text="$t('common.move')"
                color="gray"
                name="files-move-popup"
                @click="openMovePopup(selectedPaths)"
              />
              <SolidButton
                v-if="hasServerFilesUpdateAccess"
                type="button"
                :text="$t('common.delete')"
                color="gray"
                name="files-delete-popup"
                @click="handleDeleteSelected"
              />
            </template>
            <template v-else>
              <SolidButton
                v-if="hasServerFilesUpdateAccess"
                type="button"
                :text="$t('common.create')"
                color="gray"
                name="file-create-popup"
                @click="openCreatePopup"
              />
              <SolidButton
                v-if="hasServerFilesUpdateAccess"
                type="button"
                :text="$t('common.upload')"
                color="gray"
                name="file-upload-popup"
                @click="openUploadPopup"
              />
              <SolidButton
                v-if="hasServerFilesViewAccess"
                type="button"
                :text="$t('common.reload')"
                color="gray"
                name="file-reload-popup"
                @click="handleReload"
              />
            </template>
          </template>
          <template #footerCounter>
            <Counter
              :files="listData?.total_files ?? 0"
              :folders="listData?.total_directories ?? 0"
            />
          </template>
        </Table>
      </template>
      <div v-else class="editor">
        <div class="header">
          <span class="filename">{{ openedFile?.name }}</span>
        </div>
        <FileEditor
          ref="fileEditorRef"
          :model-value="openedFile?.content ?? ''"
          :language="getEditorLanguage(openedFile?.name ?? '')"
        />
        <div class="footer">
          <SolidButton
            type="button"
            v-if="hasServerFilesUpdateAccess"
            :text="$t('common.save')"
            color="gray"
            name="file-save"
            @click="handleSaveContent"
          />
          <SolidButton
            type="button"
            :text="$t('common.close')"
            color="gray"
            name="file-close"
            @click="closeEditor"
          />
        </div>
      </div>
    </template>
  </Block>
  <Popup ref="createPopup" class="create-file-popup">
    <template #content="{ close }">
      <Header
        :icon="filesIcon"
        icon-color="blue"
        :title="$t('servers.server.files.popup.create.title')"
        :description="$t('servers.server.files.popup.create.description')"
        size="large"
        :icon-filled="true"
      />
      <Form
        ref="createForm"
        class="form"
        :on-submit="() => createForm?.validate() && handleCreate(close)"
      >
        <Input
          v-model="createName"
          :validationName="$t('servers.server.files.popup.name.label')"
          :label="$t('servers.server.files.popup.name.label')"
          :placeholder="$t('servers.server.files.popup.create.name.placeholder')"
          name="file-name"
          :required="true"
        />
        <Select
          v-model="createType"
          :options="createTypeOptions"
          :validationName="$t('servers.server.files.popup.type.label')"
          :label="$t('servers.server.files.popup.type.label')"
          :placeholder="$t('servers.server.files.popup.type.placeholder')"
          name="file-type"
          :required="true"
        />
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
          name="file-create"
          @click="createForm?.validate() && handleCreate(close)"
        />
      </div>
    </template>
  </Popup>
  <Popup ref="renamePopup" class="rename-file-popup">
    <template #content="{ close }">
      <Header
        :icon="editIcon"
        icon-color="blue"
        :title="$t('servers.server.files.popup.rename.title')"
        :description="$t('servers.server.files.popup.rename.description')"
        size="large"
        :icon-filled="true"
      />
      <Form
        ref="renameForm"
        class="form"
        :on-submit="() => renameForm?.validate() && handleRename(close)"
      >
        <Input
          v-model="renameName"
          :validationName="$t('servers.server.files.popup.rename.name.label')"
          :label="$t('servers.server.files.popup.rename.name.label')"
          :placeholder="$t('servers.server.files.popup.rename.name.placeholder')"
          name="file-name"
          :required="true"
        />
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
          :text="$t('servers.server.files.popup.rename.submit')"
          color="blue"
          name="file-rename"
          @click="renameForm?.validate() && handleRename(close)"
        />
      </div>
    </template>
  </Popup>
  <Popup ref="movePopup" class="move-file-popup">
    <template #content="{ close }">
      <Header
        :icon="moveIcon"
        icon-color="blue"
        :title="$t('servers.server.files.popup.move.title')"
        :description="$t('servers.server.files.popup.move.description')"
        size="large"
        :icon-filled="true"
      />
      <Form
        ref="moveForm"
        class="form"
        :on-submit="() => moveForm?.validate() && handleMove(close)"
      >
        <Input
          v-model="moveDestination"
          :validationName="$t('servers.server.files.popup.move.destination.label')"
          :label="$t('servers.server.files.popup.move.destination.label')"
          :placeholder="$t('servers.server.files.popup.move.destination.placeholder')"
          name="file-move-destination"
          :required="true"
        />
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
          :text="$t('common.move')"
          color="blue"
          name="file-move"
          @click="moveForm?.validate() && handleMove(close)"
        />
      </div>
    </template>
  </Popup>
  <Popup ref="uploadPopup" class="upload-file-popup">
    <template #content="{ close }">
      <Header
        :icon="filesIcon"
        icon-color="blue"
        :title="$t('servers.server.files.popup.upload.title')"
        :description="$t('servers.server.files.popup.upload.description')"
        size="large"
        :icon-filled="true"
      />
      <Form
        ref="uploadForm"
        class="form"
        :on-submit="() => uploadForm?.validate() && handleUpload(close)"
      >
        <FileUpload
          v-model="uploadFiles"
          :validationName="$t('servers.server.files.popup.upload.label')"
          :upload-progress="uploadProgress"
          :required="true"
        />
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
          :text="$t('common.upload')"
          color="blue"
          :disabled="isUploadFormLoading"
          @click="uploadForm?.validate() && handleUpload(close)"
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

import { HTTP_FILES_API_SERVICE_KEY, LOCALE_HELPER_KEY } from "@/utils"
import { useTableStore, useUserStore } from "@/stores"
import { PermissionsEnum } from "@/types"
import type {
  FileContentEntity,
  FilesListEntity,
  ActionsMenuButton,
  BlockHeaderSize,
  Color,
  FileType,
  FileTypeEntry,
  SelectOption,
  TableColumn,
  ServerBlockMode
} from "@/types"

import Block from "@/components/ui/Block.vue"
import Header from "@/components/ui/Header.vue"
import Popup from "@/components/ui/Popup.vue"
import Input from "@/components/ui/forms/Input.vue"
import Select from "@/components/ui/forms/Select.vue"
import FileUpload from "@/components/ui/forms/FileUpload.vue"
import SolidButton from "@/components/ui/forms/buttons/SolidButton.vue"
import ActionsButton from "@/components/ui/forms/buttons/ActionsButton.vue"
import Table from "@/components/ui/tables/Table.vue"
import Search from "@/components/ui/tables/Search.vue"
import Form from "@/components/ui/forms/Form.vue"
import Counter from "@/components/ui/editors/Counter.vue"
import FileEditor from "@/components/ui/editors/FileEditor.vue"
import Message from "@/components/ui/Message.vue"
import ConfirmPopup from "@/components/widgets/popups/ConfirmPopup.vue"
import filesIcon from "@/assets/images/svg/files.svg?raw"
import trashIcon from "@/assets/images/svg/trash.svg?raw"
import editIcon from "@/assets/images/svg/edit.svg?raw"
import moveIcon from "@/assets/images/svg/move.svg?raw"
import openIcon from "@/assets/images/svg/book.svg?raw"
import downloadIcon from "@/assets/images/svg/download.svg?raw"
import duplicateIcon from "@/assets/images/svg/copy.svg?raw"
import listIcon from "@/assets/images/svg/clipboard-blank.svg?raw"

import iconFolder from "@/assets/images/svg/files/folder.svg"
import iconDefault from "@/assets/images/svg/files/document.svg"
import iconJson from "@/assets/images/svg/files/json.svg"
import iconXml from "@/assets/images/svg/files/xml.svg"
import iconYaml from "@/assets/images/svg/files/yaml.svg"
import iconBash from "@/assets/images/svg/files/powershell.svg"
import iconLog from "@/assets/images/svg/files/log.svg"
import iconSettings from "@/assets/images/svg/files/settings.svg"
import iconZip from "@/assets/images/svg/files/zip.svg"
import iconDll from "@/assets/images/svg/files/dll.svg"
import iconExe from "@/assets/images/svg/files/exe.svg"
import iconImage from "@/assets/images/svg/files/image.svg"
import iconLua from "@/assets/images/svg/files/lua.svg"
import iconJar from "@/assets/images/svg/files/jar.svg"

const props = withDefaults(defineProps<{
  mode: ServerBlockMode
  serverId?: number
  icon?: string
  iconColor?: Color
  title?: string
  description?: string
  size?: BlockHeaderSize
  filled?: boolean
}>(), {
  serverId: undefined,
  icon: filesIcon,
  iconColor: "blue",
  size: "large",
  filled: true,
})

const localeHelper = inject(LOCALE_HELPER_KEY)!
const httpFilesApiService = inject(HTTP_FILES_API_SERVICE_KEY)!
const tableStore = useTableStore()
const userStore = useUserStore()
const { notify } = useNotification()
const { t } = useI18n()

const tableStoreId = "files"
const listData = ref<FilesListEntity | null>(null)
const currentPath = ref<string>("/")
const pathHistory = ref<string[]>([])

const isEditing = ref<boolean>(false)
const openedFile = ref<FileContentEntity | null>(null)
const fileEditorRef = ref<InstanceType<typeof FileEditor> | null>(null)

const createPopup = ref<InstanceType<typeof Popup> | null>(null)
const createForm = ref<InstanceType<typeof Form> | null>(null)
const createName = ref<string>("")
const createType = ref<FileType>("file")

const renamePopup = ref<InstanceType<typeof Popup> | null>(null)
const renameForm = ref<InstanceType<typeof Form> | null>(null)
const renameName = ref<string>("")
const renameTargetPath = ref<string>("")

const movePopup = ref<InstanceType<typeof Popup> | null>(null)
const moveForm = ref<InstanceType<typeof Form> | null>(null)
const moveDestination = ref<string>("")
const movePaths = ref<string[]>([])

const uploadPopup = ref<InstanceType<typeof Popup> | null>(null)
const uploadForm = ref<InstanceType<typeof Form> | null>(null)
const uploadFiles = ref<File[]>([])
const uploadProgress = ref<number | null>(null)
const isUploadFormLoading = ref<boolean>(false)

const confirmPopup = ref<InstanceType<typeof ConfirmPopup> | null>(null)

const columns = computed((): TableColumn[] => [
  {
    field: "name",
    type: "icon-text",
    params: {
      label: {
        value: t("servers.server.files.columns.name"),
        highlighted: true
      },
      iconField: "icon",
      iconSize: "small",
      action: (row) => handleOpen(row)
    }
  },
  {
    field: "type_label",
    type: "text",
    params: {
      label: {
        value: t("servers.server.files.columns.type"),
        highlighted: false
      }
    }
  },
  {
    field: "size_label",
    type: "text",
    params: {
      label: {
        value: t("servers.server.files.columns.size"),
        highlighted: false
      }
    }
  },
  {
    field: "modified_at",
    type: "text",
    params: {
      label: {
        value: t("servers.server.files.columns.modifiedAt"),
        highlighted: false
      }
    }
  }
])

const createTypeOptions = computed((): SelectOption[] => [
  {
    value: "file",
    label: t("servers.server.files.types.file")
  },
  {
    value: "directory",
    label: t("servers.server.files.types.directory")
  }
])

const FILE_TYPE_MAP: Record<string, FileTypeEntry> = {
  "__directory__": { icon: iconFolder },
  "__default__": { icon: iconDefault, language: "plaintext" },
  "json": { icon: iconJson, language: "json" },
  "xml": { icon: iconXml, language: "xml" },
  "yml": { icon: iconYaml, language: "yaml" },
  "yaml": { icon: iconYaml, language: "yaml" },
  "sh": { icon: iconBash, language: "shell" },
  "bat": { icon: iconBash, language: "shell" },
  "log": { icon: iconLog, language: "plaintext" },
  "cfg": { icon: iconSettings, language: "properties" },
  "ini": { icon: iconSettings, language: "properties" },
  "properties": { icon: iconSettings, language: "properties" },
  "zip": { icon: iconZip, language: "plaintext" },
  "dll": { icon: iconDll, language: "plaintext" },
  "exe": { icon: iconExe, language: "plaintext" },
  "png": { icon: iconImage, language: "plaintext" },
  "jpg": { icon: iconImage, language: "plaintext" },
  "jpeg": { icon: iconImage, language: "plaintext" },
  "ico": { icon: iconImage, language: "plaintext" },
  "lua": { icon: iconLua, language: "lua" },
  "jar": { icon: iconJar, language: "lua" }
}

/**
 * Returns the list of visible action items for a given row based on user permissions.
 *
 * Parameters:
 * - row: Table row data object.
 *
 * Returns:
 * - Array of menu item descriptors with label, icon, danger flag, and action callback.
 */
function actionsMenuItems(row: Record<string, any>): Array<ActionsMenuButton> {
  return [
    {
      label: t("servers.server.files.actions.open"),
      name: "file-open",
      icon: openIcon,
      show: hasServerFilesViewAccess,
      action: () => handleOpen(row),
    },
    {
      label: t("servers.server.files.actions.rename"),
      name: "file-rename-popup",
      icon: editIcon,
      show: hasServerFilesUpdateAccess,
      action: () => openRenamePopup(row),
    },
    {
      label: t("servers.server.files.actions.download"),
      name: "file-download",
      icon: downloadIcon,
      show: hasServerFilesDownloadAccess,
      action: () => handleDownloadOne(row),
    },
    {
      label: t("servers.server.files.actions.duplicate"),
      name: "file-duplicate",
      icon: duplicateIcon,
      show: hasServerFilesUpdateAccess,
      action: () => handleDuplicateOne(row),
    },
    {
      label: t("servers.server.files.actions.move"),
      name: "file-move-popup",
      icon: moveIcon,
      show: hasServerFilesUpdateAccess,
      action: () => openMovePopup([row.path]),
    },
    {
      label: t("servers.server.files.actions.extract"),
      name: "file-extract",
      icon: filesIcon,
      show: hasServerFilesUpdateAccess.value && row.format === "zip",
      action: () => handleExtract(row.path),
    },
    {
      label: t("servers.server.files.actions.delete"),
      name: "file-delete-popup",
      icon: trashIcon,
      danger: true,
      show: hasServerFilesUpdateAccess,
      action: () => handleDeleteOne(row.path),
    },
  ].filter(item => item.show)
}

/**
 * Resolves the `FileTypeEntry` for a given file or directory.
 *
 * Parameters:
 * - name: File or directory name.
 * - type: FileType object.
 *
 * Returns:
 * - FileTypeEntry: Resolved icon and optional language.
 */
function resolveFileType(name: string, type: FileType): FileTypeEntry {
  if (type === "directory") return FILE_TYPE_MAP["__directory__"] as FileTypeEntry
  const lower = name.toLowerCase()
  if (FILE_TYPE_MAP[lower]) return FILE_TYPE_MAP[lower]
  const ext = lower.includes(".") ? lower.split(".").pop()! : ""
  if (ext && FILE_TYPE_MAP[ext]) return FILE_TYPE_MAP[ext]
  return FILE_TYPE_MAP["__default__"] as FileTypeEntry
}

/**
 * Returns the raw SVG icon string for a given file or directory.
 *
 * Parameters:
 * - name: File or directory name.
 * - type: FileType object.
 *
 * Returns:
 * - string: Raw SVG string.
 */
function getFileIcon(name: string, type: FileType): string {
  return resolveFileType(name, type).icon
}

/**
 * Resolves the editor language identifier for a given file name.
 *
 * Parameters:
 * - name: File name including extension.
 *
 * Returns:
 * - string: Language id.
 */
function getEditorLanguage(name: string): string {
  return resolveFileType(name, "file").language ?? "plaintext"
}

/**
 * Fetches the file list for the current path from the API and applies
 * any active search filter from the table store.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchFiles(): Promise<void> {
  const search = tableStore.getSearch(tableStoreId)

  try {
    listData.value = await httpFilesApiService.getList(props.serverId!, {
      path: currentPath.value,
    })

    if (search) {
      const searchLower = search.toLowerCase()
      listData.value = {
        ...listData.value,
        files: listData.value.files.filter(
          file => file.name.toLowerCase().includes(searchLower)
        ),
      }
    }
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.files.fetch.error"),
    })
    listData.value = null
  }
}

/**
 * Pushes the current path onto the history stack and navigates into a
 * subdirectory, then refreshes the file list.
 *
 * Parameters:
 * - path: Absolute path of the directory to navigate into.
 *
 * Returns:
 * - void.
 */
function navigateInto(path: string): void {
  pathHistory.value.push(currentPath.value)
  currentPath.value = path
  tableStore.clearSelected(tableStoreId)
  fetchFiles()
}

/**
 * Pops the most recent path from the history stack and navigates back to
 * it, then refreshes the file list.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function navigateBack(): void {
  const prev = pathHistory.value.pop()
  if (prev !== undefined) {
    currentPath.value = prev
    tableStore.clearSelected(tableStoreId)
    fetchFiles()
  }
}

/**
 * Handles a row open action: navigates back if the back row is clicked,
 * navigates into a directory, or opens a file in the editor.
 *
 * Parameters:
 * - row: Table row data object.
 *
 * Returns:
 * - void.
 */
function handleOpen(row: Record<string, any>): void {
  if (row.id === "__back__") {
    navigateBack()
  } else if (row.type === "directory") {
    navigateInto(row.path)
  } else {
    openFile(row)
  }
}

/**
 * Fetches file content from the API and opens it in the editor.
 *
 * Parameters:
 * - row: Table row data object containing at least a `path` property.
 *
 * Returns:
 * - Promise<void>.
 */
async function openFile(row: Record<string, any>): Promise<void> {
  try {
    openedFile.value = await httpFilesApiService.getContent(props.serverId!, {
      path: row.path
    })
    isEditing.value = true
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.files.open.error"),
    })
  }
}

/**
 * Persists the current editor content back to the server,
 * then closes the editor on success.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleSaveContent(): Promise<void> {
  if (!openedFile.value) return

  try {
    await httpFilesApiService.saveContent(props.serverId!, {
      path: openedFile.value.path,
      content: fileEditorRef.value?.getValue() ?? "",
    })
    notify({
      type: "success",
      text: t("servers.server.files.save.success")
    })
    closeEditor()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.files.save.error"),
    })
  }
}

/**
 * Closes the editor and clears the opened file reference.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function closeEditor(): void {
  isEditing.value = false
  openedFile.value = null
}

/**
 * Triggers a download for a single table row.
 *
 * Parameters:
 * - row: Table row data object containing at least a `path` property.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleDownloadOne(row: Record<string, any>): Promise<void> {
  await downloadPaths([row.path])
}

/**
 * Triggers a download for all currently selected rows.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleDownloadSelected(): Promise<void> {
  await downloadPaths(selectedPaths.value)
}

/**
 * Requests a ZIP archive for the given paths from the API and triggers a
 * browser download.
 *
 * Parameters:
 * - paths: Array of absolute file/directory paths to include in the archive.
 *
 * Returns:
 * - Promise<void>.
 */
async function downloadPaths(paths: string[]): Promise<void> {
  try {
    const blob = await httpFilesApiService.download(props.serverId!, { paths })
    const url = URL.createObjectURL(blob)
    const element = document.createElement("a")
    element.href = url
    element.download = `cobalt_server_${props.serverId}_files.zip`
    element.click()
    URL.revokeObjectURL(url)
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.files.download.error"),
    })
  }
}

/**
 * Duplicates a single table row.
 *
 * Parameters:
 * - row: Table row data object containing at least a `path` property.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleDuplicateOne(row: Record<string, any>): Promise<void> {
  await duplicatePaths([row.path])
}

/**
 * Duplicates all currently selected rows.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleDuplicateSelected(): Promise<void> {
  await duplicatePaths(selectedPaths.value)
}

/**
 * Sends a duplicate request for the given paths and refreshes the file list.
 *
 * Parameters:
 * - paths: Array of absolute paths to duplicate.
 *
 * Returns:
 * - Promise<void>.
 */
async function duplicatePaths(paths: string[]): Promise<void> {
  try {
    await httpFilesApiService.duplicate(props.serverId!, { paths })
    notify({
      type: "success",
      text: t("servers.server.files.duplicate.success")
    })
    fetchFiles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.files.duplicate.error"),
    })
  }
}

/**
 * Opens the confirm popup before deleting a single file or directory.
 *
 * Parameters:
 * - path: Absolute path of the entry to delete.
 *
 * Returns:
 * - void.
 */
function handleDeleteOne(path: string): void {
  confirmPopup.value?.open(() => deletePaths([path]))
}

/**
 * Opens the confirm popup before deleting all currently selected rows.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleDeleteSelected(): void {
  confirmPopup.value?.open(async () => {
    await deletePaths(selectedPaths.value)
    tableStore.clearSelected(tableStoreId)
  })
}

/**
 * Sends a delete request for the given paths and refreshes the file list.
 *
 * Parameters:
 * - paths: Array of absolute paths to delete.
 *
 * Returns:
 * - Promise<void>.
 */
async function deletePaths(paths: string[]): Promise<void> {
  try {
    await httpFilesApiService.delete(props.serverId!, { paths })
    notify({
      type: "success",
      text: t("servers.server.files.delete.success")
    })
    fetchFiles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.files.delete.error"),
    })
  }
}

/**
 * Resets the create-popup form fields and opens the popup.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function openCreatePopup(): void {
  createName.value = ""
  createType.value = "file"
  createPopup.value?.open()
}

/**
 * Creates a new file or directory at the current path using the values from
 * the create form, then closes the popup and refreshes the file list.
 *
 * Parameters:
 * - close: Callback that closes the create popup.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleCreate(close: () => void): Promise<void> {
  const path = currentPath.value.replace(/\/$/, "") + "/" + createName.value

  try {
    await httpFilesApiService.create(props.serverId!, { path, type: createType.value })
    notify({
      type: "success",
      text: t("servers.server.files.create.success")
    })
    close()
    fetchFiles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.files.create.error"),
    })
  }
}

/**
 * Re-fetches the file list for the current path and shows a success notification.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleReload(): Promise<void> {
  await fetchFiles()

  if (listData.value) {
    notify({
      type: "success",
      text: t("servers.server.files.reload.success")
    })
  }
}

/**
 * Populates the rename form with the current name of a row and opens the
 * rename popup.
 *
 * Parameters:
 * - row: Table row data object containing `path` and `name` properties.
 *
 * Returns:
 * - void.
 */
function openRenamePopup(row: Record<string, any>): void {
  renameTargetPath.value = row.path
  renameName.value = row.name
  renamePopup.value?.open()
}

/**
 * Sends a rename request for the target path using the value from the rename
 * form, then closes the popup and refreshes the file list.
 *
 * Parameters:
 * - close: Callback that closes the rename popup.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleRename(close: () => void): Promise<void> {
  try {
    await httpFilesApiService.rename(props.serverId!, {
      path: renameTargetPath.value,
      name: renameName.value,
    })
    notify({
      type: "success",
      text: t("servers.server.files.rename.success")
    })
    close()
    fetchFiles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.files.rename.error"),
    })
  }
}

/**
 * Stores the paths to move and opens the move popup with a blank destination.
 *
 * Parameters:
 * - paths: Array of absolute paths that will be moved.
 *
 * Returns:
 * - void.
 */
function openMovePopup(paths: string[]): void {
  movePaths.value = paths
  moveDestination.value = ""
  movePopup.value?.open()
}

/**
 * Sends a move request for the stored paths using the destination from the
 * move form, then clears the selection, closes the popup, and refreshes the
 * file list.
 *
 * Parameters:
 * - close: Callback that closes the move popup.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleMove(close: () => void): Promise<void> {
  try {
    await httpFilesApiService.move(props.serverId!, {
      paths: movePaths.value,
      destination_path: moveDestination.value,
    })
    notify({
      type: "success",
      text: t("servers.server.files.move.success")
    })
    tableStore.clearSelected(tableStoreId)
    close()
    fetchFiles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.files.move.error"),
    })
  }
}

/**
 * Extracts a ZIP archive in place.
 *
 * Parameters:
 * - path: Absolute path to the ZIP archive.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleExtract(path: string): Promise<void> {
  try {
    await httpFilesApiService.extract(props.serverId!, { path })
    notify({
      type: "success",
      text: t("servers.server.files.extract.success")
    })
    fetchFiles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.files.extract.error"),
    })
  }
}

/**
 * Resets the upload popup state and opens the popup.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function openUploadPopup(): void {
  uploadFiles.value = []
  uploadPopup.value?.open()
}

/**
 * Uploads the selected files to the current directory path, then closes
 * the popup and refreshes the file list on success.
 *
 * Parameters:
 * - close: Callback that closes the upload popup.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleUpload(close: () => void): Promise<void> {
  if (!uploadFiles.value.length) return

  isUploadFormLoading.value = true
  uploadProgress.value = 0

  try {
    await httpFilesApiService.upload(props.serverId!, {
      path: currentPath.value,
      files: uploadFiles.value,
    }, (percent) => {
      uploadProgress.value = percent
    })
    notify({
      type: "success",
      text: t("servers.server.files.upload.success")
    })
    close()
    fetchFiles()
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("servers.server.files.upload.error"),
    })
  } finally {
    uploadProgress.value = null
    isUploadFormLoading.value = false
  }
}

/**
 * Re-fetches the file list when the search input changes.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleSearchChange(): void {
  fetchFiles()
}

/**
 * Re-fetches the file list when a column sort change is emitted.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleSortChange(): void {
  fetchFiles()
}

/**
 * Formats a byte count into a human-readable size string.
 *
 * Parameters:
 * - bytes: Number of bytes, or null for directories.
 *
 * Returns:
 * - string: Formatted size string (e.g. "1.23 MB").
 */
function formatSize(bytes: number | null): string {
  if (bytes === null) return "-"
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(2)} MB`
  return `${(bytes / 1024 / 1024 / 1024).toFixed(2)} GB`
}

/**
 * Returns the computed list of table rows for the current directory.
 * Prepends a ".." back-navigation row when inside a subdirectory.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Array<Record<string, any>>: List of rows ready for the Table component.
 */
const rows = computed((): Array<Record<string, any>> => {
  const fileRows = listData.value?.files.map(file => ({
    id: file.path,
    name: file.name,
    path: file.path,
    type: file.type,
    type_label: file.type === "directory"
      ? t("servers.server.files.types.directory")
      : file.format
        ? file.format.toUpperCase()
        : t("servers.server.files.types.file"),
    format: file.format,
    icon: getFileIcon(file.name, file.type),
    size_label: formatSize(file.size),
    modified_at: localeHelper.formatDateTime(file.modified_at),
  })) ?? []

  if (pathHistory.value.length === 0) return fileRows

  return [
    {
      id: "__back__",
      name: "..",
      path: "",
      type: "directory",
      type_label: "",
      format: "",
      icon: getFileIcon("", "directory"),
      size_label: "",
      modified_at: "",
    },
    ...fileRows,
  ]
})

/**
 * Returns true if at least one row is currently selected.
 * Subscribes to selection version to stay reactive on external changes.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if any row is selected, `false` otherwise.
 */
const hasSelected = computed((): boolean => {
  void tableStore.getSelectionVersion(tableStoreId)
  return tableStore.getSelected(tableStoreId).size > 0
})

/**
 * Returns the list of file paths for all currently selected rows.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - string[]: Array of absolute paths of selected rows.
 */
const selectedPaths = computed((): string[] =>
  [...tableStore.getSelected(tableStoreId)] as string[]
)

/**
 * Checks whether the current user has access to view server files.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServerFilesViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.SERVER_FILES_VIEW)
)

/**
 * Checks whether the current user has access to update server files.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServerFilesUpdateAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.SERVER_FILES_UPDATE)
)

/**
 * Checks whether the current user has access to download server files.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasServerFilesDownloadAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.SERVER_FILES_DOWNLOAD)
)

onMounted(() => {
  if (props.mode !== "empty" && hasServerFilesViewAccess.value) {
    fetchFiles()
  }
})

onUnmounted(() => {
  tableStore.clear(tableStoreId)
})
</script>

<style scoped lang="scss">
.files {
  min-height: 500px;
  display: flex;
  flex-direction: column;

  .heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: $space-xl;
    padding: $space-xl;
  }

  :deep(.table) {
    .footer {
      .counter {
        width: unset;
        flex: 1;
      }
    }
  }

  .editor {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;

    .header {
      display: flex;
      align-items: center;
      padding: $space-md $space-xl;
      background-color: $color-block-alt;

      .filename {
        font-size: $font-sm;
        font-weight: 600;
        color: $color-text;
      }
    }

    :deep(.codemirror-editor) {
      flex: 1;
      min-height: 0;
    }

    .footer {
      display: flex;
      gap: $space-md;
      padding: $space-xl;
      border-top: 1px solid $color-border;
    }
  }

  .message {
    height: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .files {
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

    :deep(.table) {
      .footer {
        .actions {
          width: 100%;
        }

        .counter {
          width: 100%;
          flex: unset;
          text-align: center;
        }
      }
    }

    .editor {
      .header {
        padding: $space-md $space-lg;
      }

      .footer {
        gap: $space-lg;
        padding: $space-lg;
      }
    }
  }
}
</style>

<style lang="scss">
.create-file-popup,
.rename-file-popup,
.move-file-popup,
.upload-file-popup {
  .actions {
    width: 100%;
    display: flex;
    justify-content: space-between;
    gap: $space-xl;
  }
}

@media (max-width: 768px) {
  .create-file-popup,
  .rename-file-popup,
  .move-file-popup,
  .upload-file-popup {
    .actions {
      gap: $space-md;
    }
  }
}
</style>