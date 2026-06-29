import { defineConfig } from "vitepress"

export default defineConfig({
  base: "/cobalt/",
  title: "Cobalt",
  description: "Documentation for the Cobalt dashboard",
  head: [
    ["link", { rel: "icon", href: "/cobalt/assets/images/svg/logo.svg" }]
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
            items: [
              { text: "Roles", link: "/docs/tutorials/roles" },
              { text: "Users", link: "/docs/tutorials/users" },
              { text: "Servers", link: "/docs/tutorials/servers" }
            ]
          },
          {
            text: "Games",
            items: [
              { text: "Minecraft", link: "/docs/tutorials/minecraft" },
              { text: "Terraria", link: "/docs/tutorials/terraria" },
              { text: "Don't Starve Together", link: "/docs/tutorials/dont-starve-together" },
              { text: "Factorio", link: "/docs/tutorials/factorio" }
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
      { icon: "github", link: "https://github.com/ArtoriasCode/cobalt" }
    ]
  }
})