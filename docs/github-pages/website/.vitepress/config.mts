import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/cobalt/',
  title: 'Cobalt Documentation',
  description: 'Documentation for the Cobalt dashboard',
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Documentation', link: '/getting-started/installation' }
    ],
    sidebar: [
      {
        text: 'Getting started',
        items: [
          { text: 'Installation', link: '/getting-started/installation' },
          { text: 'Testing', link: '/getting-started/testing' }
        ]
      },
      {
        text: 'Development',
        items: [
          { text: 'Local installation', link: '/development/local-installation' },
          { text: 'Adding a language', link: '/development/adding-a-language' },
          { text: 'Adding a game', link: '/development/adding-a-game' }
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/ArtoriasCode/cobalt' }
    ]
  }
})