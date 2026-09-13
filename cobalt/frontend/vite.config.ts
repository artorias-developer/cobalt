import { fileURLToPath, URL } from "node:url"

import { defineConfig, Plugin } from "vite"
import vue from "@vitejs/plugin-vue"


// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const isDev = process.env.APP_ENVIRONMENT === "dev"
  const appBase = process.env.APP_BASE_URL
  const appDomain = process.env.APP_DOMAIN

  return {
    define: {
      __VUE_PROD_DEVTOOLS__: false,
      __BUNDLED_DEV__: JSON.stringify(false),
      __VUE_I18N_FULL_INSTALL__: JSON.stringify(true),
      __VUE_I18N_LEGACY_API__: JSON.stringify(false),
      __SERVER_FORWARD_CONSOLE__: JSON.stringify(false),
    },
    plugins: [
      vue(),
      blockRootRedirect()
    ],
    base: getBase(appBase),
    server: {
      host: "0.0.0.0",
      port: 8011,
      strictPort: true,
      hmr: {
        protocol: "wss",
        host: "127.0.0.1",
        clientPort: 443,
      },
      allowedHosts: getAllowedHosts(isDev, appDomain),
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

/**
 * Resolves the `allowedHosts` list for the Vite dev server.
 *
 * In dev mode, returns a fixed list of known local/tunnel hosts.
 * In non-dev mode, requires `appDomain` to be set and restricts access to that host only.
 *
 * Parameters:
 * - isDev: Whether the app is running in development mode.
 * - appDomain: The production domain (e.g. from `APP_DOMAIN` env var). Required when `isDev` is false.
 *
 * Returns:
 * - string[] | true: An array of allowed hosts.
 *
 * Throws:
 * - Error: If `isDev` is false and `appDomain` is not provided.
 */
function getAllowedHosts(isDev: boolean, appDomain?: string): string[] | true {
  if (isDev) {
    return ["localhost", "127.0.0.1", ".ngrok-free.app"]
  }

  if (!appDomain) {
    throw new Error("APP_DOMAIN is required in production")
  }

  return [appDomain]
}

/**
 * Vite plugin that blocks requests to the root path ("/") during development,
 * returning a 404 instead. Used to prevent access outside the app's base path.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Plugin: A Vite plugin instance.
 */
function blockRootRedirect(): Plugin {
  return {
    name: "block-root-redirect",
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        if (req.url === "/") {
          res.statusCode = 404
          res.end("Not Found")
          return
        }
        next()
      })
    }
  }
}