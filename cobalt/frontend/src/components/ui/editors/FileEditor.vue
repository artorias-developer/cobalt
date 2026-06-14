<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div ref="container" class="codemirror-editor"/>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue"

import { basicSetup } from "codemirror"
import { EditorState, Compartment, type Extension } from "@codemirror/state"
import { EditorView, keymap } from "@codemirror/view"
import { defaultKeymap } from "@codemirror/commands"
import { StreamLanguage, HighlightStyle, syntaxHighlighting } from "@codemirror/language"
import { tags } from "@lezer/highlight"
import { highlightSelectionMatches } from "@codemirror/search"
import { oneDark } from "@codemirror/theme-one-dark"
import { json } from "@codemirror/lang-json"
import { xml } from "@codemirror/lang-xml"
import { yaml } from "@codemirror/lang-yaml"
import { lua } from "@codemirror/legacy-modes/mode/lua"
import { shell } from "@codemirror/legacy-modes/mode/shell"
import { properties } from "@codemirror/legacy-modes/mode/properties"

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

let view: EditorView | null = null
const container = ref<HTMLElement | null>(null)
const languageCompartment = new Compartment()

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
        oneDark,
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
    background-color: $color-block;
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
      border-left-color: $color-text;
    }

    .cm-scroller {
      overscroll-behavior: none;
      @include scrollbar();

      .cm-gutters {
        background-color: $color-block;
        border: none;
        border-right: 1px solid $color-border;
        padding-left: 0;

        .cm-lineNumbers {
          .cm-gutterElement {
            padding-left: $space-xl;

            &.cm-activeLineGutter {
              background-color: $color-block-alt;
              color: $color-title;
            }
          }
        }
      }

      .cm-content {
        padding: $space-md;

        .cm-line {
          &.cm-activeLine {
            background-color: $color-block-alt;
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