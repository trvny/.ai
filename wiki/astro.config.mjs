import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://trvny.github.io',
  base: '/.ai',
  integrations: [
    starlight({
      title: 'Overprint',
      description: 'The .ai field guide: shared core, local overlays, one effective profile.',
      logo: { src: './src/assets/mark.svg' },
      favicon: '/favicon.svg',
      customCss: ['./src/styles/overprint.css'],
      head: [
        { tag: 'link', attrs: { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' } },
        { tag: 'link', attrs: { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400..800&display=swap' } },
      ],
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/trvny/.ai' }],
      sidebar: [
        { label: 'Start here', items: [
          { label: 'Overview', slug: '' },
          { label: 'Design principles', slug: 'principles' },
          { label: 'Overlays and composition', slug: 'overlays' },
          { label: 'Field notes', slug: 'field-notes' },
        ] },
      ],
    }),
  ],
});
