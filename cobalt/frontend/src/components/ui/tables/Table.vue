<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="table">
    <div class="wrapper">
      <table v-if="rows.length > 0 && !accessDenied">
        <thead>
        <tr>
          <th v-if="withCheckboxes">
            <div class="label-checkbox">
              <input
                type="checkbox"
                class="checkbox"
                :checked="allSelected"
                @change="handleToggleAllSelection"
              />
            </div>
          </th>
          <th
            v-for="column in columns"
            :key="column.field"
            :data-sort-field="column.params.sorting?.sortable ? column.field : undefined"
            :class="[
                column.params.sorting?.sortable ? 'sortable' : '',
                currentSort?.field === (column.params.sorting?.field ?? column.field)
                  ? `sort-${currentSort.direction}`
                  : ''
              ]"
            @click="column.params.sorting?.sortable && handleSortClick(column)"
          >
            <span>{{ column.params.label.value }}</span>
          </th>
          <th v-if="withActions && $slots.tableRowActions">{{ $t('common.actions') }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="row in rows" :key="row.id">
          <td v-if="withCheckboxes">
            <div class="label-checkbox">
              <input
                v-if="row.id !== '__back__'"
                type="checkbox"
                class="checkbox item"
                :checked="tableStore.isSelected(tableId, row.id)"
                @change="handleToggleItemSelection(row.id)"
              />
            </div>
          </td>
          <td
            v-for="column in columns"
            :key="column.field"
            class="cell"
            :class="{ clickable: !!column.params.action }"
            @click="column.params.action?.(row)"
          >
            <div class="field">
              <template v-if="column.type === 'text'">
                <div class="text" :class="{ highlighted: column.params.label.highlighted }">
                  <p class="value">
                    {{ row[column.field] }}
                    <span class="tooltip">{{ row[column.field] }}</span>
                  </p>
                </div>
              </template>
              <template v-else-if="column.type === 'tag'">
                <div class="tag" :class="column.params.color">
                  <p class="value">
                    {{ row[column.field] }}
                    <span class="tooltip">{{ row[column.field] }}</span>
                  </p>
                </div>
              </template>
              <template v-else-if="column.type === 'icon-text'">
                <div class="icon-text" :class="{ highlighted: column.params.label.highlighted }">
                  <div
                    v-if="column.params.iconField && row[column.params.iconField]"
                    class="icon"
                    :class="column.params.iconSize"
                  >
                    <img
                      :src="row[column.params.iconField]"
                      :alt="row[column.field]"
                    />
                  </div>
                  <p class="value">
                    {{ row[column.field] }}
                    <span class="tooltip">{{ row[column.field] }}</span>
                  </p>
                </div>
              </template>
            </div>
          </td>
          <td
            v-if="withActions && $slots.tableRowActions" class="actions">
            <slot name="tableRowActions" :row="row"/>
          </td>
        </tr>
        </tbody>
      </table>
      <div v-else-if="accessDenied" class="empty-state">
        <Message
          :icon="padlockIcon"
          :text="$t('common.accessDenied')"
        />
      </div>
      <div v-else class="empty-state">
        <Message
          :icon="listIcon"
          :text="$t('common.noData')"
        />
      </div>
    </div>
    <div class="footer" v-if="$slots.footerActions || $slots.footerPagination || $slots.footerCounter">
      <div class="actions" v-if="$slots.footerActions">
        <slot name="footerActions"/>
      </div>
      <div class="pagination" v-if="$slots.footerPagination">
        <slot name="footerPagination"/>
      </div>
      <div class="counter" v-if="$slots.footerCounter">
        <slot name="footerCounter"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"

import { useTableStore } from "@/stores"
import type { SortDirection, SortState, TableColumn } from "@/types"

import Message from "@/components/ui/Message.vue"
import padlockIcon from "@/assets/images/svg/padlock.svg?raw"
import listIcon from "@/assets/images/svg/clipboard-blank.svg?raw"

const props = withDefaults(defineProps<{
  tableId: string
  columns: TableColumn[]
  rows: Array<Record<string, any>>
  withActions?: boolean
  withCheckboxes?: boolean
  accessDenied?: boolean
}>(), {
  withActions: false,
  withCheckboxes: true,
  accessDenied: false
})

const emit = defineEmits<{
  (e: "sort-change", field: string, direction: SortDirection): void
}>()

const tableStore = useTableStore()

/**
 * Toggles selection state for all rows on the current page.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function handleToggleAllSelection(): void {
  tableStore.toggleAllSelection(props.tableId, rowIds.value)
}

/**
 * Toggles selection state for a single row.
 *
 * Parameters:
 * - id: string | number - unique identifier of the row to toggle.
 *
 * Returns:
 * - void.
 */
function handleToggleItemSelection(id: string | number): void {
  tableStore.toggleItemSelection(props.tableId, id)
}

/**
 * Handles sort column click, toggles direction if same field or resets to desc for a new field.
 *
 * Parameters:
 * - field: string - column field name to sort by.
 *
 * Returns:
 * - void.
 */
function handleSortClick(column: TableColumn): void {
  const field = column.params.sorting?.field ?? column.field
  const sort = tableStore.toggleSort(props.tableId, field)
  emit("sort-change", sort.field, sort.direction)
}

/**
 * Returns a list of all row IDs on the current page.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Array<string | number>: List of IDs from all currently rendered rows.
 */
const rowIds = computed((): Array<string | number> =>
  props.rows
    .filter(row => row.id !== "__back__")
    .map(row => row.id)
)

/**
 * Returns true if all rows on the current page are selected.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if every row on the current page is selected, `false` otherwise.
 */
const allSelected = computed((): boolean =>
  tableStore.isAllSelected(props.tableId, rowIds.value)
)

/**
 * Returns current sort state for the table.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - SortState | null: current sort field and direction, or null if no sort is applied.
 */
const currentSort = computed((): SortState | null =>
  tableStore.getSort(props.tableId)
)
</script>

<style scoped lang="scss">
@mixin tooltip-popup {
  visibility: hidden;
  width: max-content;
  max-width: 200px;
  bottom: calc(100% + #{$space-md});
  left: 50%;
  transform: translateX(-50%);
  background-color: var(--color-block-alt);
  color: var(--color-text);
  font-size: $font-xs;
  padding: $space-md;
  border-radius: 6px;
  position: absolute;
  z-index: 1;
  opacity: 0;
  border: 1px solid var(--color-border-alt);
  box-shadow: var(--shadow-easy);
  transition: opacity 0.3s;
  word-break: break-word;
  white-space: break-spaces;

  &::after {
    content: " ";
    position: absolute;
    top: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: var(--color-block-alt) transparent transparent transparent;
  }
}

.table {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;

  .wrapper {
    width: 100%;
    height: 100%;
    overflow: auto;
    overscroll-behavior: none;
    @include scrollbar();
    display: flex;
    flex-direction: column;

    .empty-state {
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--color-text);
      font-size: $font-md;
      border-top: 1px solid var(--color-border-alt);
    }
  }
}

table {
  width: 100%;
  white-space: nowrap;
  border-collapse: collapse;

  thead {
    position: sticky;
    top: 0;
    z-index: 1;

    tr {
      background-color: var(--color-block-alt);
      border-bottom: unset;

      th {
        padding: $space-md;
        font-weight: 600;
      }
    }
  }

  tr {
    text-align: left;
    border-bottom: 1px solid var(--color-border-alt);

    th,
    td {
      font-size: $font-md;
      color: var(--color-text);
      width: max-content;
      padding: $space-xl $space-md;

      &:first-child {
        padding-left: $space-xl;
      }

      &:last-child {
        padding-right: $space-xl;
      }

      .field {
        display: flex;
        justify-content: flex-start;
        position: relative;
        width: max-content;

        .text,
        .tag,
        .icon-text {
          max-width: 250px;
          display: flex;
          align-items: center;

          &.highlighted {
            color: var(--color-title);
          }

          .value {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            line-height: normal;
          }
        }

        .tag {
          padding: $space-sm $space-md;
          border-radius: 4px;

          &.red {
            color: var(--color-red);
            background-color: var(--color-red-background);
          }

          &.blue {
            color: var(--color-blue);
            background-color: var(--color-blue-background);
          }

          &.green {
            color: var(--color-green);
            background-color: var(--color-green-background);
          }

          &.yellow {
            color: var(--color-yellow);
            background-color: var(--color-yellow-background);
          }

          &.gray {
            color: var(--color-text);
            background-color: var(--color-gray-background);
          }
        }

        .icon-text {
          display: flex;
          align-items: center;
          gap: $space-md;

          .icon {
            &.small {
              width: 18px;
              min-width: 18px;
              height: 18px;
            }

            &.medium {
              width: 30px;
              min-width: 30px;
              height: 30px;
            }

            img {
              width: 100%;
              height: 100%;
              object-fit: contain;
            }
          }
        }
      }
    }

    th:first-child,
    td:first-child {
      width: 1px;
      white-space: nowrap;
    }

    th.sortable {
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
    }

    th[data-sort-field] {
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;

      &.sort-asc,
      &.sort-desc {
        span {
          position: relative;

          &::after {
            content: "";
            position: absolute;
            right: -25px;
            top: 50%;
            transform: translateY(-50%) rotate(0deg);
            width: 20px;
            height: 20px;
            background-color: var(--color-text);
            -webkit-mask-image: url("@/assets/images/svg/angle-down.svg");
            mask-image: url("@/assets/images/svg/angle-down.svg");
            mask-repeat: no-repeat;
            mask-size: contain;
            transition: transform 0.3s ease;
          }
        }
      }

      &.sort-asc {
        span::after {
          transform: translateY(-50%) rotate(180deg);
        }
      }
    }

    .label-checkbox {
      display: flex;
      align-items: center;

      .checkbox {
        appearance: none;
        -webkit-appearance: none;
        width: 20px;
        height: 20px;
        border: 2px solid var(--color-border);
        border-radius: 4px;
        background-color: transparent;
        cursor: pointer;
        margin: 0;
        position: relative;

        &:focus-visible {
          outline: 2px solid var(--color-primary);
          outline-offset: -2px;
        }

        &:checked {
          background-color: var(--color-primary);
          border-color: var(--color-primary);

          &::after {
            content: "";
            position: absolute;
            inset: 0;
            background-color: var(--color-white);
            -webkit-mask-image: url("@/assets/images/svg/check.svg");
            mask-image: url("@/assets/images/svg/check.svg");
            mask-repeat: no-repeat;
            mask-position: center;
            mask-size: 16px;
          }
        }
      }
    }

    .cell {
      position: relative;

      &.clickable {
        cursor: pointer;

        .value {
          transition: color 0.3s ease;

          &:hover {
            color: var(--color-primary);
          }
        }
      }

      .value {
        .tooltip {
          @include tooltip-popup;
          text-align: center;
        }

        &:hover .tooltip {
          visibility: visible;
          opacity: 1;
        }
      }
    }

    .actions {
      width: 100%;
      display: flex;
      align-items: center;
      gap: $space-md;
      box-sizing: border-box;

      :deep(.status-icon) {
        position: relative;
        display: flex;
        align-items: center;

        .hint {
          text-align: center;
          @include tooltip-popup;
        }

        &:hover .hint {
          visibility: visible;
          opacity: 1;
        }
      }
    }
  }
}

.footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: $space-md;
  padding: $space-xl;
  margin-top: auto;
  border-top: 1px solid var(--color-border-alt);

  .actions,
  .pagination,
  .counter {
    width: 100%;
    display: flex;
  }

  .actions {
    justify-content: flex-start;
    flex-wrap: wrap;
    gap: $space-md;
  }

  .pagination {
    justify-content: center;
  }

  .counter {
    justify-content: flex-end;
    text-wrap: nowrap;
  }
}

@media (max-width: 768px) {
  .table {
    .wrapper {
      .empty-state {
        font-size: $font-sm;
      }
    }
  }

  table {
    tr {
      th,
      td {
        font-size: $font-sm;
        padding: $space-lg $space-md;
      }

      th {
        &:first-child {
          padding-left: $space-lg;
        }

        &:last-child {
          padding-right: $space-lg;
        }
      }

      td {
        &:first-child {
          padding-left: $space-lg;
        }

        &:last-child {
          padding-right: $space-lg;
        }
      }

      .label-checkbox {
        .checkbox {
          width: 18px;
          height: 18px;
        }
      }
    }
  }

  .footer {
    flex-wrap: wrap;
    padding: $space-lg;

    .actions {
      width: auto;
    }

    .pagination {
      width: auto;
    }

    .counter {
      width: 100%;
      justify-content: center;
      order: 1;
    }
  }
}
</style>