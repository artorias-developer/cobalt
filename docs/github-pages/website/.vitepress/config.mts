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
        text: 'Getting Started',
        items: [
          { text: 'Installation', link: '/getting-started/installation' },
          { text: 'Testing', link: '/getting-started/testing' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/ArtoriasCode/cobalt' }
    ]
  }
})