<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block class="logs">
    <div class="heading">
      <Header
        :icon="monitorIcon"
        icon-color="blue"
        :title="title ?? $t('logs.title')"
        :description="description ?? $t('logs.description')"
        :icon-filled="true"
      />
    </div>
    <Message
      v-if="!hasLogsViewAccess"
      :icon="padlockIcon"
      :text="$t('common.accessDenied')"
    />
    <Message
      v-else-if="parsedLogs.length === 0"
      :icon="listIcon"
      :text="$t('common.noData')"
    />
    <TabsBlock
      v-else
      ref="tabsRef"
      :tabs="logTabs"
      v-model="activeTab"
    >
      <template v-for="tab in logTabs" :key="tab.value" #[tab.value]>
        <div class="items">
          <div v-for="(log, index) in parsedLogs" :key="index" class="item">
            <template v-for="(line, lineIndex) in log.message.split('\n')" :key="lineIndex">
              <div class="line">
                <span class="message">
                  <template v-if="lineIndex === 0">
                    <span v-if="log.date" class="date">{{ log.date }}</span>
                    >
                  </template>{{ line }}
                </span>
              </div>
            </template>
          </div>
        </div>
      </template>
    </TabsBlock>
    <template v-if="hasConsoleExecuteAccess">
      <div class="console-input-wrapper">
        <input
          class="console-input"
          v-model="command"
          :placeholder="$t('logs.placeholder')"
          name="server-console"
          @keydown.enter="handleExecute"
          @keydown.up.prevent="handleHistoryUp"
          @keydown.down.prevent="handleHistoryDown"
        />
        <div class="history-arrows">
          <button type="button" class="arrow-btn" @click="handleHistoryUp" v-html="angleUpIcon" />
          <button type="button" class="arrow-btn" @click="handleHistoryDown" v-html="angleDownIcon" />
        </div>
      </div>
    </template>
  </Block>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"
import { inject, onMounted, onUnmounted, ref, computed, nextTick, watch } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import { useServerConsoleStore, useUserStore } from "@/stores"
import {
  LOCALE_HELPER_KEY,
  HTTP_LOGS_API_SERVICE_KEY,
  HTTP_SERVERS_API_SERVICE_KEY,
  WS_LOGS_API_SERVICE_KEY
} from "@/constants"
import { PermissionEnum } from "@/types"

import Block from "@/components/ui/Block.vue"
import Header from "@/components/ui/Header.vue"
import TabsBlock from "@/components/ui/tabs/TabsBlock.vue"
import Message from "@/components/ui/Message.vue"

import monitorIcon from "@/assets/images/svg/monitor.svg?raw"
import padlockIcon from "@/assets/images/svg/padlock.svg?raw"
import listIcon from "@/assets/images/svg/clipboard-blank.svg?raw"
import angleUpIcon from "@/assets/images/svg/angle-up.svg?raw"
import angleDownIcon from "@/assets/images/svg/angle-down.svg?raw"

interface ServerLog {
  date: string | null
  message: string
}

const props = defineProps<{
  serverId: number
  title?: string
  description?: string
  maxLogs: number
}>()

const wsLogsApiService = inject(WS_LOGS_API_SERVICE_KEY)!
const httpLogsApiService = inject(HTTP_LOGS_API_SERVICE_KEY)!
const httpServersApiService = inject(HTTP_SERVERS_API_SERVICE_KEY)!
const localeHelper = inject(LOCALE_HELPER_KEY)!
const userStore = useUserStore()
const serverConsoleStore = useServerConsoleStore()
const { notify } = useNotification()
const { t } = useI18n()

const TAB_VALUE = "logs"

const parsedLogs = ref<ServerLog[]>([])
const tabsRef = ref<InstanceType<typeof TabsBlock> | null>(null)
const activeTab = ref<string | null>(TAB_VALUE)
const command = ref("")

const LOG_REGEX = /^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})(?:\.\d+)?Z? ?(.*)/s
const CONTINUATION_REGEX = /^\s/

/**
 * Parses a raw log message into a structured ServerLog object.
 * Supports format: "2026-04-06 15:48:37 message"
 *
 * Parameters:
 * - message: Raw log string to parse.
 *
 * Returns:
 * - ServerLog: Object with nullable date and message body.
 */
function parseLog(message: string): ServerLog {
  const match = message.match(LOG_REGEX)

  console.log(message)

  if (match) {
    const date = `${match[1]} ${match[2]}Z`
    const time = localeHelper.formatTimeWithSeconds(date)

    return {
      date: `${match[1]} ${time}`,
      message: match[3] ?? ""
    }
  }

  return {
    date: null,
    message: message
  }
}

/**
 * Returns the active scrollable panel container.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - HTMLElement | null: The `.wrapper` element, or null if not found.
 */
function getScrollContainer(): HTMLElement | null {
  const element = tabsRef.value?.$el as HTMLElement | undefined
  if (!element) return null

  const wrappers = Array.from(element.querySelectorAll('.wrapper')) as HTMLElement[]

  return wrappers[0] ?? null
}

/**
 * Checks if the user is near the bottom of the log panel.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if user is near the bottom.
 */
function isNearBottom(): boolean {
  const element = getScrollContainer()
  if (!element) return true
  const { scrollTop, scrollHeight, clientHeight } = element
  return scrollHeight - scrollTop - clientHeight <= 300
}

/**
 * Scrolls the log panel to the bottom after the next DOM update.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function scrollToBottom(): Promise<void> {
  await nextTick()
  const el = getScrollContainer()
  if (el) {
    el.scrollTop = el.scrollHeight
  }
}

/**
 * Merges a continuation line into the last entry of the target array.
 * If the target is empty, parses the text as a new entry.
 * When merging, trims combined lines to maxLogs if exceeded.
 *
 * Parameters:
 * - target: ServerLog array to merge into.
 * - text: Text to append to the last entry's message.
 *
 * Returns:
 * - void.
 */
function mergeIntoLast(target: ServerLog[], text: string): void {
  const last = target[target.length - 1] as ServerLog | undefined

  if (last) {
    const combined = last.message + "\n" + text
    const lines = combined.split('\n')

    target[target.length - 1] = {
      ...last,
      message: lines.length > props.maxLogs
        ? lines.slice(-props.maxLogs).join('\n')
        : combined
    }
  } else {
    target.push(parseLog(text))
  }
}

/**
 * Appends a batch of raw log objects into the target ServerLog array.
 *
 * Parameters:
 * - target: Target ServerLog array to append into.
 * - rawLogs: Raw log objects with a message field.
 *
 * Returns:
 * - void.
 */
function appendLogs(target: ServerLog[], rawLogs: Array<{ message: string }>): void {
  for (const log of rawLogs) {
    const parsed = parseLog(log.message)

    if (parsed.date !== null) {
      if (!parsed.message.trim()) {
        continue
      }

      if (CONTINUATION_REGEX.test(parsed.message)) {
        mergeIntoLast(target, parsed.message)
      } else {
        target.push(parsed)
      }
    } else {
      mergeIntoLast(target, log.message)
    }
  }
}

/**
 * Fetches initial logs from the API and populates parsedLogs.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function fetchInitialData(): Promise<void> {
  try {
    const raw = await httpLogsApiService.getServerAll(props.serverId)

    const result: ServerLog[] = []
    appendLogs(result, raw)
    parsedLogs.value = result
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("logs.fetch.error")
    })
  }
}

/**
 * Handles real-time log updates received from WebSocket.
 * Ignores messages from other servers.
 * Trims parsedLogs to maxLogs after appending.
 *
 * Parameters:
 * - message: Message object containing log data and server_id.
 *
 * Returns:
 * - void.
 */
function handleLogUpdate(message: any): void {
  if (message.server_id !== props.serverId) return

  appendLogs(parsedLogs.value, message.data)

  if (parsedLogs.value.length > props.maxLogs) {
    parsedLogs.value = parsedLogs.value.slice(-props.maxLogs)
  }
}

/**
 * Executes a command inside the server container.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleExecute(): Promise<void> {
  if (!command.value.trim()) return

  try {
    await httpServersApiService.execute(props.serverId, {
      command: command.value
    })

    serverConsoleStore.push(props.serverId, command.value)
    serverConsoleStore.resetNavigation(props.serverId)
    command.value = ""
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("logs.execute.error")
    })
  }
}

/**
 * Navigates to the previous command in history for the current server.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleHistoryUp(): void {
  const value = serverConsoleStore.navigateUp(props.serverId, command.value)
  if (value !== null) command.value = value
}

/**
 * Navigates to the next command in history for the current server.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleHistoryDown(): void {
  const value = serverConsoleStore.navigateDown(props.serverId)
  if (value !== null) command.value = value
}

/**
 * Builds the single "logs" tab.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Array<{ label: string, value: string }>: Tab definitions.
 */
const logTabs = computed(() => [
  {
    label: `${t("logs.title")} ${parsedLogs.value.length}`,
    value: TAB_VALUE
  }
])

/**
 * Checks whether the current user has access to view server logs.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasLogsViewAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.SERVER_LOGS_VIEW)
)

/**
 * Checks whether the current user has access to execute console commands.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasConsoleExecuteAccess = computed((): boolean =>
  userStore.hasPermission(PermissionEnum.SERVER_CONSOLE_EXECUTE)
)

watch(parsedLogs, async () => {
  if (isNearBottom()) {
    await scrollToBottom()
  }
}, { deep: true })

watch(activeTab, async () => {
  await scrollToBottom()
})

onMounted(() => {
  if (hasLogsViewAccess.value) {
    fetchInitialData()
    wsLogsApiService.subscribeServer(props.serverId, handleLogUpdate)
  }
})

onUnmounted(() => {
  wsLogsApiService.unsubscribeServer(props.serverId, handleLogUpdate)
})
</script>

<style scoped lang="scss">
.logs {
  min-height: 500px;
  display: flex;
  flex-direction: column;

  .heading {
    padding: $space-xl;
  }

  .tabs {
    :deep(.content) {
      padding: $space-xl;
    }
  }

  .console-input-wrapper {
    display: flex;
    position: relative;

    .console-input {
      width: 100%;
      background-color: var(--color-block-alt);
      padding: $space-xl;
      border-radius: 0 0 12px 12px;
      border: none;
      color: var(--color-description);
      font-size: $font-md;
      font-weight: 600;
      font-family: "Montserrat", sans-serif;
      box-sizing: border-box;
      outline: none;

      &::placeholder {
        opacity: 1;
        color: var(--color-description);
      }
    }

    .history-arrows {
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: $space-md;
      position: absolute;
      right: $space-xl;
      bottom: 0;

      .arrow-btn {
        width: 11px;
        height: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--color-description);
        background-color: transparent;
        border: none;
        padding: 0;
        cursor: pointer;
        transition: color 0.3s;

        &:hover {
          color: var(--color-title);
        }

        svg {
          width: 100%;
          height: 100%;
          object-fit: contain;
        }
      }
    }
  }

  .items {
    outline: none;

    .item {
      span {
        font-family: "JetBrains Mono", monospace;
        font-weight: 600;
      }

      .line {
        .message {
          color: var(--color-description);
          font-size: $font-sm;
          word-break: break-word;
          line-height: 1.8;
          white-space: pre-wrap;

          .date {
            color: var(--color-title);
            white-space: nowrap;
            flex-shrink: 0;
          }
        }
      }
    }
  }

  .message {
    height: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .logs {
    .heading {
      padding: $space-lg;
    }

    .tabs {
      :deep(.content) {
        padding: $space-lg;
      }
    }

    .console-input-wrapper {
      .console-input {
        font-size: $font-sm;
        padding: $space-lg;
      }

      .history-arrows {
        right: $space-lg;

        .arrow-btn {
          width: 9px;
          height: 9px;
        }
      }
    }
  }
}
</style>