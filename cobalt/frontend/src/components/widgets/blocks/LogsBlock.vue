<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
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
      v-if="mode !== 'empty' && !hasLogsViewAccess"
      :icon="padlockIcon"
      :text="$t('common.accessDenied')"
    />
    <Message
      v-else-if="mode === 'empty' || parsedLogs.length === 0"
      :icon="listIcon"
      :text="$t('common.noData')"
    />
    <BlockTabs
      v-else
      ref="tabsRef"
      :tabs="logTabs"
      v-model="activeTab"
    >
      <template v-for="tab in logTabs" :key="tab.value" #[tab.value]>
        <div class="items">
          <div v-for="(log, index) in filteredLogs" :key="index" class="item">
            <template v-for="(line, lineIndex) in log.message.split('\n')" :key="lineIndex">
              <div class="line">
                <span class="message">
                  <template v-if="lineIndex === 0">
                    <span v-if="log.date" class="date">{{ log.date }}</span>
                    <span v-if="log.level" class="level" :class="log.level.toLowerCase()">[{{ log.level }}]</span>
                  </template>{{ line }}
                </span>
              </div>
            </template>
          </div>
        </div>
      </template>
    </BlockTabs>
    <template v-if="mode === 'server' && hasConsoleExecuteAccess">
      <input
        class="console-input"
        v-model="command"
        :placeholder="$t('logs.placeholder')"
        name="server-console"
        @keydown.enter="handleExecute"
      />
    </template>
  </Block>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"
import { inject, onMounted, onUnmounted, ref, computed, nextTick, watch } from "vue"
import { useNotification } from "@kyvg/vue3-notification"

import { LOCALE_HELPER_KEY, HTTP_LOGS_API_SERVICE_KEY, HTTP_SERVERS_API_SERVICE_KEY, WS_LOGS_API_SERVICE_KEY } from "@/utils"
import { useUserStore } from "@/stores"
import { PermissionsEnum } from "@/types"
import type { UniversalBlockMode, ParsedLog } from "@/types"

import Block from "@/components/ui/Block.vue"
import Header from "@/components/ui/Header.vue"
import BlockTabs from "@/components/ui/tabs/BlockTabs.vue"
import Message from "@/components/ui/Message.vue"
import monitorIcon from "@/assets/images/svg/monitor.svg?raw"
import padlockIcon from "@/assets/images/svg/padlock.svg?raw"
import listIcon from "@/assets/images/svg/clipboard-blank.svg?raw"

const props = withDefaults(defineProps<{
  mode: UniversalBlockMode
  serverId?: number
  title?: string
  description?: string
  maxLogs: number
  logsRegex?: RegExp
}>(), {
  serverId: undefined
})

const wsLogsApiService = inject(WS_LOGS_API_SERVICE_KEY)!
const httpLogsApiService = inject(HTTP_LOGS_API_SERVICE_KEY)!
const httpServersApiService = inject(HTTP_SERVERS_API_SERVICE_KEY)!
const localeHelper = inject(LOCALE_HELPER_KEY)!
const userStore = useUserStore()
const { notify } = useNotification()
const { t } = useI18n()

const parsedLogs = ref<ParsedLog[]>([])
const tabsRef = ref<InstanceType<typeof BlockTabs> | null>(null)
const activeTab = ref<string | null>(null)
const command = ref("")

const LOG_REGEX = /^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})\s+(INFO|ERROR|WARNING|WARN|DEBUG|CRITICAL)? (.*)/s
const CONTINUATION_REGEX = /^\s/
const LEVEL_ORDER: Record<string, number> = {
  Info: 0,
  Warn: 1,
  Error: 2,
  Critical: 3,
  Debug: 4
}
const LEVEL_ALIAS: Record<string, string> = {
  INF: "Info",
  WRN: "Warn",
  ERR: "Error",
  EXC: "Critical"
}

/**
 * Guesses log level from message content.
 *
 * Parameters:
 * - message: Log message string.
 *
 * Returns:
 * - string: Guessed log level.
 */
function guessLevel(message: string): string {
  if (/warn(ing)?/i.test(message)) return "Warn"
  if (/error|exception|failed|failure/i.test(message)) return "Error"
  return "Info"
}

/**
 * Parses a raw log message into a structured ParsedLog object.
 * Supports format: "2026-04-06 15:48:37 LEVEL message"
 *
 * Parameters:
 * - message: Raw log string to parse.
 * - regex: Regular expression to match against.
 *
 * Returns:
 * - ParsedLog: Object with nullable date, level, and message body.
 */
function parseLog(message: string, regex: RegExp): ParsedLog {
  const stripped = message.replace(/\x1b\[[0-9;]*m/g, '')
  const match = stripped.match(regex)

  if (match) {
    const rawLevel = match[3]
    const rest = match[4] ?? ""
    let level: string

    if (!rawLevel) {
      level = guessLevel(rest)
    } else if (LEVEL_ALIAS[rawLevel.toUpperCase()]) {
      level = LEVEL_ALIAS[rawLevel.toUpperCase()] ?? "Info"
    } else if (rawLevel.toLowerCase() === "warning") {
      level = "Warn"
    } else {
      level = rawLevel.charAt(0).toUpperCase() + rawLevel.slice(1).toLowerCase()
    }

    let date = `${match[1]} ${match[2]}Z`
    let time = localeHelper.formatTimeWithSeconds(date)

    return {
      date: `${match[1]} ${time}`,
      level: level,
      message: rest
    }
  }

  return {
    date: null,
    level: guessLevel(message),
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
 * - HTMLElement | null: The active `.wrapper` element, or null if not found.
 */
function getScrollContainer(): HTMLElement | null {
  const element = tabsRef.value?.$el as HTMLElement | undefined
  if (!element) return null

  const wrappers = Array.from(element.querySelectorAll('.wrapper')) as HTMLElement[]
  const index = logTabs.value.findIndex(tab => tab.value === activeTab.value)

  return wrappers[index] ?? null
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
 * Scrolls the active log panel to the bottom after the next DOM update.
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
 * If the target is empty, parses the text as a new entry via defaultParseLog.
 * When merging, trims combined lines to maxLogs if exceeded.
 *
 * Parameters:
 * - target: ParsedLog array to merge into.
 * - text: Text to append to the last entry's message.
 *
 * Returns:
 * - void.
 */
function mergeIntoLast(target: ParsedLog[], text: string): void {
  const last = target[target.length - 1] as ParsedLog | undefined

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
    target.push(parseLog(text, activeRegex.value))
  }
}

/**
 * Appends a batch of raw log objects into the target ParsedLog array.
 *
 * Parameters:
 * - target: Target ParsedLog array to append into.
 * - rawLogs: Raw log objects with a message field.
 *
 * Returns:
 * - void.
 */
function appendLogs(target: ParsedLog[], rawLogs: Array<{ message: string }>): void {
  for (const log of rawLogs) {
    const parsed = parseLog(log.message, activeRegex.value)

    if (parsed.date !== null) {
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
    const raw = props.mode === "server"
      ? await httpLogsApiService.getServerAll(props.serverId!)
      : await httpLogsApiService.getHostAll()

    const result: ParsedLog[] = []
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
 * Ignores messages from other servers when in server mode.
 * Trims parsedLogs to maxLogs after appending.
 *
 * Parameters:
 * - message: Message object containing log data and optional server_id.
 *
 * Returns:
 * - void.
 */
function handleLogUpdate(message: any): void {
  if (props.mode === "server" && message.server_id !== props.serverId) return

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
  if (!command.value.trim() || props.mode !== "server") return

  try {
    await httpServersApiService.execute(props.serverId!, {
      command: command.value
    })
    command.value = ""
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("logs.execute.error")
    })
  }
}

/**
 * Builds the list of tabs from existing log levels.
 * Does not include an "All" tab - first available level is selected by default.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Array<{ label: string, value: string }>: Tab definitions for each log level.
 */
const logTabs = computed(() => {
  const counts: Record<string, number> = {}

  for (const log of parsedLogs.value) {
    const level = log.level ?? "Info"
    counts[level] = (counts[level] ?? 0) + 1
  }

  return Object.entries(counts)
    .sort(([a], [b]) => (LEVEL_ORDER[a] ?? 99) - (LEVEL_ORDER[b] ?? 99))
    .map(([level, count]) => ({
      label: `${t(`logs.levels.${level.toLowerCase()}`)} ${count}`,
      value: level
    }))
})

/**
 * Returns logs filtered by the active tab level.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - ParsedLog[]: Filtered log entries matching the active level.
 */
const filteredLogs = computed(() => {
  if (!activeTab.value) return parsedLogs.value
  return parsedLogs.value.filter(log => (log.level ?? "Info") === activeTab.value)
})

/**
 * Returns the active regex.
 * Uses the custom logsRegex prop if provided, otherwise falls back to LOG_REGEX.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - RegExp.
 */
const activeRegex = computed((): RegExp =>
  props.logsRegex ?? LOG_REGEX
)

/**
 * Checks whether the current user has access to view logs.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasLogsViewAccess = computed((): boolean =>
  props.mode === "server"
    ? userStore.hasPermission(PermissionsEnum.SERVER_LOGS_VIEW)
    : userStore.hasPermission(PermissionsEnum.DASHBOARD_LOGS_VIEW)
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
  userStore.hasPermission(PermissionsEnum.SERVER_CONSOLE_EXECUTE)
)

watch(parsedLogs, async () => {
  if (isNearBottom()) {
    await scrollToBottom()
  }
}, { deep: true })

watch(activeTab, async () => {
  await scrollToBottom()
})

watch(logTabs, (tabs) => {
  const [first] = tabs
  if (!activeTab.value && first) {
    activeTab.value = first.value
  }
})

onMounted(() => {
  if (props.mode !== "empty" && hasLogsViewAccess.value) {
    fetchInitialData()

    if (props.mode === "server") {
      wsLogsApiService.subscribeServer(props.serverId!, handleLogUpdate)
    } else {
      wsLogsApiService.subscribeHost(handleLogUpdate)
    }
  }
})

onUnmounted(() => {
  if (props.mode === "server") {
    wsLogsApiService.unsubscribeServer(props.serverId!, handleLogUpdate)
  } else {
    wsLogsApiService.unsubscribeHost(handleLogUpdate)
  }
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
            margin-right: $space-sm;
          }

          .level {
            font-weight: 700;
            white-space: nowrap;
            flex-shrink: 0;
            margin-right: $space-sm;

            &.info {
              color: var(--color-blue);
            }

            &.error,
            &.critical,
            &.fatal {
              color: var(--color-red);
            }

            &.warn {
              color: var(--color-yellow);
            }

            &.debug {
              color: var(--color-green);
            }
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

    .console-input {
      font-size: $font-sm;
      padding: $space-lg;
    }
  }
}
</style>