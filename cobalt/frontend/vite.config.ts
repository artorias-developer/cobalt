import { fileURLToPath, URL } from "node:url"

import { defineConfig, Plugin } from "vite"
import vue from "@vitejs/plugin-vue"


// https://vite.dev/config/
export default defineConfig(() => {
  return {
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
    base: getBase(process.env.APP_BASE_URL),
    server: {
      host: "0.0.0.0",
      port: 8011,
      strictPort: true,
      hmr: {
        protocol: "wss",
        host: "127.0.0.1",
        clientPort: 443,
      },
      allowedHosts: ["localhost", "127.0.0.1", ".ngrok-free.app"],
    },
    build: {
      sourcemap: false,
      rolldownOptions: {
        output: {
          manualChunks: (id: string) => {
            const chunks: Record<string, string[]> = {
              vue: ["vue", "vue-router", "vue-i18n", "pinia", "@babel/runtime"],
              echarts: ["echarts"],
              editor: ["codemirror", "@codemirror", "@lezer", "@uiw/codemirror-theme-github"],
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
        "qr-code-styling",
        "@uiw/codemirror-theme-github"
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
  }
})

/**
 * Resolves the Vite `base` path from the app's base segment.
 *
 * Parameters:
 * - appBase: The app base segment (e.g. from `APP_BASE` env var), without leading/trailing slashes.
 *
 * Returns:
 * - string: `/${appBase}/` if `appBase` is set, otherwise `/`.
 */
function getBase(appBase?: string): string {
  return appBase ? `/${appBase}/` : '/'
}