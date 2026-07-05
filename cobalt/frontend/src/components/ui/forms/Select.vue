<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="select-wrapper">
    <FieldLabel
      v-if="label"
      :text="label"
      :required="required"
    />
    <div
      ref="selectRef"
      class="select"
      :class="{
        open: isOpen,
        disabled
      }"
      :aria-label="name"
    >
      <div
        class="trigger"
        tabindex="0"
        @click="toggle"
        @keydown.tab="close"
        @keydown.down.prevent="selectNext"
        @keydown.up.prevent="selectPrev"
      >
        <div class="content">
          <div
            v-if="selectedOption?.icon"
            class="icon"
            v-html="selectedOption.icon"
          />
          <span class="value" :class="{ placeholder: !modelValue }">
            {{ selectedLabel ?? placeholder ?? 'Select...' }}
          </span>
        </div>
        <div class="arrow" />
      </div>
    </div>
    <Teleport to="body">
      <Transition name="dropdown">
        <div
          v-if="isOpen"
          ref="dropdownRef"
          class="select-dropdown"
          :style="style"
          @keydown.esc="close"
        >
          <div
            v-for="option in options"
            :key="option.value"
            class="option"
            @click="select(option)"
          >
            <div
              v-if="option.icon"
              class="icon"
              v-html="option.icon"
            />
              <span
                class="value"
                :class="{ selected: modelValue === option.value }"
                :aria-label="String(option.value)"
              >
                {{ option.label }}
              </span>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, inject, onMounted, onUnmounted, watch } from "vue"

import { FORM_KEY } from "@/utils"
import type { FormContext, SelectOption } from "@/types"

import FieldLabel from "@/components/ui/forms/FieldLabel.vue"

const props = defineProps<{
  validationName?: string
  modelValue?: string | number
  options: SelectOption[]
  name?: string
  placeholder?: string
  disabled?: boolean
  label?: string
  required?: boolean
}>()

const emit = defineEmits<{
  (e: "update:modelValue", value: string | number): void
}>()

const form = inject<FormContext | null>(FORM_KEY, null)

const id = Symbol()
const isOpen = ref(false)
const selectRef = ref<HTMLElement | null>(null)
const dropdownRef = ref<HTMLElement | null>(null)
const style = ref<Record<string, string>>({})

const DROPDOWN_MIN_ITEMS = 4
const DROPDOWN_MOBILE_BREAKPOINT = 768
const DROPDOWN_OFFSET_MOBILE = 10
const DROPDOWN_OFFSET_DESKTOP = 20
const DROPDOWN_GAP = 10

/**
 * Opens the dropdown.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function toggle(): void {
  if (props.disabled) return
  isOpen.value = !isOpen.value
}

/**
 * Closes the dropdown.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function close(): void {
  isOpen.value = false
}

/**
 * Selects an option and closes the dropdown.
 *
 * Parameters:
 * - option: Option to select.
 *
 * Returns:
 * - void.
 */
function select(option: SelectOption): void {
  emit("update:modelValue", option.value)
  close()
}

/**
 * Selects the next option in the list without opening the dropdown.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function selectNext(): void {
  if (props.disabled || props.options.length === 0) return
  const currentIndex = props.options.findIndex(option => option.value === props.modelValue)
  const next = currentIndex < props.options.length - 1 ? currentIndex + 1 : 0
  const option = props.options[next]
  if (option) emit("update:modelValue", option.value)
}

/**
 * Selects the previous option in the list without opening the dropdown.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function selectPrev(): void {
  if (props.disabled || props.options.length === 0) return
  const currentIndex = props.options.findIndex(option => option.value === props.modelValue)
  const prev = currentIndex > 0 ? currentIndex - 1 : props.options.length - 1
  const option = props.options[prev]
  if (option) emit("update:modelValue", option.value)
}

/**
 * Closes the dropdown when clicking outside the component.
 *
 * Parameters:
 * - event: Click event.
 *
 * Returns:
 * - void.
 */
function handleClickOutside(event: MouseEvent): void {
  const target = event.target as Node
  const dropdown = document.querySelector(".select-dropdown")

  if (
    selectRef.value &&
    !selectRef.value.contains(target) &&
    !(dropdown && dropdown.contains(target))
  ) {
    close()
  }
}

/**
 * Returns the currently selected option object.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - SelectOption | undefined: The matched option or undefined.
 */
const selectedOption = computed((): SelectOption | undefined =>
  props.options.find(option => option.value === props.modelValue)
)

/**
 * Returns the label of the currently selected option.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - string | undefined: The label of the matched option, or undefined if no option is selected.
 */
const selectedLabel = computed((): string | undefined =>
  selectedOption.value?.label
)

/**
 * Computes dropdown position when it opens.
 *
 * Parameters:
 * - value: Whether the dropdown is opening or closing.
 *
 * Returns:
 * - Promise<void>.
 */
watch(isOpen, async (value: boolean): Promise<void> => {
  if (!value || !selectRef.value || !dropdownRef.value) return

  const rect = selectRef.value.getBoundingClientRect()
  const offset = window.innerWidth <= DROPDOWN_MOBILE_BREAKPOINT ? DROPDOWN_OFFSET_MOBILE : DROPDOWN_OFFSET_DESKTOP
  const option = dropdownRef.value.querySelector(".option") as HTMLElement | null
  const optionHeight = option?.getBoundingClientRect().height ?? 0
  const minItemsHeight = optionHeight * DROPDOWN_MIN_ITEMS

  const spaceBelow = window.innerHeight - rect.bottom - DROPDOWN_GAP - offset
  const spaceAbove = rect.top - DROPDOWN_GAP - offset
  const openUp = spaceBelow < minItemsHeight && spaceAbove > spaceBelow

  style.value = {
    position: "fixed",
    width: `${rect.width}px`,
    left: `${rect.left}px`,
    zIndex: "1000",
    ...(openUp
        ? {
          bottom: `${window.innerHeight - rect.top + DROPDOWN_GAP}px`,
          maxHeight: `${spaceAbove}px`,
        }
        : {
          top: `${rect.bottom + DROPDOWN_GAP}px`,
          maxHeight: `${spaceBelow}px`,
        }
    ),
  }
}, { flush: "post" })

onMounted(() => {
  if (props.required && props.validationName && form) {
    form.register(id, {
      name: props.validationName,
      getValue: () => props.modelValue
    })
  }
  document.addEventListener("click", handleClickOutside)
})

onUnmounted(() => {
  form?.unregister(id)
  document.removeEventListener("click", handleClickOutside)
})
</script>

<style scoped lang="scss">
.select-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: $space-sm;

  .select {
    position: relative;
    width: 100%;

    &.disabled {
      opacity: 0.5;
      pointer-events: none;
    }

    &.open {
      .trigger {
        border-color: var(--color-primary);
      }

      .arrow {
        transform: rotate(180deg);
      }
    }

    .trigger {
      width: 100%;
      height: 40px;
      padding: 0 $space-lg;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: $space-md;
      background-color: transparent;
      border: 2px solid var(--color-border);
      border-radius: 8px;
      cursor: pointer;
      box-sizing: border-box;
      transition: border-color 0.3s ease;

      &:focus {
        outline: none;
        border-color: var(--color-primary);
      }

      .content {
        display: flex;
        align-items: center;
        gap: $space-md;
        overflow: hidden;

        .icon {
          width: 18px;
          height: 18px;

          :deep(svg) {
            width: 100%;
            height: 100%;
            object-fit: contain;
          }
        }

        .value {
          font-size: $font-md;
          font-weight: 600;
          color: var(--color-text);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          line-height: normal;

          &.placeholder {
            color: var(--color-text);
          }
        }
      }

      .arrow {
        width: 24px;
        height: 24px;
        flex-shrink: 0;
        background-color: var(--color-text);
        -webkit-mask-image: url("@/assets/images/svg/angle-down.svg");
        mask-image: url("@/assets/images/svg/angle-down.svg");
        mask-repeat: no-repeat;
        mask-size: contain;
        transition: transform 0.3s ease;
      }
    }
  }
}

@media (max-width: 768px) {
  .select-wrapper {
    .select {
      .trigger {
        height: 36px;

        .content {
          .icon {
            width: 16px;
            height: 16px;
          }

          .value {
            font-size: $font-sm;
          }
        }
      }
    }
  }
}
</style>

<style lang="scss">
.select-dropdown {
  background-color: var(--color-block-alt);
  border-radius: 8px;
  overflow-y: auto;
  overscroll-behavior: none;
  @include scrollbar();
  border: 1px solid var(--color-border-alt);
  box-shadow: var(--shadow-easy);

  .option {
    padding: $space-md $space-lg;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: $space-md;
    transition: background-color 0.3s ease, color 0.3s ease;

    &:hover {
      background-color: var(--color-block);
    }

    .icon {
      width: 18px;
      height: 18px;

      :deep(svg) {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
    }

    .value {
      font-size: $font-md;
      font-weight: 600;
      color: var(--color-text);

      &.selected {
        color: var(--color-title);
      }
    }
  }
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.3s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .select-dropdown {
    .option {
      .icon {
        width: 16px;
        height: 16px;
      }

      .value {
        font-size: $font-sm;
      }
    }
  }
}
</style>