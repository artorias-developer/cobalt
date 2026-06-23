import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/cobalt/',
  title: 'Cobalt Documentation',
  description: 'Documentation for the Cobalt dashboard',
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Documentation', link: '/docs/getting-started/installation' }
    ],
    sidebar: [
      {
        text: 'Overview',
        items: [
          { text: 'Introduction', link: '/docs/overview/introduction' },
          { text: 'Terminology', link: '/docs/overview/terminology' }
        ]
      },
      {
        text: 'Getting started',
        items: [
          { text: 'Installation', link: '/docs/getting-started/installation' },
          { text: 'Testing', link: '/docs/getting-started/testing' }
        ]
      },
      {
        text: 'Development',
        items: [
          { text: 'Local installation', link: '/docs/development/local-installation' },
          { text: 'Adding a language', link: '/docs/development/adding-a-language' },
          { text: 'Adding a game', link: '/docs/development/adding-a-game' }
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/ArtoriasCode/cobalt' }
    ]
  }
})