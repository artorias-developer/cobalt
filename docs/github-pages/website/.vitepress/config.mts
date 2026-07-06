import { defineConfig } from "vitepress"

export default defineConfig({
  title: "Cobalt",
  description: "Documentation for the Cobalt dashboard",
  head: [
    ["link", { rel: "icon", href: "/cobalt/assets/images/svg/logo.svg" }],
    ["meta", { name: "google-site-verification", content: "RtxZJ237LBxMmW3QHsFhSu8rIBtkiPpK1JiDNfBG6yg" }],
    ["meta", { name: "google-adsense-account", content: "ca-pub-2553125098165337" }]
  ],
  themeConfig: {
    logo: "/assets/images/svg/logo.svg",
    nav: [
      { text: "Home", link: '/' },
      { text: "Documentation", link: "/docs/overview/introduction" }
    ],
    sidebar: [
      {
        text: "Overview",
        items: [
          { text: "Introduction", link: "/docs/overview/introduction" },
          { text: "Terminology", link: "/docs/overview/terminology" }
        ]
      },
      {
        text: "Getting started",
        items: [
          { text: "Installation", link: "/docs/getting-started/installation" },
          { text: "Testing", link: "/docs/getting-started/testing" }
        ]
      },
      {
        text: "Tutorials",
        items: [
          {
            text: "Dashboard",
            collapsed: true,
            items: [
              { text: "Roles", link: "/docs/tutorials/dashboard/roles" },
              { text: "Users", link: "/docs/tutorials/dashboard/users" },
              { text: "Servers", link: "/docs/tutorials/dashboard/servers" }
            ]
          },
          {
            text: "Games",
            collapsed: true,
            items: [
              { text: "Minecraft", link: "/docs/tutorials/games/minecraft" },
              { text: "Terraria", link: "/docs/tutorials/games/terraria" },
              { text: "Don't Starve Together", link: "/docs/tutorials/games/dont-starve-together" },
              { text: "Factorio", link: "/docs/tutorials/games/factorio" },
              { text: "RimWorld", link: "/docs/tutorials/games/rim-world" },
              { text: "7 Days to Die", link: "/docs/tutorials/games/seven-days-to-die" },
              { text: "Project Zomboid", link: "/docs/tutorials/games/project-zomboid" }
            ]
          }
        ]
      },
      {
        text: "Development",
        items: [
          { text: "Local installation", link: "/docs/development/local-installation" },
          { text: "Adding a language", link: "/docs/development/adding-a-language" },
          { text: "Adding a game", link: "/docs/development/adding-a-game" }
        ]
      }
    ],
    socialLinks: [
      { icon: "github", link: "https://github.com/artorias-developer/cobalt" }
    ]
  }
})