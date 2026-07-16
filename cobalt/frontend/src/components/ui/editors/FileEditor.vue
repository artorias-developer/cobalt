<!--
  - Copyright (C) 2026 Artorias
  - Author: Artorias
  - Repository: https://github.com/artorias-developer/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div ref="container" class="codemirror-editor"/>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from "vue"
import { basicSetup } from "codemirror"
import { EditorState, Compartment, type Extension } from "@codemirror/state"
import { EditorView, keymap } from "@codemirror/view"
import { defaultKeymap } from "@codemirror/commands"
import { StreamLanguage, HighlightStyle, syntaxHighlighting } from "@codemirror/language"
import { tags } from "@lezer/highlight"
import { highlightSelectionMatches } from "@codemirror/search"
import { githubLight, githubDark } from "@uiw/codemirror-theme-github"
import { json } from "@codemirror/lang-json"
import { xml } from "@codemirror/lang-xml"
import { yaml } from "@codemirror/lang-yaml"
import { lua } from "@codemirror/legacy-modes/mode/lua"
import { shell } from "@codemirror/legacy-modes/mode/shell"
import { properties } from "@codemirror/legacy-modes/mode/properties"

import { useUserStore } from "@/stores"

const props = withDefaults(defineProps<{
  modelValue: string
  language?: string
}>(), {
  language: "plaintext"
})

const emit = defineEmits<{
  "update:modelValue": [value: string]
}>()

defineExpose({
  getValue: () => view?.state.doc.toString() ?? ""
})

const userStore = useUserStore()

let view: EditorView | null = null
const container = ref<HTMLElement | null>(null)
const languageCompartment = new Compartment()
const themeCompartment = new Compartment()

const luaLang = StreamLanguage.define(lua)
const shellLang = StreamLanguage.define(shell)
const propertiesLang = StreamLanguage.define(properties)

const propertiesHighlight = HighlightStyle.define(
  [
    {
      tag: tags.variableName,
      color: "#d19a66"
    }
  ],
  {
    scope: propertiesLang
  }
)

/**
 * Resolves CodeMirror language mode.
 *
 * Parameters:
 * - language: Language identifier.
 *
 * Returns:
 * - Extension: CodeMirror extension.
 */
function resolveLanguage(language: string): Extension {
  switch (language) {
    case "json":
      return json()
    case "xml":
      return xml()
    case "yaml":
      return yaml()
    case "lua":
      return luaLang
    case "shell":
      return shellLang
    case "properties":
      return propertiesLang
    default:
      return []
  }
}

/**
 * Resolves the CodeMirror editor theme extension based on the current user theme setting.
 *
 * Parameters:
 * - light: Whether the light theme is currently active.
 *
 * Returns:
 * - Extension: CodeMirror theme extension.
 */
function resolveTheme(light: boolean): Extension {
  return light ? githubLight : githubDark
}

/**
 * Determines whether the light theme is selected.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: True if the user's theme setting is "light".
 */
const isLightTheme = computed((): boolean =>
  Boolean(userStore.user?.settings?.theme?.toLowerCase().includes("light"))
)

/**
 * Watches for language prop changes and updates editor mode via Compartment.
 *
 * Parameters:
 * - language: New language.
 *
 * Returns:
 * - void.
 */
watch(() => props.language, (language: string): void => {
  if (!view) return

  view.dispatch({
    effects: languageCompartment.reconfigure(resolveLanguage(language))
  })
})

/**
 * Watches for user theme setting changes and updates editor theme via Compartment.
 *
 * Parameters:
 * - light: Whether the light theme is currently active.
 *
 * Returns:
 * - void.
 */
watch(isLightTheme, (light: boolean): void => {
  if (!view) return

  view.dispatch({
    effects: themeCompartment.reconfigure(resolveTheme(light))
  })
})

onMounted(() => {
  if (!container.value) return

  view = new EditorView({
    state: EditorState.create({
      doc: props.modelValue,
      extensions: [
        basicSetup,
        keymap.of(defaultKeymap),
        languageCompartment.of(resolveLanguage(props.language)),
        highlightSelectionMatches({
          minSelectionLength: 1,
          highlightWordAroundCursor: true
        }),
        syntaxHighlighting(propertiesHighlight),
        themeCompartment.of(resolveTheme(isLightTheme.value)),
        EditorView.updateListener.of((update) => {
          if (update.docChanged) {
            emit("update:modelValue", update.state.doc.toString())
          }
        })
      ]
    }),
    parent: container.value
  })
})

onUnmounted(() => {
  view?.destroy()
  view = null
})
</script>

<style scoped lang="scss">
.codemirror-editor {
  :deep(.cm-editor) {
    background-color: var(--color-block);
    font-size: 14px;
    line-height: 22px;
    height: 100%;

    &.cm-focused {
      outline: none;
    }

    span, div {
      font-family: "JetBrains Mono", monospace;
      font-weight: 600;
    }

    .cm-cursor {
      border-left-color: var(--color-description);
    }

    .cm-scroller {
      overscroll-behavior: none;
      @include scrollbar();

      .cm-gutters {
        background-color: var(--color-block);
        border: none;
        border-right: 1px solid var(--color-border);
        padding-left: 0;

        .cm-lineNumbers {
          .cm-gutterElement {
            padding-left: $space-xl;

            &.cm-activeLineGutter {
              background-color: var(--color-block-alt);
              color: var(--color-title);
            }
          }
        }

        .cm-foldGutter {
          .cm-activeLineGutter {
            background-color: var(--color-block-alt);
          }
        }
      }

      .cm-content {
        padding: $space-md;

        .cm-line {
          &.cm-activeLine {
            background-color: var(--color-block-alt);
          }
        }
      }
    }
  }

  @media (max-width: 768px) {
    :deep(.cm-editor) {
      .cm-scroller {
        .cm-gutters {
          .cm-lineNumbers {
            .cm-gutterElement {
              padding-left: $space-lg;
            }
          }
        }
      }
    }
  }
}
</style>