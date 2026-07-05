import { fileURLToPath, URL } from "node:url"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"

// https://vite.dev/config/
export default defineConfig({
  define: {
    __VUE_PROD_DEVTOOLS__: false,
    __BUNDLED_DEV__: JSON.stringify(false),
    __VUE_I18N_FULL_INSTALL__: JSON.stringify(true),
    __VUE_I18N_LEGACY_API__: JSON.stringify(false),
    __SERVER_FORWARD_CONSOLE__: JSON.stringify(false),
  },
  plugins: [
    vue()
  ],
  server: {
    host: "0.0.0.0",
    port: 8011,
    strictPort: true,
    hmr: {
      protocol: "wss",
      host: "127.0.0.1",
      clientPort: 443,
    },
  },
  build: {
    sourcemap: false,
    rolldownOptions: {
      output: {
        manualChunks: (id: string) => {
          const chunks: Record<string, string[]> = {
            vue: ["vue", "vue-router", "vue-i18n", "pinia"],
            echarts: ["echarts"],
            editor: ["codemirror", "@codemirror", "@lezer", "@uiw/codemirror-theme-github", "@babel/runtime"],
            qrcode: ["qr-code-styling"],
          }

          for (const [chunk, packages] of Object.entries(chunks)) {
            if (packages.some(pkg => id.includes(pkg))) return chunk
          }
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
      "vue-i18n",
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
        @use "@/assets/styles/variables/themes" as *;
        @use "@/assets/styles/variables/spacing" as *;
        @use "@/assets/styles/variables/fonts" as *;
        @use "@/assets/styles/globals" as *;
        @use "@/assets/styles/mixins" as *;
        `
      }
    }
  }
})
