import { fileURLToPath, URL } from "node:url"

import { defineConfig } from "vite"
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
      allowedHosts: true,
      ws: {
        protocol: "wss"
      }
    },
    build: {
      sourcemap: false,
      rolldownOptions: {
        output: {
          manualChunks: (id: string) => {
            if (!id.includes("node_modules/")) return

            const chunks: Record<string, string[]> = {
              vue: ["vue", "@vue", "vue-router", "vue-i18n", "@intlify", "pinia", "@babel/runtime"],
              echarts: ["echarts", "zrender"],
              editor: ["codemirror", "@codemirror", "@lezer", "@uiw/codemirror-theme-github"],
              qrcode: ["qr-code-styling"],
            }

            const path = id.split("node_modules/").pop()!
            const parts = path.split("/")
            const pkg = path.startsWith("@") ? `${parts[0]}/${parts[1]}` : parts[0]

            for (const [chunk, packages] of Object.entries(chunks)) {
              if (packages.some(p => pkg === p || pkg.startsWith(`${p}/`))) return chunk
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