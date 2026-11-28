import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://trvny.github.io',
  base: '/.ai',
  integrations: [
    starlight({
      title: '.ai Wiki',
      description: 'Portable AI core: instructions, profiles, overlays, tools, templates and skills.',
      logo: { src: './src/assets/mark.svg' },
      favicon: '/.ai/favicon.svg',
      customCss: ['./src/styles/overprint.css'],
      head: [
        { tag: 'meta', attrs: { name: 'google-site-verification', content: 'xbXKq1w3ClpoMlxws6qobmZjpSmGVhi2xbrf7kwJV0s' } },
        { tag: 'link', attrs: { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' } },
        { tag: 'link', attrs: { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400..800&display=swap' } },
      ],
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/trvny/.ai' }],
      sidebar: [
        { label: 'Start here', items: [
          { label: 'Overview', slug: '' },
          { label: 'Core rules', slug: 'principles' },
          { label: 'Compose and render', slug: 'overlays' },
          { label: 'Repository map', slug: 'field-notes' },
        ] },
        { label: 'Guides', items: [{ autogenerate: { directory: 'guides' } }] },
        { label: 'Reference', items: [{ autogenerate: { directory: 'reference' } }] },
        { label: 'Tools', items: [{ autogenerate: { directory: 'tools' } }] },
        { label: 'Templates', items: [{ label: 'Overview', slug: 'templates' }, { autogenerate: { directory: 'templates' } }] },
        { label: 'Skills', slug: 'skills' },
      ],
    }),
  ],
});
