import { fileURLToPath, URL } from "node:url"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"

// https://vite.dev/config/
export default defineConfig({
  define: {
    __VUE_PROD_DEVTOOLS__: false
  },
  plugins: [
    vue()
  ],
  build: {
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vue: [
            "vue",
            "vue-router",
            "pinia"
          ],
          echarts: [
            "echarts"
          ],
          codemirror: [
            "codemirror",
            "@codemirror/state",
            "@codemirror/view",
            "@codemirror/language",
            "@codemirror/commands",
            "@codemirror/lang-json",
            "@codemirror/lang-xml",
            "@codemirror/lang-yaml",
            "@codemirror/theme-one-dark",
            "@lezer/highlight"
          ],
          "qrcode": [
            "qr-code-styling"
          ]
        }
      }
    }
  },
  optimizeDeps: {
    include: [
      "echarts",
      "axios",
      "pinia",
      "vue-router",
      "@kyvg/vue3-notification",
      "qr-code-styling"
    ]
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL("./src", import.meta.url))
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
        @use "@/assets/styles/variables/colors" as *;
        @use "@/assets/styles/variables/spacing" as *;
        @use "@/assets/styles/variables/fonts" as *;
        @use "@/assets/styles/globals" as *;
        @use "@/assets/styles/mixins" as *;
        `
      }
    }
  }
})
